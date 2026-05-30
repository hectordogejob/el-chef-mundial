from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database.models import Favorito, Platillo


def agregar_favorito(db: Session, usuario_id: int, platillo_id: int):
    existente = db.query(Favorito).filter(
        Favorito.UsuarioId == usuario_id,
        Favorito.PlatilloId == platillo_id
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este platillo ya está en tus favoritos"
        )

    favorito = Favorito(UsuarioId=usuario_id, PlatilloId=platillo_id)
    db.add(favorito)
    db.commit()
    return {"mensaje": "Agregado a favoritos"}


def quitar_favorito(db: Session, usuario_id: int, platillo_id: int):
    favorito = db.query(Favorito).filter(
        Favorito.UsuarioId == usuario_id,
        Favorito.PlatilloId == platillo_id
    ).first()

    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Este platillo no está en tus favoritos"
        )

    db.delete(favorito)
    db.commit()
    return {"mensaje": "Eliminado de favoritos"}


def obtener_favoritos(db: Session, usuario_id: int) -> list[dict]:
    favoritos = (
        db.query(Favorito)
        .filter(Favorito.UsuarioId == usuario_id)
        .all()
    )
    return [
        {
            "id": f.platillo.Id,
            "nombre": f.platillo.Nombre,
            "cocina": f.platillo.cocina.Nombre,
            "pais": f.platillo.cocina.pais.Nombre,
            "continente": f.platillo.cocina.pais.continente.Nombre,
            "nivel": f.platillo.nivel.Nombre,
            "imagen": f.platillo.Imagen
        }
        for f in favoritos
    ]


def es_favorito(db: Session, usuario_id: int, platillo_id: int) -> bool:
    return db.query(Favorito).filter(
        Favorito.UsuarioId == usuario_id,
        Favorito.PlatilloId == platillo_id
    ).first() is not None


def obtener_ids_favoritos(db: Session, usuario_id: int) -> list[int]:
    favoritos = db.query(Favorito.PlatilloId).filter(
        Favorito.UsuarioId == usuario_id
    ).all()
    return [f[0] for f in favoritos]
