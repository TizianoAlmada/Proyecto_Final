# ==============================================================================
# MÓDULO: main.py - Punto de Entrada Principal de RetroTrack
# ==============================================================================
# Este archivo es el punto de inicio de la aplicación.
# Su responsabilidad es:
# 1. Inicializar la biblioteca Pygame y configurar la ventana de 800x600.
# 2. Coordinar la navegación entre el Menú Principal, la Selección de Personajes
#    y el bucle de la Partida.
# 3. Mantener en memoria el personaje seleccionado (Alex o Sara).
# 4. Finalizar el programa de forma limpia y ordenada al salir.
#
# Ejecución:
#     python main.py
# ==============================================================================

import sys
import os
import pygame

# Ocultar el mensaje publicitario de Pygame al iniciar en la consola
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Importamos los módulos que creamos para el proyecto
import menu
import juego
import personajes

# Configuración de dimensiones fijas de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
TITULO_VENTANA = "RetroTrack - Videojuego Arcade 2D & Estadísticas"


def iniciar_aplicacion():
    """
    Función principal que arranca el juego y coordina la transición entre pantallas.
    """
    pygame.init()
    pygame.font.init()

    # Creación de la ventana y el reloj
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption(TITULO_VENTANA)
    reloj = pygame.time.Clock()

    # Personaje seleccionado por defecto al abrir el juego
    # Nave espacial seleccionada por defecto al abrir el juego
    personaje_actual = "Astra"

    # Bucle general de navegación de la aplicación
    ejecutando_aplicacion = True

    while ejecutando_aplicacion:
        # 1. Mostramos el Menú Principal
        accion, personaje_actual = menu.mostrar_menu_principal(
            pantalla=pantalla,
            reloj=reloj,
            personaje_actual=personaje_actual
        )

        # 2. Evaluamos la decisión del usuario en el menú
        if accion == "salir":
            ejecutando_aplicacion = False

        elif accion == "jugar":
            # El usuario eligió jugar: entramos al bucle de partidas
            jugando = True
            while jugando:
                # Iniciamos la partida con el personaje activo
                siguiente_paso = juego.iniciar_partida(
                    pantalla=pantalla,
                    reloj=reloj,
                    nombre_personaje=personaje_actual
                )

                if siguiente_paso == "reiniciar":
                    # Vuelve a empezar de inmediato con el mismo personaje
                    continue

                elif siguiente_paso == "cambiar_personaje":
                    # Abre la pantalla de selección y vuelve a jugar
                    personaje_actual = personajes.mostrar_pantalla_seleccion(
                        pantalla=pantalla,
                        reloj=reloj,
                        personaje_actual=personaje_actual
                    )
                    continue

                elif siguiente_paso == "menu":
                    # Rompe el bucle de partidas para regresar al menú principal
                    jugando = False

                elif siguiente_paso == "salir":
                    # Cierra por completo la aplicación
                    jugando = False
                    ejecutando_aplicacion = False

    # Cierre seguro y ordenado de los subsistemas de Pygame y del proceso
    pygame.quit()
    print("\n[RetroTrack] ¡Gracias por jugar! Programa cerrado correctamente.")
    sys.exit(0)


# Comprobación estándar de Python para ejecutar la función si este archivo es el principal
if __name__ == "__main__":
    iniciar_aplicacion()
