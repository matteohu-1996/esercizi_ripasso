import enum

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
from models.relazioni import voce_tags_extra


class StatoPrestito(str, enum.Enum):
    PRENOTATO = 'PRENOTATO'
    RITIRATO = 'RITIRATO'
    RESTITUITO = 'RESTITUITO'
    IN_RITARDO = 'IN RITARDO'

class Prestito(Base):
    __tablename__ = "prestiti"

    prestito_id = Column(Integer, primary_key=True, index=True)
    data_ora = Column(DateTime, index=True)
    stato = Column(Enum(StatoPrestito), default=StatoPrestito.PRENOTATO)
    note = Column(Text,nullable=True)

    lettore_id = Column(Integer, ForeignKey("lettori.lettore_id"))
    lettore = relationship("Lettore", back_populates="prestiti")
    voci = relationship("VocePrestito", back_populates="prestito", cascade="all, delete-orphan")

class VocePrestito(Base):
    __tablename__ = "voce_prestiti"

    voce_id = Column(Integer, primary_key=True, index=True)
    quantita = Column(Integer, default=1)

    prestito_id = Column(Integer, ForeignKey("prestiti.prestito_id"))
    libro_id = Column(Integer, ForeignKey("libri.libro_id"))

    prestito = relationship("Prestito", back_populates="voci")
    libro = relationship("Libro", back_populates="voci")

    tags_extra = relationship("Tag", secondary=voce_tags_extra, back_populates="voci_extra")
