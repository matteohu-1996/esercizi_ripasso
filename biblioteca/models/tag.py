from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from models.relazioni import voce_tags_extra


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True,unique=True)
    nome = Column(String(30), unique=True, index=True)
    giorni_extra = Column(Integer, default=0, nullable=False)
    riservato = Column(Boolean, default=False, nullable=False)
    didattico = Column(Boolean, default=False, nullable=False)

    libri = relationship("Libri", back_populates="tags")
    voci_extra = relationship("VocePrestito", secondary=voce_tags_extra, back_populates="tags_extra")