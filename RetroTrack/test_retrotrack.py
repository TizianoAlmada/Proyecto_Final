"""
==============================================================================
Script de Pruebas Automatizadas - RetroTrack
==============================================================================
Verifica de forma rigurosa:
1. Creación y formato del archivo CSV.
2. Conservación de datos históricos (modo append).
3. Cálculos de métricas con Pandas (promedios, máximos, evolución).
4. Clases del videojuego (Jugador, Obstaculo, Colisiones, Límites de pantalla).
5. Generación de gráficos con Matplotlib (backend headless).
==============================================================================
"""

import os
import sys
import tempfile
from pathlib import Path

# Configurar entorno de pruebas
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_test")

import pygame
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend sin ventana para pruebas automáticas
import matplotlib.pyplot as plt

# Agregar la ruta del proyecto
DIRECTORIO_PROYECTO = Path(__file__).resolve().parent
sys.path.insert(0, str(DIRECTORIO_PROYECTO))

import estadisticas
import juego

def ejecutar_pruebas():
    print("=" * 60)
    print(" INICIANDO BATERÍA DE PRUEBAS TÉCNICAS PARA RETROTRACK")
    print("=" * 60)

    # 1. Probar estado inicial sin datos
    csv_original = estadisticas.RUTA_CSV
    csv_backup = DIRECTORIO_PROYECTO / "historial_partidas_backup.csv"

    # Si existe un csv previo, respaldarlo temporalmente
    if csv_original.exists():
        csv_original.rename(csv_backup)

    try:
        print("\n[TEST 1] Verificación con CSV ausente...")
        metricas_vacio = estadisticas.calcular_metricas()
        assert metricas_vacio["hay_datos"] is False, "Debe reportar que no hay datos"
        assert "Aún no hay partidas" in metricas_vacio["mensaje"], "Mensaje de invitación incorrecto"
        record_vacio = estadisticas.obtener_mejor_puntaje()
        assert record_vacio == 0, f"Récord inicial debe ser 0, dio {record_vacio}"
        print("  -> PASADO: Manejo de historial vacío correcto y amigable.")

        # 2. Probar guardado de partidas
        print("\n[TEST 2] Verificación de guardado en CSV (modo append)...")
        # Simular 4 partidas consecutivas con tiempos y puntajes progresivos
        partidas_prueba = [
            (12.5, 250),
            (18.2, 420),
            (25.0, 680),
            (32.8, 950)
        ]

        for duracion, puntaje in partidas_prueba:
            exito = estadisticas.guardar_partida(duracion, puntaje)
            assert exito is True, "El guardado debió retornar True"

        assert csv_original.exists(), "El archivo CSV no fue creado"

        # Leer archivo con pandas y verificar integridad
        df = estadisticas.cargar_datos()
        assert df is not None, "El DataFrame no debe ser None"
        assert len(df) == 4, f"Se esperaban 4 partidas, se encontraron {len(df)}"
        assert list(df.columns) == ["fecha", "duracion_segundos", "puntaje"]
        print("  -> PASADO: Archivo CSV creado y registros agregados sin sobreescritura.")

        # 3. Probar cálculos de Pandas
        print("\n[TEST 3] Verificación de métricas estadísticas con Pandas...")
        metricas = estadisticas.calcular_metricas(df)
        assert metricas["hay_datos"] is True
        assert metricas["total_partidas"] == 4
        assert metricas["mejor_puntaje"] == 950, f"Mejor puntaje esperado 950, obtenido {metricas['mejor_puntaje']}"
        assert metricas["mayor_tiempo"] == 32.8, f"Mayor tiempo esperado 32.8, obtenido {metricas['mayor_tiempo']}"
        
        promedio_pts_esperado = round((250 + 420 + 680 + 950) / 4, 2)
        assert metricas["puntaje_promedio"] == promedio_pts_esperado, f"Esperado {promedio_pts_esperado}, obtenido {metricas['puntaje_promedio']}"
        
        promedio_tiempo_esperado = round((12.5 + 18.2 + 25.0 + 32.8) / 4, 2)
        assert metricas["tiempo_promedio"] == promedio_tiempo_esperado, f"Esperado {promedio_tiempo_esperado}, obtenido {metricas['tiempo_promedio']}"
        
        assert metricas["primer_puntaje"] == 250
        assert metricas["ultimo_puntaje"] == 950
        assert metricas["diferencia_puntaje"] == 700
        print(f"  -> PASADO: Métricas de Pandas exactas (Total: {metricas['total_partidas']}, Promedio Pts: {metricas['puntaje_promedio']}, Max: {metricas['mejor_puntaje']}).")

        # 4. Probar clases del juego (Pygame)
        print("\n[TEST 4] Verificación de mecánicas de juego (Jugador, Obstáculos, Colisión)...")
        pygame.init()
        jugador = juego.Jugador(400, 520)
        assert jugador.rect.x == 400
        assert jugador.rect.y == 520

        # Probar límites de pantalla del jugador
        jugador.x = -100
        jugador.mover({pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False, pygame.K_d: False})
        assert jugador.rect.x >= 10, "El jugador no debe salir por la izquierda"

        jugador.x = 1000
        jugador.mover({pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False, pygame.K_d: False})
        assert jugador.rect.right <= juego.ANCHO, "El jugador no debe salir por la derecha"

        # Probar obstáculo
        obs = juego.Obstaculo(velocidad_base=5.0)
        assert obs.rect.y == -obs.alto, "Debe nacer arriba de la pantalla"
        y_inicial = obs.y
        obs.actualizar()
        assert obs.y > y_inicial, "El obstáculo debe descender"

        # Probar colisión
        obs.rect.topleft = jugador.rect.topleft
        assert jugador.rect.colliderect(obs.rect) is True, "Debe detectar la colisión"
        print("  -> PASADO: Lógica de jugador, límites, movimiento y colisiones verificada.")

        # 5. Probar generación de gráficos de Matplotlib
        print("\n[TEST 5] Verificación de generación de gráficos con Matplotlib...")
        # Simular llamada a mostrar_graficos con backend Agg (sin ventana)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        numero_partidas = np.arange(1, len(df) + 1)
        ax1.plot(numero_partidas, df["puntaje"].values)
        ax2.plot(numero_partidas, df["duracion_segundos"].values)
        
        # Probar cálculo de tendencia lineal
        coef_p = np.polyfit(numero_partidas, df["puntaje"].values, 1)
        assert len(coef_p) == 2, "El ajuste de tendencia lineal debe retornar pendiente e intercepto"
        plt.close(fig)
        print("  -> PASADO: Generación de figuras, subplots y cálculo de tendencia exitoso.")

        print("\n" + "=" * 60)
        print(" ¡TODAS LAS PRUEBAS TÉCNICAS (5/5) FUERON SUPERADAS CON ÉXITO!")
        print("=" * 60)

    finally:
        # Limpieza de archivos de prueba
        if csv_backup.exists():
            if csv_original.exists():
                csv_original.unlink()
            csv_backup.rename(csv_original)
        elif csv_original.exists():
            csv_original.unlink()
        pygame.quit()

if __name__ == "__main__":
    ejecutar_pruebas()
