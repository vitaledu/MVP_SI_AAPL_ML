from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
import joblib

from sqlalchemy.exc import IntegrityError

from model import Session, Acao, Model
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)

acao_tag = Tag(
    name="Acao",
    description="Adição, visualização, remoção e predição de Ações da Apple",
)


# Rota home
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect("/openapi")


# Rota de listagem de ações
@app.get(
    "/acoes",
    tags=[acao_tag],
    responses={"200": AcaoViewSchema, "404": ErrorSchema},
)
def get_acoes():
    """Lista todos as negociações cadastradas na base
    Retorna uma lista de negociações cadastradas na base.

    Args:
        id (int): número da operação de negociação

    Returns:
        list: lista de negociações cadastradas na base
    """
    session = Session()

    # Buscando todos as ações
    acoes = session.query(Acao).all()

    if not acoes:
        logger.warning("Não há negociações cadastradas na base :/")
        return {"message": "Não há negociações cadastradas na base :/"}, 404
    else:
        logger.debug(f"%d negociações encontradas" % len(acoes))
        return apresenta_acoes(acoes), 200


# Rota de adição de negociação
@app.post(
    "/acao",
    tags=[acao_tag],
    responses={"200": AcaoViewSchema, "400": ErrorSchema, "409": ErrorSchema},
)
def predict(form: AcaoSchema):
    """Adiciona um novo registro de ações à base de dados

        Args:
            open (int): valor que abriu a ação
            high (int): valor mais alto da ação
            low (int): valor mais baixo da ação
            close (int): valor que fechou a ação
            adjclose (int): valor ajustado da ação

    Returns:
        dict: ações da Apple cadastradas na base
    """

    # Carregando modelo
    ml_path = "ml_model/apple_lr.pkl"
    scaler_path = "ml_model/scaler.joblib"
    modelo = Model.carrega_modelo(ml_path, scaler_path)

    acao = Acao(
        open=form.open,
        high=form.high,
        low=form.low,
        close=form.close,
        adjclose=form.adjclose,
        volume=Model.preditor(modelo, form),
    )
    logger.debug(f"Adicionando negociação: '{acao.id}'")

    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando negociação
        session.add(acao)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        
        return apresenta_acao(acao), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar nova negociação :/"
        logger.warning(
            f"Erro ao adicionar nova negociação '{acao.id}', {error_msg}")
        return {"message": error_msg}, 400


# Métodos baseados em id
# Rota de busca de negociação por id
@app.get(
    "/acao",
    tags=[acao_tag],
    responses={"200": AcaoViewSchema, "404": ErrorSchema},
)
def get_acao(query: AcaoBuscaSchema):
    """Faz a busca de uma negociação cadastrada na base a partir do id

    Args:
        id (int): número de identificação da negociação

    Returns:
        dict: representação da negociação cadastrada na base
    """

    acao_id = query.id
    logger.debug(f"Coletando dados sobre produto #{acao_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    acao = session.query(Acao).filter(Acao.id == acao_id).first()

    if not acao:
        # se a negociação não foi encontrada
        error_msg = f"Negociação {acao_id} não encontrada na base."
        logger.warning(f"Erro ao buscar negociação '{acao_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Negociação econtrada: '{acao.id}'")
        # retorna a representação de negociação
        return apresenta_acao(acao), 200


# Rota de remoção de negociação por id
@app.delete(
    "/acao",
    tags=[acao_tag],
    responses={"200": AcaoViewSchema, "404": ErrorSchema}
)
def delete_acao(query: AcaoBuscaSchema):
    """Remove uma negociação cadastrada na base a partir do id

    Args:
        id (int): id da negociação a ser removida

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    acao_id = query.id
    logger.debug(f"Deletando dados sobre negociação #{acao_id}")

    # Criando conexão com a base
    session = Session()

    # Buscando negociação
    acao = session.query(Acao).filter(Acao.id == acao_id).first()

    if not acao:
        error_msg = "Negociação não encontrada na base."
        logger.warning(f"Erro ao deletar negociação '{acao_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(acao)
        session.commit()
        logger.debug(f"Deletado negociação #{acao_id}")
        return {"message": f"Negociação {acao_id} removida com sucesso!"}, 200
    

