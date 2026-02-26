from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes import pqrs_routes
from app.routes import conversacion_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(pqrs_routes.router, prefix="/api")

app.include_router(conversacion_routes.router, prefix="/api")