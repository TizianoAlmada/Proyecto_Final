"""
Módulo: utilidades.py
Descripción: Funciones auxiliares y de uso general para el Limpiador de PC.
Nivel: 3.º Año - Escuela Técnica en Programación

En este archivo agrupamos funciones matemáticas y de manejo de rutas que son
utilizadas por varios módulos a la vez. Así evitamos repetir código.
"""

import os
import sys
from pathlib import Path


def formatear_tamano(cantidad_bytes):
    """
    Convierte una cantidad de bytes a una cadena legible (B, KB, MB, GB).
    
    Explicación para 3.º año:
    En informática, 1 Kilobyte equivale a 1024 Bytes.
    Dividimos sucesivamente entre 1024 hasta encontrar la unidad adecuada
    para que el número no tenga demasiados dígitos.
    
    Ejemplo:
        formatear_tamano(1048576) -> "1.00 MB"
    """
    if cantidad_bytes is None or cantidad_bytes < 0:
        return "0 B"
    
    # Lista con las unidades de medida en orden ascendente
    unidades = ['B', 'KB', 'MB', 'GB', 'TB']
    
    tamano = float(cantidad_bytes)
    indice_unidad = 0
    
    # Mientras el tamaño sea mayor o igual a 1024 y tengamos unidades mayores
    while tamano >= 1024.0 and indice_unidad < len(unidades) - 1:
        tamano = tamano / 1024.0
        indice_unidad += 1
        
    # Formateamos a 2 decimales para que sea estético y claro
    if indice_unidad == 0:
        return f"{int(tamano)} {unidades[indice_unidad]}"
    else:
        return f"{tamano:.2f} {unidades[indice_unidad]}"


def obtener_ruta_recurso(nombre_relativo):
    """
    Obtiene la ruta absoluta hacia un archivo de recursos (imágenes, iconos, etc.).
    
    Explicación para 3.º año:
    Cuando ejecutamos el script directamente con Python, los archivos se buscan
    relativos a la carpeta del proyecto.
    Pero cuando el programa se compila a un archivo .exe con PyInstaller, los archivos
    se descomprimen temporalmente en una carpeta oculta del sistema guardada en
    sys._MEIPASS. Esta función detecta automáticamente en qué modo estamos trabajando.
    """
    try:
        # Modo PyInstaller (archivo ejecutable .exe)
        carpeta_base = sys._MEIPASS
    except AttributeError:
        # Modo desarrollo habitual (ejecutando con Python)
        carpeta_base = os.path.abspath(os.path.dirname(__file__))
        
    return os.path.join(carpeta_base, nombre_relativo)


def es_ruta_segura(ruta_a_comprobar, lista_carpetas_permitidas):
    """
    Comprueba si una ruta pertenece estrictamente a una de las carpetas temporales permitidas.
    
    Esta función es CLAVE PARA LA SEGURIDAD:
    Impide que el limpiador intente borrar carpetas personales como Documentos,
    Imágenes, el Escritorio o directorios críticos de Windows como System32.
    """
    try:
        # Convertimos ambas rutas a rutas absolutas y normalizadas para evitar trucos como '../'
        ruta_evaluada = Path(ruta_a_comprobar).resolve()
        
        # Lista negra explícita de carpetas que JAMÁS se deben tocar
        carpetas_prohibidas = [
            Path(os.environ.get('USERPROFILE', '')).resolve() / "Desktop",
            Path(os.environ.get('USERPROFILE', '')).resolve() / "Documents",
            Path(os.environ.get('USERPROFILE', '')).resolve() / "Downloads",
            Path(os.environ.get('USERPROFILE', '')).resolve() / "Pictures",
            Path(os.environ.get('USERPROFILE', '')).resolve() / "Music",
            Path(os.environ.get('USERPROFILE', '')).resolve() / "Videos",
            Path(os.environ.get('SystemRoot', 'C:\\Windows')).resolve() / "System32",
            Path(os.environ.get('ProgramFiles', 'C:\\Program Files')).resolve(),
        ]
        
        for carpeta_prohibida in carpetas_prohibidas:
            # Si la ruta coincide exactamente con una carpeta prohibida, denegar
            if ruta_evaluada == carpeta_prohibida or carpeta_prohibida in ruta_evaluada.parents:
                return False
        
        # Verificar que la ruta pertenezca al menos a una carpeta permitida
        for carpeta_permitida in lista_carpetas_permitidas:
            ruta_base_permitida = Path(carpeta_permitida).resolve()
            # La ruta debe ser hija de la carpeta permitida (estar dentro de ella)
            if ruta_base_permitida in ruta_evaluada.parents or ruta_evaluada == ruta_base_permitida:
                return True
                
        return False
    except Exception:
        # Ante cualquier error o duda, por seguridad rechazamos la ruta
        return False
