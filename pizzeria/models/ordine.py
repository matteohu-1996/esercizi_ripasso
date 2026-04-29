import enum

from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from pizzeria.database import Base
from datetime import datetime

class Ordine(Base):
    __tablename__ = "ordini"

    ordine_id = Column(Integer, primary_key=True, index=True)
    quantita = Column(Integer, default=1)
    nome = Column(String(30), index=True)
    data_ora = datetime
    stato = enum.Enum("ricevuto", "in_preparazione", "pronto", "consegnato")

    # relazioni con cliente e pizza
    id_cliente = Column(Integer, ForeignKey("clienti.cliente.id"))
    id_pizza = Column(Integer, ForeignKey("pizze.pizza.id"))

    # relazioni inverse
    cliente = relationship("Cliente", back_populates="ordini")
    pizza = relationship("Pizza", back_populates="ordini")