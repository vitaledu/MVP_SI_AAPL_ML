from pydantic import BaseModel
from typing import Optional, List
from model.acao import Acao
import json
import numpy as np


class AcaoSchema(BaseModel):
    """ Define uma nova acao a ser inserido no banco
    """
    open: float = 0.503348
    high: float = 0.517857
    low: float = 0.453125
    close: float = 0.459821
    adjclose: float = 0.389781


class AcaoViewSchema(BaseModel):
    """Define como a ação será retornada
    """
    id: int = 1
    open: float = 0.503348
    high: float = 0.517857
    low: float = 0.453125
    close: float = 0.459821
    adjclose: float = 0.389781
    volume: Optional[float] = 0.389781


class AcaoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no id da negociação.
    """
    id: int = 1


class ListaAcoesSchema(BaseModel):
    """Define como uma lista de negociações de ações será representada
    """
    acoes: List[AcaoSchema]


class AcaoDelSchema(BaseModel):
    """Define como uma negociação será deletada
    """
    id: int = 1

# Apresenta apenas os dados de uma ação


def apresenta_acao(acao: Acao):
    """ Retorna uma representação de uma negociação seguindo o schema definido em
        AcaoViewSchema.
    """
    return {
        "id": acao.id,
        "open": acao.open,
        "high": acao.high,
        "low": acao.low,
        "close": acao.close,
        "adjclose": acao.adjclose,
        "volume": acao.volume,
    }

# Apresenta uma lista de ações


def apresenta_acoes(acoes: List[Acao]):
    """ Retorna uma representação da negociações seguindo o schema definido em
        AcaoViewSchema.
    """
    result = []
    for acao in acoes:
        result.append(
            {
                "id": acao.id,
                "open": acao.open,
                "high": acao.high,
                "low": acao.low,
                "close": acao.close,
                "adjclose": acao.adjclose,
                "volume": acao.volume
            }
        )

    return {"acoes": result}
