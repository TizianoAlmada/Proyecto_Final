"""
Módulo: almacenamiento.py
Descripción: Consulta la información de almacenamiento del disco duro en Windows.
Nivel: 3.º Año - Escuela Técnica en Programación

Este archivo se encarga de averiguar:
1. Cuánto espacio total tiene el disco.
2. Cuánto espacio está ocupado.
3. Cuánto espacio libre queda disponible.
4. El porcentaje de ocupación (para dibujarlo en una barra gráfica).
"""

import os
import shutil
import string
from utilidades import formatear_tamano

# Intentamos importar psutil si está instalado en el sistema.
# Si no está instalado, utilizamos la librería estándar 'shutil', que viene incluida con Python.
# Esto asegura que el programa nunca falle por falta de una librería externa.
try:
    import psutil
    TIENE_PSUTIL = True
except ImportError:
    psutil = None
    TIENE_PSUTIL = False


def obtener_unidades_disponibles():
    """
    Detecta todas las letras de unidades de disco presentes en la computadora (C:, D:, etc.).
    
    Explicación para 3.º año:
    En Windows las unidades se nombran con letras de la A a la Z seguidas de dos puntos.
    Recorremos el abecedario y con 'os.path.exists()' verificamos cuáles existen de verdad.
    """
    unidades_encontradas = []
    for letra in string.ascii_uppercase:
        ruta_unidad = f"{letra}:\\"
        if os.path.exists(ruta_unidad):
            unidades_encontradas.append(ruta_unidad)
            
    # Si por alguna razón la lista queda vacía, aseguramos al menos la unidad C:
    if not unidades_encontradas:
        unidades_encontradas.append("C:\\")
        
    return unidades_encontradas


def obtener_informacion_disco(ruta_unidad="C:\\"):
    """
    Devuelve un diccionario con las estadísticas de almacenamiento de una unidad de disco.
    
    Parámetros:
        ruta_unidad (str): La ruta o letra del disco a consultar (por defecto 'C:\\').
        
    Retorna:
        dict: Un diccionario con los valores en bytes, formateados y porcentajes.
    """
    try:
        if TIENE_PSUTIL and psutil is not None:
            # Usando la librería psutil
            uso = psutil.disk_usage(ruta_unidad)
            total = uso.total
            usado = uso.used
            libre = uso.free
        else:
            # Usando la librería estándar shutil (muy segura y nativa de Python)
            uso = shutil.disk_usage(ruta_unidad)
            total = uso.total
            usado = uso.used
            libre = uso.free
            
        # Calculamos los porcentajes
        if total > 0:
            porcentaje_usado = (usado / total) * 100.0
            porcentaje_libre = (libre / total) * 100.0
        else:
            porcentaje_usado = 0.0
            porcentaje_libre = 0.0
            
        # Estructuramos el resultado en un diccionario ordenado y claro
        datos_disco = {
            "unidad": ruta_unidad,
            "total_bytes": total,
            "usado_bytes": usado,
            "libre_bytes": libre,
            "total_formateado": formatear_tamano(total),
            "usado_formateado": formatear_tamano(usado),
            "libre_formateado": formatear_tamano(libre),
            "porcentaje_usado": round(porcentaje_usado, 1),
            "porcentaje_libre": round(porcentaje_libre, 1)
        }
        
        return datos_disco
        
    except Exception as error:
        # En caso de que ocurra algún error (por ejemplo, unidad no lista como una lectora de CD vacía)
        print(f"Error al leer la unidad {ruta_unidad}: {error}")
        return {
            "unidad": ruta_unidad,
            "total_bytes": 0,
            "usado_bytes": 0,
            "libre_bytes": 0,
            "total_formateado": "0 B",
            "usado_formateado": "0 B",
            "libre_formateado": "0 B",
            "porcentaje_usado": 0.0,
            "porcentaje_libre": 0.0
        }
