"""
==============================================================================
Generador de Datos de Demostración - RetroTrack
==============================================================================
Este script opcional permite poblar 'historial_partidas.csv' con una serie
de partidas simuladas que muestran una curva de progreso realista.

Útil para docentes y estudiantes que deseen visualizar los gráficos y
estadísticas de inmediato sin tener que jugar varias partidas previamente.

Uso:
    python generar_datos_ejemplo.py
==============================================================================
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Asegurar que se encuentre el módulo de estadísticas
DIRECTORIO_ACTUAL = Path(__file__).resolve().parent
sys.path.insert(0, str(DIRECTORIO_ACTUAL))

import estadisticas

PARTIDAS_SIMULADAS = [
    {"segundos_atras": 3600, "duracion": 11.40, "puntaje": 230},
    {"segundos_atras": 3000, "duracion": 16.85, "puntaje": 390},
    {"segundos_atras": 2400, "duracion": 21.20, "puntaje": 540},
    {"segundos_atras": 1800, "duracion": 27.50, "puntaje": 720},
    {"segundos_atras": 1200, "duracion": 33.10, "puntaje": 890},
    {"segundos_atras": 600,  "duracion": 42.60, "puntaje": 1180},
]


def generar_datos():
    print("=" * 60)
    print(" GENERADOR DE DATOS DE EJEMPLO - RETROTRACK")
    print("=" * 60)
    
    ahora = datetime.now()
    ruta_csv = estadisticas.RUTA_CSV

    # Si ya existe, consultamos o lo reemplazamos limpiamente
    print(f"\n[+] Generando {len(PARTIDAS_SIMULADAS)} partidas de prueba en: {ruta_csv.name}")

    # Escribir cabecera y partidas simuladas
    with open(ruta_csv, mode="w", encoding="utf-8", newline="") as f:
        f.write("fecha,duracion_segundos,puntaje\n")
        for i, p in enumerate(PARTIDAS_SIMULADAS, start=1):
            fecha = (ahora - timedelta(seconds=p["segundos_atras"])).strftime("%Y-%m-%d %H:%M:%S")
            linea = f"{fecha},{p['duracion']},{p['puntaje']}\n"
            f.write(linea)
            print(f"  Partida {i}: {fecha} | {p['duracion']}s | {p['puntaje']} pts")

    print("\n[OK] Datos de demostración generados con éxito.")
    print("Ahora podés ejecutar 'python main.py' y presionar [ 2 ] para ver los gráficos con Matplotlib.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    generar_datos()
