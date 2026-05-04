from fastapi import FastAPI
from database import engine, Base
from routers import libri, prestiti



Base.metadata.create_all(engine)

app = FastAPI(
    title="Biblioteca Civica Aldrovandi",
    description="backend per una biblioteca che gestisce il catalogo, i tag descrittivi e i prestiti dei lettori.",
    version="1.0.0",
)

app.include_router(libri.router)
app.include_router(prestiti.router)


@app.get("/")
def main():
    return {"message": "Benvenuto nella Biblioteca Civica Aldrovandi"}