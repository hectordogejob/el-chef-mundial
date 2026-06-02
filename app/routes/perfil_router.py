from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Usuario
from app.services import gamificacion_service
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(prefix="/perfil", tags=["Perfil Gamer"])


@router.get("/")
def mi_perfil(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return gamificacion_service.obtener_perfil(db, usuario.Id)


@router.get("/logros")
def mis_logros(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return gamificacion_service.obtener_logros(db, usuario.Id)
