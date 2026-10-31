"""
Módulo: main.py
Descripción: Punto de entrada principal para el Limpiador de Almacenamiento en Windows.
Nivel: 3.º Año - Escuela Técnica en Programación

Este archivo es el que se ejecuta para iniciar el programa.
Se encarga de:
1. Verificar que existan las carpetas necesarias ('datos' y 'recursos').
2. Iniciar el motor gráfico de Tkinter ('tk.Tk()').
3. Crear una instancia de nuestra clase 'VentanaPrincipal' definida en 'interfaz.py'.
4. Iniciar el bucle de eventos 'root.mainloop()', que mantiene la ventana abierta y receptiva.
"""

import os
import tkinter as tk
from interfaz import VentanaPrincipal


def asegurar_entorno():
    """
    Crea las carpetas 'datos' y 'recursos' en el directorio del programa si no existen.
    
    Explicación para 3.º año:
    Al arrancar el software por primera vez en una computadora nueva, nos aseguramos
    de que existan los directorios donde se guardará el historial JSON y los recursos.
    """
    carpeta_base = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(carpeta_base, "datos"), exist_ok=True)
    os.makedirs(os.path.join(carpeta_base, "recursos"), exist_ok=True)


def main():
    """
    Función principal del programa.
    """
    # 1. Aseguramos la existencia de las carpetas locales
    asegurar_entorno()
    
    # 2. Inicializamos la ventana raíz de Tkinter
    root = tk.Tk()
    
    # 3. Instanciamos la interfaz gráfica conectando todos los módulos
    app = VentanaPrincipal(root)
    
    # 4. Iniciamos el bucle principal de la aplicación de escritorio.
    # El método mainloop() escucha los clics del mouse, eventos del teclado y actualizaciones visuales.
    root.mainloop()


# Esta condición comprueba si el archivo está siendo ejecutado directamente por el usuario
# (y no importado como módulo desde otro script).
if __name__ == "__main__":
    main()
