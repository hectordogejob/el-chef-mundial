from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.schemas import Pregunta, Respuesta
from app.database.connection import get_db
from app.database.models import Usuario
from app.services import ia_service, conversaciones_service
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(prefix="/chef", tags=["Chef Vittorio"])


@router.post("/preguntar")
def preguntar_al_chef(
    pregunta: Pregunta,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    conv_id = pregunta.conversacion_id

    # Si no hay conversacion, crear una nueva con las primeras palabras como titulo
    if not conv_id:
        titulo = pregunta.texto[:50] + "..." if len(pregunta.texto) > 50 else pregunta.texto
        conv = conversaciones_service.crear_conversacion(db, usuario.Id, titulo)
        conv_id = conv["id"]

    # Obtener historial de esta conversacion
    historial = conversaciones_service.obtener_historial_conversacion(db, conv_id)

    # Obtener respuesta de la IA
    respuesta = ia_service.obtener_respuesta_chef(db, pregunta.texto, historial)

    # Guardar pregunta y respuesta
    conversaciones_service.guardar_mensaje(db, usuario.Id, conv_id, "user", pregunta.texto)
    conversaciones_service.guardar_mensaje(db, usuario.Id, conv_id, "assistant", respuesta)

    return {"respuesta": respuesta, "conversacion_id": conv_id}