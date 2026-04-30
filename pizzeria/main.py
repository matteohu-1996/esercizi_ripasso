
from fastapi import FastAPI
from database import engine, Base
from routers import ingrediente

# Crea tutte le tabelle come descritto in models
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="API Pizzeria Completa",
    description="Esercizio per gestire pizzeria",
    version="1.0.0",
)

app.include_router(ingrediente.router)
# Da ripetere per tutti i router

# Altra cosa qua: Gestione CORS e Middleware

@app.get("/")
def root():
    return {"message": "Da Mario"}

