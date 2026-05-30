from sqlalchemy.orm import Session
from app.database.models import HistorialConversacion


def guardar_mensaje(db: Session, usuario_id: int, role: str, contenido: str):
    mensaje = HistorialConversacion(
        UsuarioId=usuario_id,
        Role=role,
        Contenido=contenido
    )
    db.add(mensaje)
    db.commit()


def obtener_historial(db: Session, usuario_id: int, limite: int = 50) -> list[dict]:
    mensajes = (
        db.query(HistorialConversacion)
        .filter(HistorialConversacion.UsuarioId == usuario_id)
        .order_by(HistorialConversacion.Fecha.asc())
        .limit(limite)
        .all()
    )
    return [
        {
            "role": m.Role,
            "content": m.Contenido
        }
        for m in mensajes
    ]


def limpiar_historial(db: Session, usuario_id: int):
    db.query(HistorialConversacion).filter(
        HistorialConversacion.UsuarioId == usuario_id
    ).delete()
    db.commit()
