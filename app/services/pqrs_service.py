from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.pqrs import Pqrs
import time
import datetime

class PqrsService:

    @staticmethod
    def crear_pqrs(db: Session, data):

        usuario = Usuario(
            nombre=data.nombre,
            telefono=data.telefono,
            correo=data.correo,
            documento=data.documento,
            programa=data.programa
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        radicado = f"PQRS-{datetime.datetime.now().year}-{int(time.time())}"

        pqrs = Pqrs(
            usuario_id=usuario.id,
            tipo=data.tipo,
            descripcion=data.mensaje,
            radicado=radicado
        )

        db.add(pqrs)
        db.commit()
        db.refresh(pqrs)

        return radicado