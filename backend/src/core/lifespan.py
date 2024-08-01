from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.core.const import _genv
from src.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init(_genv("DB_URL"))
    # await db.init_models()
    
    yield
