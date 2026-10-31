"""
Módulo: historial.py
Descripción: Administra el guardado y consulta del historial de limpiezas en formato JSON.
Nivel: 3.º Año - Escuela Técnica en Programación

Este módulo utiliza:
- 'json': para guardar y leer listas de diccionarios en un archivo de texto estructurado.
- 'datetime': para obtener la fecha y la hora actual en la que se ejecutó la limpieza.
- 'os': para verificar si el archivo y la carpeta 'datos/' existen.
"""

import os
import sys
import json
from datetime import datetime
from utilidades import formatear_tamano


def _obtener_ruta_historial():
    """
    Determina la ruta permanente del archivo 'historial.json'.
    
    Explicación para 3.º año:
    Si estamos ejecutando el programa desde el código fuente (.py), guardamos en la carpeta local 'datos/'.
    Si estamos ejecutando el archivo compilado (.exe), sys.frozen es True y sys.executable apunta
    al archivo .exe. Así guardamos 'datos/historial.json' al lado del .exe de forma permanente.
    """
    if getattr(sys, 'frozen', False):
        carpeta_base = os.path.dirname(sys.executable)
    else:
        carpeta_base = os.path.dirname(os.path.abspath(__file__))
        
    carpeta_datos = os.path.join(carpeta_base, "datos")
    ruta_json = os.path.join(carpeta_datos, "historial.json")
    return carpeta_datos, ruta_json


def _asegurar_archivo_historial():
    """
    Función interna que crea la carpeta 'datos' y el archivo 'historial.json' si aún no existen.
    
    Explicación para 3.º año:
    El guión bajo inicial (_) indica por convención que es una función auxiliar privada,
    pensada para usarse dentro de este mismo archivo.
    """
    carpeta_datos, ruta_json = _obtener_ruta_historial()
    if not os.path.exists(carpeta_datos):
        os.makedirs(carpeta_datos, exist_ok=True)
        
    if not os.path.exists(ruta_json):
        with open(ruta_json, "w", encoding="utf-8") as archivo:
            # Escribimos una lista vacía en formato JSON
            json.dump([], archivo, indent=4)


def cargar_historial():
    """
    Lee y devuelve todos los registros guardados en 'datos/historial.json'.
    
    Retorna:
        list: Lista de diccionarios, donde cada diccionario representa una limpieza anterior.
    """
    _asegurar_archivo_historial()
    _, ruta_json = _obtener_ruta_historial()
    
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            if isinstance(datos, list):
                return datos
            return []
    except (json.JSONDecodeError, OSError) as error:
        print(f"Aviso: No se pudo leer el historial, creando uno nuevo ({error})")
        return []


def guardar_registro(archivos_eliminados, bytes_liberados, categorias_limpiadas):
    """
    Añade un nuevo registro de limpieza al archivo de historial.
    
    Parámetros:
        archivos_eliminados (int): Cantidad de archivos borrados.
        bytes_liberados (int): Espacio recuperado en bytes.
        categorias_limpiadas (list): Nombres de las categorías que se limpiaron.
        
    Retorna:
        bool: True si se guardó con éxito, False si ocurrió un fallo.
    """
    _asegurar_archivo_historial()
    _, ruta_json = _obtener_ruta_historial()
    
    # 1. Obtenemos la fecha y hora actual en formato 'AAAA-MM-DD HH:MM:SS'
    momento_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Creamos el diccionario con los datos del nuevo evento de limpieza
    nuevo_registro = {
        "fecha": momento_actual,
        "archivos_eliminados": int(archivos_eliminados),
        "bytes_liberados": int(bytes_liberados),
        "espacio_formateado": formatear_tamano(bytes_liberados),
        "categorias": categorias_limpiadas
    }
    
    # 3. Cargamos los registros anteriores y agregamos el nuevo al principio
    registros = cargar_historial()
    registros.insert(0, nuevo_registro)  # Insertamos al inicio para ver los más recientes primero
    
    # 4. Guardamos la lista actualizada en el archivo JSON
    try:
        with open(ruta_json, "w", encoding="utf-8") as archivo:
            json.dump(registros, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        print(f"Error al guardar el registro en el historial: {error}")
        return False


def vaciar_historial():
    """
    Elimina todos los registros del historial, dejando la lista vacía.
    
    Retorna:
        bool: True si se vació correctamente.
    """
    _asegurar_archivo_historial()
    _, ruta_json = _obtener_ruta_historial()
    try:
        with open(ruta_json, "w", encoding="utf-8") as archivo:
            json.dump([], archivo, indent=4)
        return True
    except OSError as error:
        print(f"Error al vaciar el historial: {error}")
        return False
