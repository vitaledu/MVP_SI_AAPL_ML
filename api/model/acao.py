from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

# colunas = Open, High, Low, Close, AdjClose, Volume


class Acao(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key=True)
    open = Column("Open", Float)
    high = Column("High", Float)
    low = Column("Low", Float)
    close = Column("Close", Float)
    adjclose = Column("AdjClose", Float)

    volume = Column("Volume", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        open: float,
        high: float,
        low: float,
        close: float,
        adjclose: float, 
        volume: int,
        data_insercao: Union[DateTime, None] = None
    ):
        """
        Cria um histórico de ação

        Arguments:
            open: valor que abriu a ação
            high: valor mais alto da ação
            low: valor mais baixo da ação
            close: valor que fechou a ação
            adjclose: valor ajustado da ação
            volume: volume de ações negociadas
            data_insercao: data de quando a ação foi inserida no banco
        """
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adjclose = adjclose
        self.volume = volume

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
