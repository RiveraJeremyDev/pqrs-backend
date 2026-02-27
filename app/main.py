from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes import pqrs_routes
from app.routes import conversacion_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(pqrs_routes.router, prefix="/api")

app.include_router(conversacion_routes.router, prefix="/api")

origins = [
    "https://pqrscul.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)