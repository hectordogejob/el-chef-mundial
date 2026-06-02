from sqlalchemy.orm import Session
from datetime import date, datetime
from app.database.models import PerfilGamer, Nivel, Logro, UsuarioLogro, Favorito


def crear_perfil(db: Session, usuario_id: int):
    existente = db.query(PerfilGamer).filter(PerfilGamer.UsuarioId == usuario_id).first()
    if existente:
        return existente
    perfil = PerfilGamer(UsuarioId=usuario_id, NivelId=1, XP=0, Racha=0, MejorRacha=0, PlatillosCocinados=0, PreguntasAlChef=0)
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil


def obtener_perfil(db: Session, usuario_id: int) -> dict:
    perfil = db.query(PerfilGamer).filter(PerfilGamer.UsuarioId == usuario_id).first()
    if not perfil:
        perfil = crear_perfil(db, usuario_id)

    nivel = db.query(Nivel).filter(Nivel.Id == perfil.NivelId).first()
    siguiente_nivel = db.query(Nivel).filter(Nivel.Id == perfil.NivelId + 1).first()

    logros = db.query(UsuarioLogro).filter(UsuarioLogro.UsuarioId == usuario_id).all()
    total_logros = db.query(Logro).count()

    return {
        "xp": perfil.XP,
        "nivel": nivel.Nombre,
        "nivel_icono": nivel.Icono,
        "xp_minimo": nivel.XPMinimo,
        "xp_maximo": nivel.XPMaximo,
        "xp_siguiente": siguiente_nivel.XPMinimo if siguiente_nivel else None,
        "racha": perfil.Racha,
        "mejor_racha": perfil.MejorRacha,
        "platillos_cocinados": perfil.PlatillosCocinados,
        "preguntas_al_chef": perfil.PreguntasAlChef,
        "logros_desbloqueados": len(logros),
        "logros_totales": total_logros,
    }


def sumar_xp(db: Session, usuario_id: int, cantidad: int):
    perfil = db.query(PerfilGamer).filter(PerfilGamer.UsuarioId == usuario_id).first()
    if not perfil:
        perfil = crear_perfil(db, usuario_id)

    perfil.XP += cantidad
    actualizar_nivel(db, perfil)
    actualizar_racha(db, perfil)
    db.commit()
    return perfil.XP


def registrar_pregunta(db: Session, usuario_id: int):
    perfil = db.query(PerfilGamer).filter(PerfilGamer.UsuarioId == usuario_id).first()
    if not perfil:
        perfil = crear_perfil(db, usuario_id)

    perfil.PreguntasAlChef += 1
    sumar_xp(db, usuario_id, 5)
    verificar_logros(db, usuario_id)


def registrar_platillo_cocinado(db: Session, usuario_id: int):
    perfil = db.query(PerfilGamer).filter(PerfilGamer.UsuarioId == usuario_id).first()
    if not perfil:
        perfil = crear_perfil(db, usuario_id)

    perfil.PlatillosCocinados += 1
    sumar_xp(db, usuario_id, 25)
    verificar_logros(db, usuario_id)


def actualizar_nivel(db: Session, perfil: PerfilGamer):
    niveles = db.query(Nivel).order_by(Nivel.XPMinimo.desc()).all()
    for nivel in niveles:
        if perfil.XP >= nivel.XPMinimo:
            if perfil.NivelId != nivel.Id:
                perfil.NivelId = nivel.Id
            break


def actualizar_racha(db: Session, perfil: PerfilGamer):
    hoy = date.today()
    if perfil.UltimaActividad:
        ultima = perfil.UltimaActividad.date() if isinstance(perfil.UltimaActividad, datetime) else perfil.UltimaActividad
        dias = (hoy - ultima).days
        if dias == 1:
            perfil.Racha += 1
        elif dias > 1:
            perfil.Racha = 1
    else:
        perfil.Racha = 1

    if perfil.Racha > perfil.MejorRacha:
        perfil.MejorRacha = perfil.Racha

    perfil.UltimaActividad = datetime.now()


def verificar_logros(db: Session, usuario_id: int):
    perfil = db.query(PerfilGamer).filter(PerfilGamer.UsuarioId == usuario_id).first()
    if not perfil:
        return

    logros = db.query(Logro).all()
    desbloqueados = [ul.LogroId for ul in db.query(UsuarioLogro).filter(UsuarioLogro.UsuarioId == usuario_id).all()]

    for logro in logros:
        if logro.Id in desbloqueados:
            continue

        desbloqueado = False

        if logro.Condicion == "platillos_cocinados" and perfil.PlatillosCocinados >= logro.Valor:
            desbloqueado = True
        elif logro.Condicion == "preguntas" and perfil.PreguntasAlChef >= logro.Valor:
            desbloqueado = True
        elif logro.Condicion == "racha" and perfil.Racha >= logro.Valor:
            desbloqueado = True
        elif logro.Condicion == "nivel" and perfil.NivelId >= logro.Valor:
            desbloqueado = True
        elif logro.Condicion == "favoritos":
            total_favs = db.query(Favorito).filter(Favorito.UsuarioId == usuario_id).count()
            if total_favs >= logro.Valor:
                desbloqueado = True

        if desbloqueado:
            nuevo = UsuarioLogro(UsuarioId=usuario_id, LogroId=logro.Id)
            db.add(nuevo)

    db.commit()


def obtener_logros(db: Session, usuario_id: int) -> list[dict]:
    todos = db.query(Logro).all()
    desbloqueados = {ul.LogroId: ul.FechaObtenido for ul in db.query(UsuarioLogro).filter(UsuarioLogro.UsuarioId == usuario_id).all()}

    return [
        {
            "id": l.Id,
            "nombre": l.Nombre,
            "descripcion": l.Descripcion,
            "icono": l.Icono,
            "desbloqueado": l.Id in desbloqueados,
            "fecha": desbloqueados[l.Id].strftime("%d/%m/%Y") if l.Id in desbloqueados else None,
        }
        for l in todos
    ]
