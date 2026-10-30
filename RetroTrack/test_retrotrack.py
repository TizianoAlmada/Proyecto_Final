"""
==============================================================================
Script de Pruebas Automatizadas - RetroTrack Espacial
==============================================================================
Verifica:
1. Módulo historial.py: guardado en CSV, modo append, columnas (incluyendo nave/piloto).
2. Módulo personajes.py: presencia de naves Astra y Nova, dibujo sin errores.
3. Módulo estadisticas.py: cálculo de promedios, máximos y generación de estadisticas.png.
4. Módulo juego.py: creación de asteroides, campo estelar y colisiones.
5. Módulo menu.py y main.py: renderizado de pantallas sin dependencias circulares ni NameError.
==============================================================================
"""

import os
import sys
import tempfile
from pathlib import Path

# Configurar entorno headless para pruebas
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_test")

import pygame
import matplotlib
matplotlib.use("Agg")

DIRECTORIO_PROYECTO = Path(__file__).resolve().parent
sys.path.insert(0, str(DIRECTORIO_PROYECTO))

import historial
import personajes
import estadisticas
import juego
import menu

def ejecutar_pruebas():
    print("=" * 65)
    print(" INICIANDO BATERÍA DE PRUEBAS TÉCNICAS - RETROTRACK ESPACIAL")
    print("=" * 65)

    # 1. Probar módulo historial.py
    print("\n[TEST 1] Verificación de historial.py y persistencia en CSV...")
    ruta_csv = historial.obtener_ruta_csv()
    ruta_backup = ruta_csv + ".bak_test"

    if os.path.exists(ruta_csv):
        os.rename(ruta_csv, ruta_backup)

    try:
        partidas_iniciales = historial.leer_partidas()
        assert len(partidas_iniciales) == 0, "El historial inicial debe estar vacío"
        assert historial.obtener_mejor_puntuacion() == 0, "El récord inicial debe ser 0"

        assert historial.guardar_partida(14.5, 320, "Astra") is True
        assert historial.guardar_partida(22.0, 580, "Nova") is True
        assert historial.guardar_partida(35.2, 940, "Astra") is True

        partidas = historial.leer_partidas()
        assert len(partidas) == 3, f"Se esperaban 3 partidas, se leyeron {len(partidas)}"
        assert partidas[0]["personaje"] == "Astra"
        assert partidas[1]["personaje"] == "Nova"
        assert partidas[2]["puntuacion"] == 940
        assert historial.obtener_mejor_puntuacion() == 940
        assert historial.obtener_total_partidas() == 3
        print("  -> PASADO: Guardado en CSV con columnas correctas y modo append verificado.")

        # 2. Probar módulo personajes.py (Naves Astra y Nova)
        print("\n[TEST 2] Verificación de personajes.py (Naves Astra y Nova)...")
        pygame.init()
        superficie_prueba = pygame.Surface((200, 200))
        
        lista_p = personajes.obtener_lista_personajes()
        nombres = [p["nombre"] for p in lista_p]
        assert "Astra" in nombres and "Nova" in nombres, "Deben existir Astra y Nova"

        personajes.dibujar_personaje(superficie_prueba, 50, 50, "Astra", anim_paso=2)
        personajes.dibujar_personaje(superficie_prueba, 100, 50, "Nova", anim_paso=2)
        print("  -> PASADO: Naves Astra y Nova definidas y dibujadas correctamente con Pygame.")

        # 3. Probar módulo estadisticas.py
        print("\n[TEST 3] Verificación de estadisticas.py y gráfico estadisticas.png...")
        resumen = estadisticas.obtener_resumen_estadisticas()
        assert resumen["hay_datos"] is True
        assert resumen["total_partidas"] == 3
        assert resumen["mejor_puntuacion"] == 940
        promedio_esperado = round((320 + 580 + 940) / 3, 1)
        assert resumen["puntuacion_promedio"] == promedio_esperado

        exito_grafico, ruta_png = estadisticas.generar_grafico_estadisticas()
        assert exito_grafico is True, "La generación del gráfico debió ser exitosa"
        assert os.path.exists(ruta_png), f"El archivo {ruta_png} no fue creado en disco"
        print(f"  -> PASADO: Resumen de datos exacto y archivo {os.path.basename(ruta_png)} generado.")

        # 4. Probar módulo juego.py (Espacio y Asteroides)
        print("\n[TEST 4] Verificación de mecánicas de juego.py (estrellas y asteroides)...")
        estrellas = juego.crear_campo_estrellas()
        assert len(estrellas) > 0, "Debe haber estrellas en el campo"

        ast = juego.crear_asteroide(velocidad_base=5.0)
        assert ast["rect"].y == -ast["rect"].height
        assert ast["tipo"] in [0, 1, 2, 3]

        rect_jugador = pygame.Rect(100, 100, 44, 40)
        ast["rect"].topleft = (100, 100)
        assert rect_jugador.colliderect(ast["rect"]) is True, "Debe detectar la colisión espacial"
        print("  -> PASADO: Asteroides, estrellas, física y colisión verificados.")

        # 5. Probar importaciones generales y renderizado de pantallas
        print("\n[TEST 5] Verificación de estructura modular, imports y renderizado de pantallas...")
        import main
        assert hasattr(main, "iniciar_aplicacion")
        assert hasattr(menu, "mostrar_menu_principal")

        pantalla_test = pygame.display.set_mode((800, 600))
        reloj_test = pygame.time.Clock()

        # Renderizado de menú
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        accion_menu, pers_menu = menu.mostrar_menu_principal(pantalla_test, reloj_test, "Astra")
        assert accion_menu == "salir"

        # Renderizado de selección de naves
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        pers_sel = personajes.mostrar_pantalla_seleccion(pantalla_test, reloj_test, "Nova")
        assert pers_sel in ["Astra", "Nova"]

        # Renderizado de pantalla de estadísticas integrada
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        estadisticas.mostrar_pantalla_estadisticas(pantalla_test, reloj_test)

        # Renderizado de partida espacial
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        accion_juego = juego.iniciar_partida(pantalla_test, reloj_test, "Astra")
        assert accion_juego == "salir"

        print("  -> PASADO: Todas las pantallas renderizan perfectamente sin errores.")

        print("\n" + "=" * 65)
        print(" ¡TODAS LAS PRUEBAS ESPACIALES (5/5) FUERON SUPERADAS CON ÉXITO!")
        print("=" * 65)

    finally:
        if os.path.exists(ruta_backup):
            if os.path.exists(ruta_csv):
                os.remove(ruta_csv)
            os.rename(ruta_backup, ruta_csv)
        pygame.quit()

if __name__ == "__main__":
    ejecutar_pruebas()
