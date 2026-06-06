from datetime import datetime, timedelta

solicitudes = {}

def verificar_limite(usuario_id: int, limite: int = 20, ventana_segundos: int = 60):
    ahora = datetime.now()
    clave = str(usuario_id)
    
    if clave not in solicitudes:
        solicitudes[clave] = []
    
    solicitudes[clave] = [t for t in solicitudes[clave] if ahora - t < timedelta(seconds=ventana_segundos)]
    
    if len(solicitudes[clave]) >= limite:
        return False
    
    solicitudes[clave].append(ahora)
    return True