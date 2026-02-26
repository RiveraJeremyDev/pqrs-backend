from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP
from sqlalchemy.sql import func
from app.config.database import Base

class Conversacion(Base):
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_inicio = Column(TIMESTAMP, server_default=func.now())
    fecha_fin = Column(TIMESTAMP)
    estado = Column(String, default="activa")