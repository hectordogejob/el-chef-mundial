from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import platillos_router, chef_router, auth_router, favoritos_router, conversaciones_router

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

app.include_router(auth_router.router)
app.include_router(platillos_router.router)
app.include_router(chef_router.router)
app.include_router(favoritos_router.router)
app.include_router(conversaciones_router.router)


@app.get("/", tags=["Health"])
def inicio():
    return {
        "mensaje": "El Chef Mundial API funcionando",
        "chef": "Chef Vittorio",
        "version": settings.APP_VERSION
    }