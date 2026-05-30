from sqlalchemy.orm import Session
from app.database.models import Platillo, Cocina, Pais, Continente


def listar_todos(db: Session) -> list[dict]:
    platillos = db.query(Platillo).filter(Platillo.Activo == True).all()
    return [
        {
            "id": p.Id,
            "nombre": p.Nombre,
            "cocina": p.cocina.Nombre,
            "pais": p.cocina.pais.Nombre,
            "continente": p.cocina.pais.continente.Nombre,
            "nivel": p.nivel.Nombre,
            "imagen": p.Imagen,
            "descripcion": p.Descripcion
        }
        for p in platillos
    ]


def obtener_por_id(db: Session, platillo_id: int) -> dict | None:
    platillo = db.query(Platillo).filter(Platillo.Id == platillo_id).first()
    if not platillo:
        return None
    return _platillo_completo(platillo)


def buscar_por_nombre(db: Session, palabra: str) -> list[dict]:
    platillos = db.query(Platillo).filter(
        Platillo.Activo == True,
        Platillo.Nombre.ilike(f"%{palabra}%")
    ).all()
    return [
        {
            "id": p.Id,
            "nombre": p.Nombre,
            "cocina": p.cocina.Nombre,
            "nivel": p.nivel.Nombre,
           "imagen": p.Imagen
        }
        for p in platillos
    ]


def listar_por_continente(db: Session, continente: str) -> list[dict]:
    platillos = (
        db.query(Platillo)
        .join(Cocina).join(Pais).join(Continente)
        .filter(Continente.Nombre.ilike(f"%{continente}%"), Platillo.Activo == True)
        .all()
    )
    return [
        {
            "id": p.Id,
            "nombre": p.Nombre,
            "cocina": p.cocina.Nombre,
            "pais": p.cocina.pais.Nombre,
            "nivel": p.nivel.Nombre,
            "imagen": p.Imagen
        }
        for p in platillos
    ]


def obtener_todos_para_ia(db: Session) -> dict:
    platillos = db.query(Platillo).filter(Platillo.Activo == True).all()
    resultado = {}
    for p in platillos:
        resultado[p.Nombre] = _platillo_completo(p)
    return resultado


def _platillo_completo(p: Platillo) -> dict:
    return {
        "nombre": p.Nombre,
        "descripcion": p.Descripcion,
        "cocina": p.cocina.Nombre,
        "pais": p.cocina.pais.Nombre,
        "continente": p.cocina.pais.continente.Nombre,
        "categoria": p.categoria.Nombre,
        "nivel": p.nivel.Nombre,
        "tiempo_preparacion": p.TiempoPreparacion,
        "porciones": p.Porciones,
        "historia": p.Historia,
        "tip_chef_vittorio": p.TipChefVittorio,
        "imagen": p.Imagen,
        "ingredientes": [
            {
                "nombre": pi.ingrediente.Nombre,
                "cantidad": pi.Cantidad,
                "notas": pi.Notas
            }
            for pi in p.ingredientes
        ],
        "utensilios": [
            {
                "nombre": pu.utensilio.Nombre,
                "obligatorio": pu.Obligatorio
            }
            for pu in p.utensilios
        ],
        "tecnicas": [
            pt.tecnica.Nombre for pt in p.tecnicas
        ],
        "pasos": [
            {
                "num": paso.NumPaso,
                "instruccion": paso.Instruccion,
                "tip_chef": paso.TipChef,
                "tiempo_minutos": paso.TiempoMinutos
            }
            for paso in sorted(p.pasos, key=lambda x: x.NumPaso)
        ]
    }
