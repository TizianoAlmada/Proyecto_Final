"""
Archivo de Pruebas Unitarias y de Integración: test_limpiador.py
Nivel: 3.º Año - Escuela Técnica en Programación

Este script ejecuta comprobaciones automáticas de cada uno de los módulos
para garantizar que funcionen correctamente antes de crear el archivo ejecutable.
"""

import os
import sys
import tempfile
import tkinter as tk

# Importamos todos los módulos a comprobar
import utilidades
import almacenamiento
import historial
import analizador
import limpiador
from interfaz import VentanaPrincipal


def probar_utilidades():
    print("[1/6] Probando módulo utilidades.py...")
    # Probar formateo de tamaños
    assert utilidades.formatear_tamano(0) == "0 B"
    assert utilidades.formatear_tamano(1024) == "1.00 KB"
    assert utilidades.formatear_tamano(1048576) == "1.00 MB"
    assert utilidades.formatear_tamano(1073741824) == "1.00 GB"
    
    # Probar seguridad de rutas
    temp_dir = tempfile.gettempdir()
    archivo_temp = os.path.join(temp_dir, "test_inofensivo.tmp")
    assert utilidades.es_ruta_segura(archivo_temp, [temp_dir]) is True
    
    # Rutas prohibidas nunca deben ser aceptadas
    user_docs = os.path.join(os.environ.get("USERPROFILE", ""), "Documents")
    assert utilidades.es_ruta_segura(user_docs, [temp_dir]) is False
    assert utilidades.es_ruta_segura("C:\\Windows\\System32\\cmd.exe", [temp_dir]) is False
    print("  -> utilidades.py OK!")


def probar_almacenamiento():
    print("[2/6] Probando módulo almacenamiento.py...")
    unidades = almacenamiento.obtener_unidades_disponibles()
    assert len(unidades) > 0, "Debe existir al menos una unidad de disco."
    
    info = almacenamiento.obtener_informacion_disco("C:\\")
    assert info["total_bytes"] > 0, "El disco C: debe tener espacio total mayor a cero."
    assert info["libre_bytes"] > 0, "El disco C: debe tener espacio libre mayor a cero."
    assert 0 <= info["porcentaje_usado"] <= 100, "El porcentaje de uso debe estar entre 0 y 100."
    print(f"  -> almacenamiento.py OK! (Disco C: {info['total_formateado']}, Libre: {info['libre_formateado']})")


def probar_historial():
    print("[3/6] Probando módulo historial.py...")
    # Vaciar primero para tener entorno limpio de prueba
    historial.vaciar_historial()
    assert len(historial.cargar_historial()) == 0
    
    # Guardar un registro de prueba
    exito = historial.guardar_registro(10, 52428800, ["Temporales de Prueba"])
    assert exito is True
    
    registros = historial.cargar_historial()
    assert len(registros) == 1
    assert registros[0]["archivos_eliminados"] == 10
    assert registros[0]["espacio_formateado"] == "50.00 MB"
    
    # Vaciar después de la prueba
    historial.vaciar_historial()
    assert len(historial.cargar_historial()) == 0
    print("  -> historial.py OK!")


def probar_analizador():
    print("[4/6] Probando módulo analizador.py...")
    papelera = analizador.consultar_papelera()
    assert "archivos" in papelera and "bytes" in papelera
    
    rutas_cat = analizador.obtener_rutas_por_categoria()
    assert "temp_usuario" in rutas_cat
    assert "temp_windows" in rutas_cat
    print(f"  -> analizador.py OK! (Papelera: {papelera['archivos']} archivos, {papelera['bytes']} bytes)")


def probar_limpiador_seguro():
    print("[5/6] Probando módulo limpiador.py en entorno controlado...")
    temp_dir = tempfile.gettempdir()
    
    # Creamos un archivo temporal falso de prueba en temp_dir
    archivo_falso = os.path.join(temp_dir, "limpiador_test_temporal_seguro.tmp")
    with open(archivo_falso, "w") as f:
        f.write("Archivo de prueba temporal para test unitario.")
        
    assert os.path.exists(archivo_falso)
    
    # Simulamos el resultado del análisis
    tamano_falso = os.path.getsize(archivo_falso)
    resultados_simulados = {
        "categorias": {
            "temp_usuario": {
                "nombre": "Archivos Temporales de Usuario",
                "archivos": 1,
                "bytes": tamano_falso,
                "tamano_formateado": utilidades.formatear_tamano(tamano_falso),
                "rutas": [archivo_falso]
            }
        }
    }
    
    # Ejecutamos la limpieza sobre la categoría 'temp_usuario'
    res_limpieza = limpiador.ejecutar_limpieza(resultados_simulados, ["temp_usuario"])
    assert res_limpieza["archivos_eliminados"] == 1
    assert res_limpieza["bytes_liberados"] == tamano_falso
    assert not os.path.exists(archivo_falso), "El archivo temporal de prueba debió ser eliminado con éxito."
    
    # Comprobamos que se guardó en el historial
    registros = historial.cargar_historial()
    assert len(registros) >= 1
    # Limpiamos el registro de prueba del historial
    historial.vaciar_historial()
    print("  -> limpiador.py OK! (Archivo temporal de prueba creado y eliminado con total seguridad)")


def probar_interfaz_headless():
    print("[6/6] Probando carga de la interfaz gráfica (interfaz.py)...")
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana para no interrumpir
    app = VentanaPrincipal(root)
    assert app is not None
    assert app.root.title() != ""
    assert len(app.variables_checkbox) == 5, "Deben estar presentes las 5 categorías con checkboxes."
    root.destroy()
    print("  -> interfaz.py OK! (Ventana y widgets inicializados sin errores)")


if __name__ == "__main__":
    print("==================================================")
    print("   INICIANDO PRUEBAS DEL LIMPIADOR DE ESPACIO    ")
    print("==================================================")
    probar_utilidades()
    probar_almacenamiento()
    probar_historial()
    probar_analizador()
    probar_limpiador_seguro()
    probar_interfaz_headless()
    print("==================================================")
    print("   TODAS LAS PRUEBAS PASARON EXITOSAMENTE (6/6)   ")
    print("==================================================")
