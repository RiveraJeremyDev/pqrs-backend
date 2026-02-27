from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.schemas.pqrs_schema import PqrsCreate
from app.services.pqrs_service import PqrsService
from app.models.pqrs import Pqrs
import requests
import os

TINY_LLAMA_URL = "https://droughty-tropologically-venessa.ngrok-free.dev/chat"

WHATSAPP_TOKEN = os.getenv("EAAMt3dqxU8QBQwtQdEjzfOVG2njMSFEXCPNUir5Om5ce9dlIPaf1ZBDETxOuiOrBQ5Pey9Gbkm662EDK2tfU2HpmZCE3mX9rEfpyOkRMIgqeONlMaK7y2ZCXpsE9vWUGndhXjTSLerqdkIPMcySSYF2J0E31jCZANoqtFAhciU3kGtIWAjW7eLi4YGhUJc0PHriPSwX6yX6kkcVCw4rHlPyEmDPlwa0Eije6mg8ZAZA7RBBJxC2pi3ArsZC1VuQWClrr5RTJnUujGoutf55RplXKDa9HraybZBaX4ZA4UDAZDZD")
PHONE_NUMBER_ID = os.getenv("938175122722689")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pqrs")
def crear_pqrs(data: PqrsCreate, db: Session = Depends(get_db)):
    radicado = PqrsService.crear_pqrs(db, data)
    return {"success": True, "radicado": radicado}

# ==========================
# GET - Listar PQRS (con filtros)
# ==========================
@router.get("/pqrs")
def listar_pqrs(
    tipo: str = None,
    estado: str = None,
    fecha: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Pqrs)

    if tipo:
        query = query.filter(Pqrs.tipo == tipo)

    if estado:
        query = query.filter(Pqrs.estado == estado)

    if fecha:
        query = query.filter(Pqrs.fecha_creacion.cast(str).like(f"{fecha}%"))

    resultados = query.all()

    return resultados

def generar_respuesta_ia(datos):

    payload = {
        "tipo": datos["tipo"],
        "nombre": datos["nombre"],
        "mensaje": datos["mensaje"],
        "programa": datos.get("programa", ""),
        "telefono": datos["telefono"]
    }

    r = requests.post(TINY_LLAMA_URL, json=payload, timeout=60)

    return r.json()["respuesta"]

def enviar_whatsapp(numero, mensaje):

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensaje
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print("WhatsApp response:", response.text)

@router.post("/api/pqrs")
async def recibir_pqrs(data: dict):

    # 1 Generar respuesta IA
    respuesta_ia = generar_respuesta_ia(data)

    # 2 Enviar por WhatsApp al número que el usuario digitó
    enviar_whatsapp(data["telefono"], respuesta_ia)

    # 3 Generar radicado (ejemplo simple)
    import uuid
    radicado = str(uuid.uuid4())[:8]

    return {
        "mensaje": "PQRS recibida",
        "radicado": radicado
    }