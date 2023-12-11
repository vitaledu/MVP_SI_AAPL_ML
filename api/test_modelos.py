from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dados = "database/AAPL.csv"
colunas = [
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
]

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)


def normalize(value):
    if value > 400623065:
        return 1
    else:
        return 0

# Remove as linhas com valores NaN
dataset = dataset.dropna()


# Separando em dados de entrada e saída
X = dataset.iloc[:, 1:5]
Y = dataset.iloc[:, 5]

Y = Y.astype(float)

print("Valores de entrada X:")
print(X)

print("\nValores de saída y:")
print(Y)

with open('database/AAPL.csv', 'r') as file:
    for _ in range(5):  # Exibir as primeiras 5 linhas
        print(file.readline())

print(dataset.info())  # Verificar informações do DataFrame
print(dataset.describe())  # Resumo estatístico do DataFrame



# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"


def test_modelo_lr():
    # Importando o modelo de regressão logística
    lr_path = "ml_model/apple_lr.pkl"
    modelo_lr = Model.carrega_modelo(lr_path)

    # Obtendo as métricas da Regressão Logística
    acuracia_lr, recall_lr, precisao_lr, f1_lr = avaliador.avaliar(
        modelo_lr, X, Y)

    # Testando as métricas da Regressão Logística
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_lr >= 0.75
    assert recall_lr >= 0.5
    assert precisao_lr >= 0.5
    assert f1_lr >= 0.5

# Método para testar modelo KNN a partir do arquivo correspondente


def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = 'ml_model/apple_knn.pkl'
    modelo_knn = Model.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn, recall_knn, precisao_knn, f1_knn = avaliador.avaliar(
        modelo_knn, X, Y)

    # Testando as métricas do KNN
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_knn >= 0.75
    assert recall_knn >= 0.5
    assert precisao_knn >= 0.5
    assert f1_knn >= 0.5
