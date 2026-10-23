"""
==============================================================================
Punto de Entrada Principal - RetroTrack (Temática Urbana)
==============================================================================
Este archivo inicializa la aplicación y gestiona el Menú Principal con Pygame:
- Navegación visual e interactiva entre opciones mediante teclado y ratón.
- Lanzamiento de la partida (módulo 'juego.py': el chico esquivando objetos).
- Consulta de estadísticas y visualización de gráficos (módulo 'estadisticas.py').
- Visualización de instrucciones y récords.
- Cierre ordenado y seguro del programa.

Ejecución:
    python main.py
==============================================================================
"""

import sys
import os
import pygame

# Ocultar el mensaje publicitario de la consola de Pygame
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Importar los módulos del proyecto
import juego
import estadisticas

# ==============================================================================
# CONFIGURACIÓN DE LA VENTANA
# ==============================================================================
ANCHO = 800
ALTO = 600
FPS = 60

# Paleta Retro Urbana
COLOR_FONDO = (18, 16, 38)
COLOR_TITULO = (0, 245, 255)         # Cian neón
COLOR_SUBTITULO = (255, 60, 90)      # Rojo coral neón
COLOR_TEXTO = (245, 245, 255)
COLOR_TEXTO_MUTED = (165, 175, 205)
COLOR_AMARILLO = (255, 220, 40)
COLOR_VERDE = (60, 240, 100)
COLOR_BOTON = (28, 30, 58)
COLOR_BOTON_HOVER = (45, 48, 92)
COLOR_BORDE_BOTON = (0, 245, 255)


class BotonMenu:
    """
    Representa un botón interactivo del menú principal con soporte para ratón y teclado.
    """
    def __init__(self, x: int, y: int, ancho: int, alto: int, texto: str, tecla_rapida: str):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.tecla_rapida = tecla_rapida
        self.seleccionado = False

    def dibujar(self, superficie: pygame.Surface, fuente: pygame.font.Font, mouse_pos: tuple[int, int]):
        esta_sobre = self.rect.collidepoint(mouse_pos) or self.seleccionado
        color_fondo = COLOR_BOTON_HOVER if esta_sobre else COLOR_BOTON
        color_borde = COLOR_TITULO if esta_sobre else (55, 65, 110)
        grosor_borde = 2 if esta_sobre else 1

        pygame.draw.rect(superficie, color_fondo, self.rect, border_radius=8)
        pygame.draw.rect(superficie, color_borde, self.rect, width=grosor_borde, border_radius=8)

        color_txt = COLOR_AMARILLO if esta_sobre else COLOR_TEXTO
        txt_surf = fuente.render(f"{self.tecla_rapida}  {self.texto}", True, color_txt)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        superficie.blit(txt_surf, txt_rect)


def mostrar_menu():
    """
    Bucle principal del Menú de RetroTrack.
    Permite navegar entre jugar, ver estadísticas y salir.
    """
    pygame.init()
    pygame.font.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("RetroTrack - Esquiva Objetos Urbanos & Analítica")
    reloj = pygame.time.Clock()

    # Fuentes del sistema
    fuente_titulo = pygame.font.SysFont("Consolas", 46, bold=True)
    fuente_subtitulo = pygame.font.SysFont("Consolas", 18, bold=True)
    fuente_botones = pygame.font.SysFont("Consolas", 20, bold=True)
    fuente_seccion = pygame.font.SysFont("Consolas", 16, bold=True)
    fuente_texto = pygame.font.SysFont("Consolas", 14)

    # Fondo urbano de la ciudad
    fondo = juego.FondoCiudad()

    # Botones principales
    ancho_btn, alto_btn = 460, 52
    centro_x = (ANCHO - ancho_btn) // 2

    botones = [
        BotonMenu(centro_x, 210, ancho_btn, alto_btn, "COMENZAR A JUGAR", "[ 1 ]"),
        BotonMenu(centro_x, 275, ancho_btn, alto_btn, "CONSULTAR ESTADÍSTICAS Y GRÁFICOS", "[ 2 ]"),
        BotonMenu(centro_x, 340, ancho_btn, alto_btn, "SALIR DEL PROGRAMA", "[ 3 ]")
    ]
    indice_seleccionado = 0

    ejecutando = True

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()

        # ======================================================================
        # GESTIÓN DE EVENTOS DEL MENÚ
        # ======================================================================
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for i, btn in enumerate(botones):
                    if btn.rect.collidepoint(mouse_pos):
                        if i == 0:
                            accion = juego.iniciar_partida(pantalla, reloj)
                            if accion == "salir":
                                ejecutando = False
                        elif i == 1:
                            abrir_estadisticas_y_graficos(pantalla, reloj)
                        elif i == 2:
                            ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    accion = juego.iniciar_partida(pantalla, reloj)
                    if accion == "salir":
                        ejecutando = False
                elif evento.key in (pygame.K_2, pygame.K_e):
                    abrir_estadisticas_y_graficos(pantalla, reloj)
                elif evento.key in (pygame.K_3, pygame.K_ESCAPE, pygame.K_q):
                    ejecutando = False
                elif evento.key in (pygame.K_UP, pygame.K_w):
                    indice_seleccionado = (indice_seleccionado - 1) % len(botones)
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    indice_seleccionado = (indice_seleccionado + 1) % len(botones)
                elif evento.key == pygame.K_RETURN:
                    if indice_seleccionado == 0:
                        accion = juego.iniciar_partida(pantalla, reloj)
                        if accion == "salir":
                            ejecutando = False
                    elif indice_seleccionado == 1:
                        abrir_estadisticas_y_graficos(pantalla, reloj)
                    elif indice_seleccionado == 2:
                        ejecutando = False

        # Sincronizar selección de botones
        for i, btn in enumerate(botones):
            btn.seleccionado = (i == indice_seleccionado)

        # ======================================================================
        # DIBUJADO DEL MENÚ
        # ======================================================================
        fondo.dibujar(pantalla)

        # Capa semitransparente suave sobre el centro para resaltar el menú
        filtro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        filtro.fill((12, 14, 28, 120))
        pantalla.blit(filtro, (0, 0))

        # 1. TÍTULO Y SUBTÍTULO
        surf_tit = fuente_titulo.render("RETROTRACK", True, COLOR_TITULO)
        rect_tit = surf_tit.get_rect(center=(ANCHO // 2, 70))
        surf_tit_sombra = fuente_titulo.render("RETROTRACK", True, COLOR_SUBTITULO)
        pantalla.blit(surf_tit_sombra, (rect_tit.x + 3, rect_tit.y + 3))
        pantalla.blit(surf_tit, rect_tit)

        surf_sub = fuente_subtitulo.render("¡ESQUIVA LOS OBJETOS URBANOS & ANALIZA TU RENDIMIENTO!", True, COLOR_TEXTO)
        rect_sub = surf_sub.get_rect(center=(ANCHO // 2, 120))
        pantalla.blit(surf_sub, rect_sub)

        pygame.draw.line(pantalla, COLOR_TITULO, (120, 145), (ANCHO - 120, 145), 2)

        # Récord histórico o bienvenida
        record_actual = estadisticas.obtener_mejor_puntaje()
        if record_actual > 0:
            txt_banner = f"★ Récord Histórico Actual: {record_actual} puntos ★"
            color_banner = COLOR_AMARILLO
        else:
            txt_banner = "¡Bienvenido! Todavía no hay partidas registradas. ¡Jugá tu primera partida!"
            color_banner = COLOR_VERDE
        
        surf_banner = fuente_seccion.render(txt_banner, True, color_banner)
        rect_banner = surf_banner.get_rect(center=(ANCHO // 2, 175))
        pantalla.blit(surf_banner, rect_banner)

        # 2. BOTONES
        for btn in botones:
            btn.dibujar(pantalla, fuente_botones, mouse_pos)

        # 3. PANEL DE INSTRUCCIONES BÁSICAS
        panel_y = 415
        panel_rect = pygame.Rect(centro_x, panel_y, ancho_btn, 155)
        pygame.draw.rect(pantalla, (22, 24, 46), panel_rect, border_radius=8)
        pygame.draw.rect(pantalla, (55, 65, 105), panel_rect, width=1, border_radius=8)

        tit_inst = fuente_seccion.render("--- INSTRUCCIONES PARA JUGAR ---", True, COLOR_TITULO)
        pantalla.blit(tit_inst, (panel_rect.centerx - tit_inst.get_width() // 2, panel_y + 12))

        instrucciones = [
            "- Controles: Flechas [ ← ] [ → ] o teclas [ A ] y [ D ] para mover al chico.",
            "- Objetivo: Esquivar macetas, pelotas, yunques, ladrillos y cajas de cartón.",
            "- Dificultad: La velocidad y frecuencia aumentan con el tiempo sobrevivido.",
            "- Registro: Cada partida se guarda automáticamente en historial_partidas.csv.",
            "- Análisis: Consultá tus estadísticas y gráficos con Pandas y Matplotlib."
        ]

        for idx, inst in enumerate(instrucciones):
            surf_inst = fuente_texto.render(inst, True, COLOR_TEXTO_MUTED)
            pantalla.blit(surf_inst, (panel_rect.x + 18, panel_y + 40 + idx * 21))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    print("\n[RetroTrack] ¡Gracias por jugar a RetroTrack! Programa finalizado.")
    sys.exit(0)


def abrir_estadisticas_y_graficos(pantalla: pygame.Surface, reloj: pygame.time.Clock):
    """
    Pausa momentáneamente el menú para imprimir métricas en consola
    y abrir los gráficos con Matplotlib.
    """
    fuente_aviso = pygame.font.SysFont("Consolas", 22, bold=True)
    superficie_aviso = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    superficie_aviso.fill((10, 10, 20, 230))
    pantalla.blit(superficie_aviso, (0, 0))

    txt1 = fuente_aviso.render("Abriendo Estadísticas y Gráficos...", True, COLOR_TITULO)
    txt2 = fuente_aviso.render("Cerrá la ventana de Matplotlib para volver al Menú", True, COLOR_TEXTO_MUTED)
    pantalla.blit(txt1, (ANCHO // 2 - txt1.get_width() // 2, ALTO // 2 - 30))
    pantalla.blit(txt2, (ANCHO // 2 - txt2.get_width() // 2, ALTO // 2 + 15))
    pygame.display.flip()

    estadisticas.mostrar_resumen_y_graficos()


if __name__ == "__main__":
    mostrar_menu()
