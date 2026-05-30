from pydantic import BaseModel


class Mensaje(BaseModel):
    role: str
    content: str


class Pregunta(BaseModel):
    texto: str
    conversacion_id: int | None = None
    historial: list[Mensaje] = []


class Respuesta(BaseModel):
    respuesta: str
    conversacion_id: int


class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str


class UsuarioLogin(BaseModel):
    email: str
    password: str


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResponse