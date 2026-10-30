# ==============================================================================
# MÓDULO: historial.py - Registro Persistente de Partidas en CSV
# ==============================================================================
# Este módulo se encarga de guardar y leer los resultados históricos de las partidas.
# Utiliza el módulo estándar 'csv' de Python para almacenar los datos en 'historial.csv'.
#
# Cada fila representa una partida terminada con:
# - fecha_hora: momento exacto de finalización.
# - tiempo_segundos: duración de la partida.
# - puntuacion: puntos conseguidos.
# - personaje: nombre del personaje utilizado ("Alex" o "Sara").
# ==============================================================================

import os
import sys
import csv
from datetime import datetime

# Nombre del archivo donde se guardan las partidas
NOMBRE_ARCHIVO_CSV = "historial.csv"


def obtener_carpeta_datos():
    """
    Determina la carpeta segura donde se almacenará el archivo CSV y las estadísticas.
    Funciona tanto al ejecutar el código en Python (.py) como al compilarlo en .exe.
    Si no tiene permisos de escritura en la carpeta del juego, usa LocalAppData.
    """
    if getattr(sys, "frozen", False):
        # Si se ejecuta como .exe generado por PyInstaller
        directorio_base = os.path.dirname(sys.executable)
    else:
        # Si se ejecuta como script normal de Python
        directorio_base = os.path.dirname(os.path.abspath(__file__))

    carpeta = os.path.join(directorio_base, "datos")

    # Intentamos crear la carpeta si no existe
    try:
        os.makedirs(carpeta, exist_ok=True)
        # Probamos escribir un archivo temporal para verificar permisos
        archivo_prueba = os.path.join(carpeta, ".permiso_test")
        with open(archivo_prueba, "w") as f:
            f.write("ok")
        os.remove(archivo_prueba)
    except (PermissionError, OSError):
        # Si Windows bloquea la escritura (por ejemplo en C:\Program Files), usamos LocalAppData
        carpeta_usuario = os.getenv("LOCALAPPDATA", os.path.expanduser("~"))
        carpeta = os.path.join(carpeta_usuario, "RetroTrack", "datos")
        os.makedirs(carpeta, exist_ok=True)

    return carpeta


def obtener_ruta_csv():
    """Devuelve la ruta completa hacia el archivo historial.csv."""
    return os.path.join(obtener_carpeta_datos(), NOMBRE_ARCHIVO_CSV)


def guardar_partida(tiempo_segundos, puntuacion, nombre_personaje="Alex"):
    """
    Guarda los resultados de una partida en 'historial.csv'.
    - Si el archivo no existe, lo crea y escribe los encabezados de columna.
    - Si ya existe, añade el nuevo registro al final (modo 'a') sin borrar lo anterior.
    
    Retorna True si se guardó correctamente, o False si ocurrió algún error.
    """
    try:
        ruta_archivo = obtener_ruta_csv()
        
        # Redondear y formatear valores
        tiempo_limpio = round(float(tiempo_segundos), 2)
        puntuacion_limpia = int(puntuacion)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        personaje_limpio = str(nombre_personaje).strip()

        # Comprobar si el archivo ya existe y tiene contenido
        existe_archivo = os.path.exists(ruta_archivo) and os.path.getsize(ruta_archivo) > 0

        # Abrimos el archivo en modo "a" (append = agregar al final)
        with open(ruta_archivo, mode="a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            
            # Si el archivo es nuevo, escribimos la fila de títulos de columna
            if not existe_archivo:
                escritor.writerow(["fecha_hora", "tiempo_segundos", "puntuacion", "personaje"])
            
            # Escribir la nueva partida
            escritor.writerow([fecha_actual, tiempo_limpio, puntuacion_limpia, personaje_limpio])

        print(f"[Historial] Partida registrada: {fecha_actual} | {tiempo_limpio}s | {puntuacion_limpia} pts | {personaje_limpio}")
        return True

    except Exception as error:
        print(f"[Historial] Error al guardar en CSV: {error}")
        return False


def leer_partidas():
    """
    Lee todas las partidas almacenadas en 'historial.csv'.
    Retorna una lista de diccionarios, donde cada diccionario representa una partida.
    Si el archivo no existe o está vacío, retorna una lista vacía [].
    """
    ruta_archivo = obtener_ruta_csv()
    
    if not os.path.exists(ruta_archivo):
        return []

    partidas = []
    try:
        with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    partida = {
                        "fecha_hora": fila.get("fecha_hora", ""),
                        "tiempo_segundos": float(fila.get("tiempo_segundos", 0.0)),
                        "puntuacion": int(fila.get("puntuacion", 0)),
                        "personaje": fila.get("personaje", "Alex")
                    }
                    partidas.append(partida)
                except (ValueError, TypeError):
                    # Si alguna fila tiene un dato dañado, la ignoramos de forma segura
                    continue
        return partidas

    except Exception as error:
        print(f"[Historial] Error al leer el archivo CSV: {error}")
        return []


def obtener_mejor_puntuacion():
    """
    Calcula y retorna la puntuación más alta registrada en el historial.
    Si todavía no hay partidas, retorna 0.
    """
    partidas = leer_partidas()
    if not partidas:
        return 0
    
    mejor = 0
    for p in partidas:
        if p["puntuacion"] > mejor:
            mejor = p["puntuacion"]
    return mejor


def obtener_total_partidas():
    """Retorna la cantidad total de partidas registradas hasta el momento."""
    partidas = leer_partidas()
    return len(partidas)


# Bloque de prueba individual si se ejecuta directamente este archivo
if __name__ == "__main__":
    print("Probando módulo historial.py...")
    print(f"Ruta del archivo CSV: {obtener_ruta_csv()}")
    print(f"Total de partidas guardadas: {obtener_total_partidas()}")
    print(f"Mejor puntuación histórica: {obtener_mejor_puntuacion()} pts")
