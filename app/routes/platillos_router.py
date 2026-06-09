from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services import platillos_service
from app.database.models import Usuario
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(prefix="/platillos", tags=["Platillos"])


@router.get("/")
def listar_platillos(db: Session = Depends(get_db)):
    return platillos_service.listar_todos(db)


@router.get("/continente/{continente}")
def platillos_por_continente(continente: str, db: Session = Depends(get_db)):
    resultados = platillos_service.listar_por_continente(db, continente)
    if resultados:
        return resultados
    return {"mensaje": "No se encontraron platillos de ese continente"}


@router.get("/buscar/{palabra}")
def buscar_platillo(palabra: str, db: Session = Depends(get_db)):
    resultados = platillos_service.buscar_por_nombre(db, palabra)
    if resultados:
        return resultados
    return {"mensaje": "No se encontraron platillos con ese nombre"}


@router.get("/{platillo_id}")
def obtener_platillo(platillo_id: int, db: Session = Depends(get_db)):
    platillo = platillos_service.obtener_por_id(db, platillo_id)
    if platillo:
        return platillo
    return {"error": "Platillo no encontrado"}


@router.get("/{platillo_id}/ingredientes")
def obtener_ingredientes(platillo_id: int, db: Session = Depends(get_db)):
    platillo = platillos_service.obtener_por_id(db, platillo_id)
    if not platillo:
        return {"error": "Platillo no encontrado"}
    if not platillo.get("ingredientes") or len(platillo["ingredientes"]) == 0:
        return {
            "platillo": platillo["nombre"],
            "tiene_ingredientes": False,
            "mensaje": "Este platillo no tiene ingredientes detallados. Pidele la receta al Chef Vittorio."
        }
    return {
        "platillo": platillo["nombre"],
        "porciones": platillo["porciones"],
        "tiene_ingredientes": True,
        "ingredientes": platillo["ingredientes"]
    }

@router.get("/{platillo_id}/nutricion")
def obtener_nutricion(
    platillo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    from app.services.nutricion_service import calcular_nutricion_platillo
    resultado = calcular_nutricion_platillo(db, platillo_id)
    if not resultado:
        return {"error": "No se pudo calcular la nutrición para este platillo"}
    return {
        "calorias": resultado.Calorias,
        "proteina": resultado.Proteina,
        "carbohidratos": resultado.Carbohidratos,
        "grasas": resultado.Grasas,
        "fibra": resultado.Fibra,
        "sodio": resultado.Sodio,
        "azucares": resultado.Azucares,
        "clasificacion": resultado.Clasificacion
    }