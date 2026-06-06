from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.schemas import UsuarioRegistro, UsuarioLogin, TokenResponse, UsuarioResponse
from app.services.auth_service import registrar_usuario, login_usuario, crear_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro", response_model=TokenResponse)
def registro(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    if len(datos.password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
    usuario = registrar_usuario(db, datos.nombre, datos.email, datos.password)
    token = crear_token(usuario.Id, usuario.Email)
    from app.services import gamificacion_service
    gamificacion_service.crear_perfil(db, usuario.Id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario=UsuarioResponse(
            id=usuario.Id,
            nombre=usuario.Nombre,
            email=usuario.Email
        )
    )


@router.post("/login", response_model=TokenResponse)
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = login_usuario(db, datos.email, datos.password)
    token = crear_token(usuario.Id, usuario.Email)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario=UsuarioResponse(
            id=usuario.Id,
            nombre=usuario.Nombre,
            email=usuario.Email
        )
    )
