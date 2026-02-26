from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.conversacion import Conversacion
from app.routes import conversacion_routes
from app.models.mensaje import Mensaje
import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/conversacion/iniciar/{usuario_id}")
def iniciar_conversacion(usuario_id: int, db: Session = Depends(get_db)):
    conversacion = Conversacion(usuario_id=usuario_id)
    db.add(conversacion)
    db.commit()
    db.refresh(conversacion)
    return conversacion

@router.post("/mensaje/{conversacion_id}")
def guardar_mensaje(conversacion_id: int, remitente: str, contenido: str, db: Session = Depends(get_db)):
    mensaje = Mensaje(
        conversacion_id=conversacion_id,
        remitente=remitente,
        contenido=contenido
    )
    db.add(mensaje)
    db.commit()
    db.refresh(mensaje)
    return mensaje

@router.put("/conversacion/finalizar/{conversacion_id}")
def finalizar_conversacion(conversacion_id: int, db: Session = Depends(get_db)):
    conversacion = db.query(Conversacion).filter(
        Conversacion.id == conversacion_id
    ).first()

    conversacion.estado = "finalizada"
    conversacion.fecha_fin = datetime.datetime.now()
    db.commit()

    return {"mensaje": "Conversación finalizada"}

@router.get("/conversacion/{conversacion_id}")
def ver_historial(conversacion_id: int, db: Session = Depends(get_db)):
    mensajes = db.query(Mensaje).filter(
        Mensaje.conversacion_id == conversacion_id
    ).all()

    return mensajes