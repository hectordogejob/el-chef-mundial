from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.routes import platillos_router, chef_router, auth_router, favoritos_router, conversaciones_router, perfil_router

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_router.router)
app.include_router(platillos_router.router)
app.include_router(chef_router.router)
app.include_router(favoritos_router.router)
app.include_router(conversaciones_router.router)
app.include_router(perfil_router.router)


@app.get("/", tags=["Health"])
def inicio():
    return {
        "mensaje": "El Chef Mundial API funcionando",
        "chef": "Chef Vittorio",
        "version": settings.APP_VERSION
    }