from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from pizzeria.database import Base

class Cliente(Base):
    __tablename__ = 'clienti'

    cliente_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True)
    telefono = Column(String(30))
    indirizzo = Column(String(100))

    # relazione con gli ordini
    ordini = relationship("Ordine", back_populates="cliente")

