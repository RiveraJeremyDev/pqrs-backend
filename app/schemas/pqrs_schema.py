from pydantic import BaseModel

class PqrsCreate(BaseModel):
    nombre: str
    correo: str
    documento: str | None = None
    programa: str | None = None
    tipo: str
    mensaje: str