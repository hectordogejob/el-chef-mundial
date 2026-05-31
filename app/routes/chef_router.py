from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, Date
from datetime import datetime, date
from app.models.schemas import Pregunta
from app.database.connection import get_db
from app.database.models import Usuario, ContadorDiario
from app.services import ia_service, conversaciones_service
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(prefix="/chef", tags=["Chef Vittorio"])


def obtener_contador(db: Session, usuario_id: int):
    hoy = date.today()
    contador = db.query(ContadorDiario).filter(
        ContadorDiario.UsuarioId == usuario_id,
        func.cast(ContadorDiario.Fecha, Date) == hoy
    ).first()
    if not contador:
        contador = ContadorDiario(UsuarioId=usuario_id, Fecha=datetime.now(), PreguntasRealizadas=0)
        db.add(contador)
        db.commit()
        db.refresh(contador)
    return contador


@router.post("/preguntar")
def preguntar_al_chef(
    pregunta: Pregunta,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    if not usuario.EsPremium:
        contador = obtener_contador(db, usuario.Id)
        preguntas_hoy = contador.PreguntasRealizadas
        limite = usuario.LimiteDiario or 3

        if preguntas_hoy >= limite:
            return {
                "respuesta": None,
                "conversacion_id": pregunta.conversacion_id,
                "limite_alcanzado": True,
                "preguntas_hoy": preguntas_hoy,
                "limite": limite,
                "mensaje": f"Has alcanzado tu limite de {limite} preguntas diarias. Hazte Premium para preguntas ilimitadas."
            }

    conv_id = pregunta.conversacion_id

    if not conv_id:
        titulo = pregunta.texto[:50] + "..." if len(pregunta.texto) > 50 else pregunta.texto
        conv = conversaciones_service.crear_conversacion(db, usuario.Id, titulo)
        conv_id = conv["id"]

    historial = conversaciones_service.obtener_historial_conversacion(db, conv_id)
    respuesta = ia_service.obtener_respuesta_chef(db, pregunta.texto, historial)

    conversaciones_service.guardar_mensaje(db, usuario.Id, conv_id, "user", pregunta.texto)
    conversaciones_service.guardar_mensaje(db, usuario.Id, conv_id, "assistant", respuesta)

    if not usuario.EsPremium:
        contador = obtener_contador(db, usuario.Id)
        contador.PreguntasRealizadas += 1
        db.commit()
        preguntas_hoy = contador.PreguntasRealizadas
        limite = usuario.LimiteDiario or 3
    else:
        preguntas_hoy = 0
        limite = 0

    return {
        "respuesta": respuesta,
        "conversacion_id": conv_id,
        "limite_alcanzado": False,
        "preguntas_restantes": max(0, limite - preguntas_hoy) if not usuario.EsPremium else -1,
        "es_premium": usuario.EsPremium
    }


@router.get("/preguntas-restantes")
def preguntas_restantes(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    if usuario.EsPremium:
        return {"es_premium": True, "restantes": -1, "limite": -1}

    contador = obtener_contador(db, usuario.Id)
    preguntas_hoy = contador.PreguntasRealizadas
    limite = usuario.LimiteDiario or 3

    return {
        "es_premium": False,
        "restantes": max(0, limite - preguntas_hoy),
        "limite": limite,
        "usadas": preguntas_hoy
    }