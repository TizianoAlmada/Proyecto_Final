"""
Módulo: analizador.py
Descripción: Escanea y analiza el almacenamiento en busca de archivos temporales e innecesarios.
Nivel: 3.º Año - Escuela Técnica en Programación

Este módulo recorre de forma segura carpetas específicas del sistema y de los usuarios,
sumando la cantidad de archivos y los bytes que ocupan, sin modificar ni borrar nada.
"""

import os
import tempfile
import glob
from pathlib import Path
import ctypes
from ctypes import Structure, c_int64, byref, sizeof
from ctypes.wintypes import DWORD

from utilidades import formatear_tamano


# Estructura requerida por la API de Windows para consultar la Papelera de Reciclaje
class _SHQUERYRBINFO(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('i64Size', c_int64),
        ('i64NumItems', c_int64)
    ]


def consultar_papelera():
    """
    Consulta a Windows cuántos archivos hay en la Papelera de Reciclaje y cuánto espacio ocupan.
    
    Explicación para 3.º año:
    Windows protege la papelera de reciclaje y no es una carpeta ordinaria.
    Utilizamos la función oficial de Windows 'SHQueryRecycleBinW' a través de la librería
    'ctypes', lo cual nos permite saber su peso exacto sin tocar ni borrar ningún archivo.
    """
    try:
        info_papelera = _SHQUERYRBINFO()
        info_papelera.cbSize = sizeof(_SHQUERYRBINFO)
        resultado = ctypes.windll.shell32.SHQueryRecycleBinW(None, byref(info_papelera))
        
        if resultado == 0:  # 0 significa S_OK (éxito en la API de Windows)
            return {
                "archivos": int(info_papelera.i64NumItems),
                "bytes": int(info_papelera.i64Size)
            }
    except Exception as error:
        print(f"No se pudo consultar la papelera: {error}")
        
    return {"archivos": 0, "bytes": 0}


def obtener_rutas_por_categoria():
    """
    Define y devuelve un diccionario con las carpetas autorizadas para cada categoría.
    
    SEGURIDAD:
    Solo se definen carpetas destinadas a temporales y cachés.
    Bajo ninguna circunstancia se agregan carpetas personales ni del sistema vital.
    """
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    appdata = os.environ.get("APPDATA", "")
    system_root = os.environ.get("SystemRoot", "C:\\Windows")
    
    rutas_categorias = {
        "temp_usuario": {
            "nombre": "Archivos Temporales de Usuario",
            "descripcion": "Archivos temporales generados por programas en su cuenta personal.",
            "carpetas": [
                tempfile.gettempdir(),
                os.path.join(local_appdata, "Temp")
            ]
        },
        "temp_windows": {
            "nombre": "Archivos Temporales de Windows",
            "descripcion": "Instaladores residuales y archivos temporales del sistema operativo.",
            "carpetas": [
                os.path.join(system_root, "Temp"),
                os.path.join(system_root, "SoftwareDistribution", "Download")
            ]
        },
        "cache_navegadores": {
            "nombre": "Caché de Navegadores Web",
            "descripcion": "Archivos temporales de páginas web visitadas (Chrome, Edge, Firefox).",
            "carpetas": [
                os.path.join(local_appdata, r"Google\Chrome\User Data\Default\Cache"),
                os.path.join(local_appdata, r"Google\Chrome\User Data\Default\Code Cache"),
                os.path.join(local_appdata, r"Google\Chrome\User Data\Default\GPUCache"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\Default\Cache"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\Default\Code Cache"),
                os.path.join(local_appdata, r"Microsoft\Edge\User Data\Default\GPUCache"),
                os.path.join(local_appdata, r"BraveSoftware\Brave-Browser\User Data\Default\Cache"),
            ]
        },
        "reportes_logs": {
            "nombre": "Reportes de Error y Logs Temporales",
            "descripcion": "Volcados de memoria de cuelgues (Crash Dumps) y registros temporales.",
            "carpetas": [
                os.path.join(local_appdata, "CrashDumps"),
                os.path.join(local_appdata, r"Microsoft\Windows\WER\ReportArchive"),
                os.path.join(local_appdata, r"Microsoft\Windows\WER\ReportQueue")
            ]
        }
    }
    
    # Añadir perfiles de Firefox dinámicamente si existen
    carpeta_firefox = os.path.join(local_appdata, r"Mozilla\Firefox\Profiles")
    if os.path.exists(carpeta_firefox):
        for subcarpeta in glob.glob(os.path.join(carpeta_firefox, "*", "cache2")):
            rutas_categorias["cache_navegadores"]["carpetas"].append(subcarpeta)
            
    return rutas_categorias


def escanear_carpeta(ruta_carpeta):
    """
    Recorre recursivamente una carpeta y calcula cuántos archivos contiene y el peso total.
    
    Parámetros:
        ruta_carpeta (str): Ruta de la carpeta a inspeccionar.
        
    Retorna:
        tuple: (cantidad_archivos, total_bytes, lista_de_rutas_archivos)
    """
    total_archivos = 0
    total_bytes = 0
    lista_archivos = []
    
    if not os.path.exists(ruta_carpeta):
        return 0, 0, []
        
    try:
        # Usamos os.walk para recorrer la carpeta y sus subcarpetas
        for raiz, directorios, archivos in os.walk(ruta_carpeta):
            for nombre_archivo in archivos:
                ruta_completa = os.path.join(raiz, nombre_archivo)
                try:
                    # Obtenemos el tamaño del archivo
                    tamano = os.path.getsize(ruta_completa)
                    total_bytes += tamano
                    total_archivos += 1
                    lista_archivos.append(ruta_completa)
                except (PermissionError, FileNotFoundError, OSError):
                    # Si un archivo está abierto por otro programa o no tenemos permisos,
                    # lo ignoramos y continuamos con el siguiente de forma segura.
                    continue
    except (PermissionError, OSError):
        # Si la carpeta completa no permite acceso, continuamos sin caer
        pass
        
    return total_archivos, total_bytes, lista_archivos


def analizar_sistema(callback_progreso=None):
    """
    Ejecuta el análisis completo de todas las categorías de archivos temporales.
    
    Parámetros:
        callback_progreso (función, opcional): Función que recibe (porcentaje, mensaje)
        para actualizar la interfaz gráfica en tiempo real.
        
    Retorna:
        dict: Resumen completo con los resultados por categoría y totales generales.
    """
    categorias_config = obtener_rutas_por_categoria()
    
    resultados = {
        "categorias": {},
        "total_archivos": 0,
        "total_bytes": 0,
        "total_formateado": "0 B"
    }
    
    # Cantidad total de pasos para calcular el porcentaje
    total_pasos = len(categorias_config) + 1  # Categorías + Papelera
    paso_actual = 0
    
    # 1. Analizamos cada categoría de carpetas
    for id_cat, datos_cat in categorias_config.items():
        paso_actual += 1
        porcentaje = int((paso_actual / total_pasos) * 100)
        
        if callback_progreso:
            callback_progreso(porcentaje, f"Analizando {datos_cat['nombre']}...")
            
        archivos_cat = 0
        bytes_cat = 0
        rutas_encontradas = []
        
        # Recorremos cada carpeta asociada a esta categoría
        for carpeta in datos_cat["carpetas"]:
            if os.path.exists(carpeta):
                cant, b, lista = escanear_carpeta(carpeta)
                archivos_cat += cant
                bytes_cat += b
                rutas_encontradas.extend(lista)
                
        resultados["categorias"][id_cat] = {
            "id": id_cat,
            "nombre": datos_cat["nombre"],
            "descripcion": datos_cat["descripcion"],
            "archivos": archivos_cat,
            "bytes": bytes_cat,
            "tamano_formateado": formatear_tamano(bytes_cat),
            "rutas": rutas_encontradas
        }
        
        resultados["total_archivos"] += archivos_cat
        resultados["total_bytes"] += bytes_cat

    # 2. Analizamos la Papelera de Reciclaje
    paso_actual += 1
    porcentaje = 100
    if callback_progreso:
        callback_progreso(porcentaje, "Consultando Papelera de Reciclaje...")
        
    datos_papelera = consultar_papelera()
    resultados["categorias"]["papelera"] = {
        "id": "papelera",
        "nombre": "Papelera de Reciclaje",
        "descripcion": "Archivos eliminados que aún ocupan espacio en el disco duro.",
        "archivos": datos_papelera["archivos"],
        "bytes": datos_papelera["bytes"],
        "tamano_formateado": formatear_tamano(datos_papelera["bytes"]),
        "rutas": []  # La papelera se limpia a través de la API oficial de Windows
    }
    
    resultados["total_archivos"] += datos_papelera["archivos"]
    resultados["total_bytes"] += datos_papelera["bytes"]
    resultados["total_formateado"] = formatear_tamano(resultados["total_bytes"])
    
    if callback_progreso:
        callback_progreso(100, f"Análisis finalizado: {resultados['total_archivos']} archivos ({resultados['total_formateado']})")
        
    return resultados
