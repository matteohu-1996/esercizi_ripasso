from sqlalchemy import Table, Column, Integer, String, Float, Boolean, ForeignKey
from database import Base


# RELAZIONE MOLTI A MOLTI N a N
pizza_ingredienti = Table(
    'pizza_ingredienti',
    Base.metadata,
    Column("pizza_id",
           Integer,
           ForeignKey("pizze.pizza_id"),
           primary_key=True
    ),
    Column(
        "ingrediente_id",
        Integer,
        ForeignKey("ingredienti.ingrediente_id"),
        primary_key=True
    )
)

voce_ingrediente_extra = Table(
    'voce_ingrediente_extra',
    Base.metadata,
    Column("voce_id",
           Integer,
           ForeignKey("voci_ordine.voce_id"),
           primary_key=True
    ),
    Column(
        "ingrediente_id",
        Integer,
        ForeignKey("ingredienti.ingrediente_id"),
        primary_key=True
    )
)