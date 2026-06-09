import os
import requests
from sqlalchemy.orm import Session
from app.database.models import NutricionPlatillo, PlatilloIngrediente, Ingrediente

USDA_API_KEY = os.getenv("USDA_API_KEY", "")
USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


def buscar_nutriente(nutrientes, nombre):
    for n in nutrientes:
        if n.get("nutrientName", "").lower() == nombre.lower():
            return round(n.get("value", 0), 1)
    return 0


def obtener_nutricion_ingrediente(nombre_ingrediente):
    try:
        response = requests.get(USDA_URL, params={
            "api_key": USDA_API_KEY,
            "query": nombre_ingrediente,
            "pageSize": 1
        })
        data = response.json()
        if data.get("foods"):
            food = data["foods"][0]
            nutrientes = food.get("foodNutrients", [])
            return {
                "calorias": buscar_nutriente(nutrientes, "Energy"),
                "proteina": buscar_nutriente(nutrientes, "Protein"),
                "carbohidratos": buscar_nutriente(nutrientes, "Carbohydrate, by difference"),
                "grasas": buscar_nutriente(nutrientes, "Total lipid (fat)"),
                "fibra": buscar_nutriente(nutrientes, "Fiber, total dietary"),
                "sodio": buscar_nutriente(nutrientes, "Sodium, Na"),
                "azucares": buscar_nutriente(nutrientes, "Sugars, total including NLEA"),
            }
    except:
        pass
    return None


def clasificar_platillo(calorias, proteina, grasas):
    if calorias < 300 and grasas < 15:
        return "Ligero y saludable"
    elif proteina > 25:
        return "Alto en proteína"
    elif calorias > 600:
        return "Platillo abundante"
    elif grasas > 30:
        return "Alto en grasas"
    else:
        return "Platillo balanceado"


def calcular_nutricion_platillo(db: Session, platillo_id: int):
    existente = db.query(NutricionPlatillo).filter(NutricionPlatillo.PlatilloId == platillo_id).first()
    if existente:
        return existente

    ingredientes = db.query(PlatilloIngrediente, Ingrediente).join(
        Ingrediente, PlatilloIngrediente.IngredienteId == Ingrediente.Id
    ).filter(PlatilloIngrediente.PlatilloId == platillo_id).all()

    if not ingredientes:
        return None

    totales = {"calorias": 0, "proteina": 0, "carbohidratos": 0, "grasas": 0, "fibra": 0, "sodio": 0, "azucares": 0}

    for pi, ing in ingredientes:
        datos = obtener_nutricion_ingrediente(ing.Nombre)
        if datos:
            for key in totales:
                totales[key] += datos[key]

    clasificacion = clasificar_platillo(totales["calorias"], totales["proteina"], totales["grasas"])

    nuevo = NutricionPlatillo(
        PlatilloId=platillo_id,
        Calorias=totales["calorias"],
        Proteina=totales["proteina"],
        Carbohidratos=totales["carbohidratos"],
        Grasas=totales["grasas"],
        Fibra=totales["fibra"],
        Sodio=totales["sodio"],
        Azucares=totales["azucares"],
        Clasificacion=clasificacion,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo