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

intentos_login = {}

def verificar_intentos_login(email: str, max_intentos: int = 5, bloqueo_minutos: int = 15):
    ahora = datetime.now()
    clave = email.lower()
    
    if clave not in intentos_login:
        intentos_login[clave] = {"intentos": 0, "bloqueado_hasta": None}
    
    registro = intentos_login[clave]
    
    if registro["bloqueado_hasta"] and ahora < registro["bloqueado_hasta"]:
        return False
    
    if registro["bloqueado_hasta"] and ahora >= registro["bloqueado_hasta"]:
        intentos_login[clave] = {"intentos": 0, "bloqueado_hasta": None}
    
    return True

def registrar_intento_fallido(email: str, max_intentos: int = 5, bloqueo_minutos: int = 15):
    ahora = datetime.now()
    clave = email.lower()
    
    if clave not in intentos_login:
        intentos_login[clave] = {"intentos": 0, "bloqueado_hasta": None}
    
    intentos_login[clave]["intentos"] += 1
    
    if intentos_login[clave]["intentos"] >= max_intentos:
        intentos_login[clave]["bloqueado_hasta"] = ahora + timedelta(minutes=bloqueo_minutos)

def limpiar_intentos(email: str):
    clave = email.lower()
    if clave in intentos_login:
        intentos_login[clave] = {"intentos": 0, "bloqueado_hasta": None}