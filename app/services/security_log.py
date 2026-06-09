from datetime import datetime

def log_seguridad(evento: str, detalle: str, usuario_id: int = None):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ahora}] {evento} | Usuario: {usuario_id} | {detalle}\n"
    with open("seguridad.log", "a", encoding="utf-8") as f:
        f.write(linea)