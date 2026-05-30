from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Usuario
from app.services import conversaciones_service
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(prefix="/conversaciones", tags=["Conversaciones"])


@router.get("/")
def mis_conversaciones(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return conversaciones_service.listar_conversaciones(db, usuario.Id)


@router.post("/nueva")
def nueva_conversacion(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return conversaciones_service.crear_conversacion(db, usuario.Id)


@router.get("/{conversacion_id}/historial")
def historial_conversacion(
    conversacion_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return conversaciones_service.obtener_historial_conversacion(db, conversacion_id)


@router.delete("/{conversacion_id}")
def eliminar(
    conversacion_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    conversaciones_service.eliminar_conversacion(db, conversacion_id)
    return {"mensaje": "Conversación eliminada"}
