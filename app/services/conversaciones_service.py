from sqlalchemy.orm import Session
from app.database.models import Conversacion, HistorialConversacion


def crear_conversacion(db: Session, usuario_id: int, titulo: str = "Nueva conversación") -> dict:
    conv = Conversacion(UsuarioId=usuario_id, Titulo=titulo)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"id": conv.Id, "titulo": conv.Titulo}


def listar_conversaciones(db: Session, usuario_id: int) -> list[dict]:
    convs = (
        db.query(Conversacion)
        .filter(Conversacion.UsuarioId == usuario_id, Conversacion.Activa == True)
        .order_by(Conversacion.FechaCreacion.desc())
        .all()
    )
    return [
        {
            "id": c.Id,
            "titulo": c.Titulo,
            "fecha": c.FechaCreacion.strftime("%d/%m/%Y %H:%M")
        }
        for c in convs
    ]


def obtener_historial_conversacion(db: Session, conversacion_id: int) -> list[dict]:
    mensajes = (
        db.query(HistorialConversacion)
        .filter(HistorialConversacion.ConversacionId == conversacion_id)
        .order_by(HistorialConversacion.Fecha.asc())
        .all()
    )
    return [
        {"role": m.Role, "content": m.Contenido}
        for m in mensajes
    ]


def guardar_mensaje(db: Session, usuario_id: int, conversacion_id: int, role: str, contenido: str):
    mensaje = HistorialConversacion(
        UsuarioId=usuario_id,
        ConversacionId=conversacion_id,
        Role=role,
        Contenido=contenido
    )
    db.add(mensaje)
    db.commit()


def actualizar_titulo(db: Session, conversacion_id: int, titulo: str):
    conv = db.query(Conversacion).filter(Conversacion.Id == conversacion_id).first()
    if conv:
        conv.Titulo = titulo
        db.commit()


def eliminar_conversacion(db: Session, conversacion_id: int):
    db.query(HistorialConversacion).filter(
        HistorialConversacion.ConversacionId == conversacion_id
    ).delete()
    db.query(Conversacion).filter(Conversacion.Id == conversacion_id).delete()
    db.commit()
