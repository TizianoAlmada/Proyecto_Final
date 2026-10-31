"""
Módulo: limpiador.py
Descripción: Ejecuta la eliminación segura de archivos temporales seleccionados por el usuario.
Nivel: 3.º Año - Escuela Técnica en Programación

PROTOCOLO DE SEGURIDAD ESTRICTO:
1. Solo se eliminan archivos de las categorías explícitamente autorizadas por el usuario.
2. Cada archivo se valida con 'es_ruta_segura()' antes de tocarlo.
3. Jamás se tocan carpetas personales (Documentos, Imágenes, etc.) ni archivos vitales de Windows.
4. Cada archivo se intenta borrar individualmente con 'try...except'. Si Windows o un programa
   lo tiene abierto o bloqueado, se captura el error 'PermissionError' y se continúa sin fallar.
5. Se registra el resultado en el historial mediante 'historial.guardar_registro()'.
"""

import os
import ctypes
from utilidades import formatear_tamano, es_ruta_segura
from analizador import obtener_rutas_por_categoria
import historial


def vaciar_papelera_segura():
    """
    Vacía la Papelera de Reciclaje utilizando la API oficial de Windows (shell32.dll).
    
    Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
    """
    try:
        # Constantes de la API de Windows:
        # SHERB_NOCONFIRMATION = 0x00000001 (No muestra diálogo nativo de confirmación)
        # SHERB_NOPROGRESSUI  = 0x00000002 (No muestra barra de progreso nativa)
        # SHERB_NOSOUND       = 0x00000004 (Sin sonido al vaciar)
        flags = 0x00000001 | 0x00000002 | 0x00000004
        resultado = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
        return resultado == 0
    except Exception as error:
        print(f"Error al vaciar la papelera: {error}")
        return False


def ejecutar_limpieza(resultados_analisis, categorias_seleccionadas, callback_progreso=None):
    """
    Ejecuta el proceso de limpieza segura de las categorías marcadas.
    
    Parámetros:
        resultados_analisis (dict): El diccionario devuelto previamente por analizador.analizar_sistema().
        categorias_seleccionadas (list): Lista de IDs de categorías a limpiar (ej: ['temp_usuario', 'papelera']).
        callback_progreso (función, opcional): Función que recibe (porcentaje, mensaje_estado).
        
    Retorna:
        dict: Resumen con cantidad de archivos eliminados, bytes liberados y omitidos.
    """
    if not categorias_seleccionadas:
        return {
            "archivos_eliminados": 0,
            "bytes_liberados": 0,
            "espacio_formateado": "0 B",
            "archivos_omitidos": 0,
            "categorias": []
        }
        
    # Obtenemos la lista total de carpetas permitidas para la verificación de seguridad
    config_rutas = obtener_rutas_por_categoria()
    carpetas_permitidas = []
    for datos_cat in config_rutas.values():
        carpetas_permitidas.extend(datos_cat["carpetas"])
        
    archivos_eliminados = 0
    bytes_liberados = 0
    archivos_omitidos = 0
    nombres_categorias_limpiadas = []
    
    # Calculamos la cantidad total de archivos que intentaremos procesar
    total_archivos_a_procesar = 0
    for id_cat in categorias_seleccionadas:
        if id_cat in resultados_analisis.get("categorias", {}):
            total_archivos_a_procesar += len(resultados_analisis["categorias"][id_cat].get("rutas", []))
            
    # Si incluye papelera, sumamos 1 operación de papelera
    if "papelera" in categorias_seleccionadas:
        total_archivos_a_procesar += 1
        
    if total_archivos_a_procesar == 0:
        total_archivos_a_procesar = 1  # Evitamos división por cero
        
    archivos_procesados = 0
    
    # 1. Procesamos cada categoría seleccionada
    for id_cat in categorias_seleccionadas:
        if id_cat not in resultados_analisis.get("categorias", {}):
            continue
            
        datos_cat = resultados_analisis["categorias"][id_cat]
        nombres_categorias_limpiadas.append(datos_cat["nombre"])
        
        # Caso especial: Papelera de Reciclaje
        if id_cat == "papelera":
            if callback_progreso:
                callback_progreso(95, "Vaciando Papelera de Reciclaje...")
                
            exito = vaciar_papelera_segura()
            if exito:
                archivos_eliminados += datos_cat["archivos"]
                bytes_liberados += datos_cat["bytes"]
            else:
                archivos_omitidos += datos_cat["archivos"]
                
            archivos_procesados += 1
            continue
            
        # Caso general: Archivos en carpetas temporales
        rutas_archivos = datos_cat.get("rutas", [])
        
        for ruta_archivo in rutas_archivos:
            archivos_procesados += 1
            porcentaje = int((archivos_procesados / total_archivos_a_procesar) * 100)
            
            # Notificamos a la interfaz cada 25 archivos para que sea fluida
            if callback_progreso and (archivos_procesados % 25 == 0 or archivos_procesados == total_archivos_a_procesar):
                nombre_corto = os.path.basename(ruta_archivo)
                callback_progreso(porcentaje, f"Eliminando: {nombre_corto}")
                
            # VERIFICACIÓN DE SEGURIDAD 1: ¿Es una ruta autorizada?
            if not es_ruta_segura(ruta_archivo, carpetas_permitidas):
                print(f"Seguridad: Se omitió el archivo por no estar en carpeta segura: {ruta_archivo}")
                archivos_omitidos += 1
                continue
                
            # VERIFICACIÓN DE SEGURIDAD 2: ¿El archivo existe?
            if not os.path.exists(ruta_archivo):
                continue
                
            try:
                # Medimos el peso antes de eliminarlo
                tamano_archivo = os.path.getsize(ruta_archivo)
                
                # Eliminación segura
                os.remove(ruta_archivo)
                archivos_eliminados += 1
                bytes_liberados += tamano_archivo
                
            except (PermissionError, OSError, FileNotFoundError):
                # Este caso es completamente normal en Windows:
                # Ocurre cuando un archivo temporal está siendo usado por una aplicación abierta.
                # En lugar de fallar, lo registramos como omitido y seguimos adelante.
                archivos_omitidos += 1
                continue

    # 2. Limpieza de subcarpetas vacías dentro de los temporales
    for carpeta_base in carpetas_permitidas:
        if os.path.exists(carpeta_base):
            try:
                # Recorremos de abajo hacia arriba (bottom-up) para poder borrar carpetas vacías anidadas
                for raiz, directorios, archivos in os.walk(carpeta_base, topdown=False):
                    # NUNCA borrar la carpeta base raíz (ej: C:\Windows\Temp)
                    if os.path.abspath(raiz) == os.path.abspath(carpeta_base):
                        continue
                    try:
                        # os.rmdir solo borra si la carpeta está completamente vacía
                        os.rmdir(raiz)
                    except OSError:
                        # Si no está vacía o está protegida, se deja intacta
                        pass
            except Exception:
                pass
                
    # 3. Guardamos el evento en el historial persistente (JSON)
    if archivos_eliminados > 0:
        historial.guardar_registro(
            archivos_eliminados=archivos_eliminados,
            bytes_liberados=bytes_liberados,
            categorias_limpiadas=nombres_categorias_limpiadas
        )
        
    if callback_progreso:
        callback_progreso(100, f"Limpieza completada: {archivos_eliminados} archivos eliminados ({formatear_tamano(bytes_liberados)})")
        
    return {
        "archivos_eliminados": archivos_eliminados,
        "bytes_liberados": bytes_liberados,
        "espacio_formateado": formatear_tamano(bytes_liberados),
        "archivos_omitidos": archivos_omitidos,
        "categorias": nombres_categorias_limpiadas
    }
