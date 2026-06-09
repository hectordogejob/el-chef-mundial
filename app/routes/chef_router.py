from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, Date
from datetime import datetime, date
from app.models.schemas import Pregunta
from app.database.connection import get_db
from app.database.models import Usuario, ContadorDiario
from app.services import ia_service, conversaciones_service
from app.services.auth_service import obtener_usuario_actual
from app.services.rate_limiter import verificar_limite
from app.services.security_log import log_seguridad

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

def buscar_en_bd(db: Session, texto: str):
    from app.database.models import Platillo, PlatilloIngrediente, Ingrediente, PasoPlatillo
    texto_lower = texto.lower()
    
    platillos = db.query(Platillo).all()
    encontrado = None
    for p in platillos:
        if p.Nombre and p.Nombre.lower() in texto_lower:
            encontrado = p
            break
    
    if not encontrado:
        return None
    
    ingredientes = db.query(PlatilloIngrediente, Ingrediente).join(
        Ingrediente, PlatilloIngrediente.IngredienteId == Ingrediente.Id
    ).filter(PlatilloIngrediente.PlatilloId == encontrado.Id).all()
    
    pasos = db.query(PasoPlatillo).filter(
        PasoPlatillo.PlatilloId == encontrado.Id
    ).order_by(PasoPlatillo.NumPaso).all()
    
    if not ingredientes and not pasos:
        return None
    
    respuesta = f"# {encontrado.Nombre} 🍽️\n\n"
    respuesta += f"**¡Perfetto!** Te voy a enseñar a preparar un auténtico **{encontrado.Nombre}**.\n\n"
    if encontrado.Descripcion:
        respuesta += f"*{encontrado.Descripcion}*\n\n"
    if encontrado.Historia:
        respuesta += f"📜 **Un poco de historia:** {encontrado.Historia}\n\n"
    if encontrado.TiempoPreparacion:
        respuesta += f"⏱️ **Tiempo:** {encontrado.TiempoPreparacion} | "
    if encontrado.Porciones:
        respuesta += f"🍽️ **Porciones:** {encontrado.Porciones}\n\n"
    if ingredientes:
        respuesta += "## 🥘 Lo que necesitas\n"
        for pi, ing in ingredientes:
            respuesta += f"- **{pi.Cantidad}** de {ing.Nombre}\n"
        respuesta += "\n"
    if pasos:
        respuesta += "## 👨‍🍳 Manos a la obra\n"
        for paso in pasos:
            respuesta += f"**Paso {paso.NumPaso}:** {paso.Instruccion}\n\n"
    if encontrado.TipChefVittorio:
        respuesta += f"\n💡 **Tip del Chef Vittorio:** *{encontrado.TipChefVittorio}*\n"
    respuesta += f"\n---\n*¿Tienes alguna duda sobre la preparación? ¡Pregúntame con confianza!* 🔥"
    
    return respuesta


def respuesta_preguardada(texto: str):
    preguntas = {
        "Tengo $200 pesos, qué puedo cocinar?": "# 💰 ¡Perfetto! $200 pesos son MÁS que suficientes\n\n¡Escúchame bien! Un buen chef no se mide por cuánto gasta, sino por lo que hace con lo que tiene. Con $200 pesos te voy a demostrar que puedes cocinar como un profesional:\n\n🥇 **Chilaquiles Rojos** (~$60 MXN) — Totopos en salsa roja hirviendo, crema, queso y cebolla. El desayuno mexicano PERFECTO.\n\n🥈 **Arroz Rojo + Frijoles Charros** (~$80 MXN) — Comida completa para toda la familia. Los frijoles con chorizo y tocino son una OBRA DE ARTE.\n\n🥉 **Enchiladas Verdes** (~$90 MXN) — Tortillas rellenas de pollo, bañadas en salsa verde con crema y queso. *Bellissimo.*\n\n⭐ **Quesadillas de Chicharrón** (~$50 MXN) — Street food legendario. Masa hecha a mano con chicharrón prensado en salsa verde.\n\n💡 **Consejo del Chef Vittorio:** *La cocina económica NO es cocina pobre, es cocina INTELIGENTE. Los mejores platillos del mundo nacieron de ingredientes humildes. ¡Manos a la obra!*\n\n¿Cuál te gustaría preparar? Te enseño paso a paso. 🔥",
    }
    return preguntas.get(texto, None)

@router.post("/preguntar")
def preguntar_al_chef(
    pregunta: Pregunta,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    if not verificar_limite(usuario.Id):
        log_seguridad("RATE_LIMIT", f"Excedio 20 peticiones/min", usuario.Id)
        return {
            "respuesta": "Has hecho demasiadas peticiones. Espera un momento antes de continuar.",
            "conversacion_id": pregunta.conversacion_id,
            "limite_alcanzado": True,
            "preguntas_hoy": 0,
            "limite": 0,
            "mensaje": "Demasiadas peticiones. Espera 1 minuto."
        }
    if len(pregunta.texto) > 1000:
        log_seguridad("MSG_LARGO", f"Mensaje de {len(pregunta.texto)} caracteres", usuario.Id)
        return {
            "respuesta": "Tu mensaje es muy largo. El límite es 1000 caracteres.",
            "conversacion_id": pregunta.conversacion_id,
            "limite_alcanzado": False,
            "preguntas_restantes": 0,
            "es_premium": usuario.EsPremium
        }
    pregunta.texto = pregunta.texto.replace("<", "").replace(">", "").replace("script", "").strip()
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

    if conv_id:
        from app.database.models import Conversacion
        conv_existente = db.query(Conversacion).filter(
            Conversacion.Id == conv_id,
            Conversacion.UsuarioId == usuario.Id
        ).first()
        if not conv_existente:
            log_seguridad("CONV_AJENA", f"Intento acceder a conversacion {conv_id}", usuario.Id)
            return {
                "respuesta": "Esta conversación no te pertenece.",
                "conversacion_id": None,
                "limite_alcanzado": False,
                "preguntas_restantes": 0,
                "es_premium": usuario.EsPremium
            }

    preguardada = respuesta_preguardada(pregunta.texto)
    if preguardada:
        respuesta = preguardada
    elif buscar_en_bd(db, pregunta.texto):
        respuesta = buscar_en_bd(db, pregunta.texto)
    else:
        historial = conversaciones_service.obtener_historial_conversacion(db, conv_id)
        respuesta = ia_service.obtener_respuesta_chef(db, pregunta.texto, historial)

    conversaciones_service.guardar_mensaje(db, usuario.Id, conv_id, "user", pregunta.texto)
    conversaciones_service.guardar_mensaje(db, usuario.Id, conv_id, "assistant", respuesta)

    from app.services import gamificacion_service
    gamificacion_service.registrar_pregunta(db, usuario.Id)

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