from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

app = FastAPI(
    title="API Pizzeria",
    description="Mini ripasso per gestire pizzeria",
    version="1.0.0",
)

