from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.relazioni import libro_tags

from models.prestito import VocePrestito


class Libro(Base):
    __tablename__ = "libri"

    libro_id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String(100), unique=True, index=True)
    isbn = Column(String(30), unique=True, index=True)
    anno = Column(Integer, index=True)
    descrizione = Column(String(100),nullable=False)
    durata_base = Column(Integer, nullable=False)
    disponibile = Column(Boolean, default=True, index=True)

    tags = relationship("Tag",secondary=libro_tags, back_populates="libri")
    voci = relationship("VocePrestito", back_populates="libro")

    @property
    def durata_totale(self):
        return self.durata_base + sum(i.giorni_extra for i in self.tags)