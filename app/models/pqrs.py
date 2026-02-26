from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.config.database import Base

class Pqrs(Base):
    __tablename__ = "pqrs"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(String, default="pendiente")
    radicado = Column(String)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())