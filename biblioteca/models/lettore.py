from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Lettore(Base):
    __tablename__ = "lettori"

    lettore_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True)
    telefono = Column(String(30), index=True)
    email = Column(String(100), index=True)
    tessera = Column(String(30), index=True, nullable=False)

    prestiti = relationship("Prestito", back_populates="lettore")