from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.schemas.pqrs_schema import PqrsCreate
from app.services.pqrs_service import PqrsService
from app.models.pqrs import Pqrs

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