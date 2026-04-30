import enum
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from pizzeria.database import Base
from models.relazioni import voce_ingrediente_extra



class StatoOrdine(str, enum.Enum):
    RICEVUTO = "ricevuto"
    IN_PREPARAZIONE = "in_preparazione"
    PRONTO = "pronto"
    CONSEGNATO = "consegnato"


class Ordine(Base):
    __tablename__ = "ordini"

    ordine_id = Column(Integer, primary_key=True, index=True)
    data_ora = Column(DateTime)
    stato = Column(Enum(StatoOrdine), default=StatoOrdine.RICEVUTO)
    note = Column(Text,nullable=True)


    # relazioni con cliente e pizza
    cliente_id = Column(Integer, ForeignKey("clienti.cliente.id"))
    pizza_id = Column(Integer, ForeignKey("pizze.pizza.id"))

    # relazioni inverse
    cliente = relationship("Cliente", back_populates="ordini")
    pizza = relationship("Pizza", back_populates="ordini")
    voci = relationship("VocePizzaOrdine", back_populates="ordine", cascade="all, delete-orphan")

class VocePizzaOrdine(Base):
    __tablename__ = "voci_ordine"

    voce_id = Column(Integer, primary_key=True, index=True)
    quantita = Column(Integer, default=1)

    ordine_id = Column(Integer, ForeignKey("ordini.ordine_id"))
    pizze_id = Column(Integer, ForeignKey("pizze.pizza_id"))

    ordine = relationship("Ordine", back_populates="voci")
    pizza = relationship("Pizza", back_populates="voci")

    ingredienti_extra = relationship("Ingrediente", secondary="voce_ingredienti_extra", back_populates="voci_extra")