from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base
from sqlalchemy.orm import relationship
from models.relazioni import pizza_ingredienti

class Pizza(Base):
    __tablename__ = 'pizze'

    pizza_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), unique=True, index=True)
    prezzo_base = Column(Float)
    descrizione = Column(String(500), nullable=True)
    disponibile = Column(Boolean,default=True)


    # relazione: una pizza può essere richiesta in molti ordini
    ordini = relationship("Ordine", back_populates="pizza")
    ingredienti = relationship("Ingrediente",secondary=pizza_ingredienti,back_populates="pizze")
    voci = relationship("VocePizzaOrdine",back_populates="pizza")

    @property
    # rende cosa scritto sotto cos'è un attributo
    def prezzo_totale(self):
        return self.prezzo_base + ...