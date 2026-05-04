from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

libro_tags = Table(
    "libro_tags",
    Base.metadata,
    Column("libro_id", Integer, ForeignKey("libri.libro_id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.tag_id"), primary_key=True),
)

voce_tags_extra = Table(
    "voce_tags_extra",
    Base.metadata,
# CORRETTO
Column("voce_id", Integer, ForeignKey("voce_prestiti.voce_id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.tag_id"), primary_key=True),
)
