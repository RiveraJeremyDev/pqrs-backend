from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, unique=True)
    correo = Column(String, nullable=False)
    documento = Column(String)
    programa = Column(String)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())