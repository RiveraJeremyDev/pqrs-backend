from sqlalchemy import Column, Integer, ForeignKey, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.config.database import Base

class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    conversacion_id = Column(Integer, ForeignKey("conversaciones.id"))
    remitente = Column(String)  # usuario o ia
    contenido = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, server_default=func.now())