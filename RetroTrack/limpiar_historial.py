"""
==============================================================================
Limpiador de Historial - RetroTrack
==============================================================================
Elimina de forma segura el archivo 'historial_partidas.csv' para reiniciar
las estadísticas y probar el comportamiento de arranque sin datos.

Uso:
    python limpiar_historial.py
==============================================================================
"""

from pathlib import Path

RUTA_CSV = Path(__file__).resolve().parent / "historial_partidas.csv"

def limpiar():
    if RUTA_CSV.exists():
        RUTA_CSV.unlink()
        print(f"[RetroTrack] El archivo '{RUTA_CSV.name}' ha sido eliminado.")
        print("[RetroTrack] El historial ahora está en cero.")
    else:
        print(f"[RetroTrack] No había ningún archivo '{RUTA_CSV.name}' para eliminar.")

if __name__ == "__main__":
    limpiar()
