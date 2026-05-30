from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Usuario
from app.services import favoritos_service
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(prefix="/favoritos", tags=["Favoritos"])


@router.get("/")
def mis_favoritos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return favoritos_service.obtener_favoritos(db, usuario.Id)


@router.get("/ids")
def mis_favoritos_ids(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return favoritos_service.obtener_ids_favoritos(db, usuario.Id)


@router.post("/{platillo_id}")
def agregar(
    platillo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return favoritos_service.agregar_favorito(db, usuario.Id, platillo_id)


@router.delete("/{platillo_id}")
def quitar(
    platillo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return favoritos_service.quitar_favorito(db, usuario.Id, platillo_id)
