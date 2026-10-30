# ==============================================================================
# MÓDULO: menu.py - Menú Principal y Navegación de RetroTrack Espacial
# ==============================================================================
# Gestiona la pantalla inicial del juego en el espacio:
# 1. Título retro neón con estrellas en movimiento.
# 2. Nave estelar actualmente seleccionada (Astra o Nova).
# 3. Botones: Comenzar Misión, Elegir Nave, Estadísticas y Salir.
# 4. Acceso directo a la pantalla de estadísticas con gráfico integrado.
# ==============================================================================

import pygame
import historial
import personajes
import estadisticas

ANCHO = 800
ALTO = 600
FPS = 60

COLOR_ESPACIO = (8, 9, 20)
COLOR_CIAN = (0, 240, 255)
COLOR_MAGENTA = (255, 40, 130)
COLOR_TITULO = (0, 240, 255)
COLOR_TITULO_SOMBRA = (255, 40, 130)
COLOR_TEXTO = (245, 245, 255)
COLOR_TEXTO_MUTED = (160, 170, 205)
COLOR_AMARILLO = (255, 220, 40)
COLOR_BOTON = (20, 24, 46)
COLOR_BOTON_HOVER = (38, 44, 82)


def crear_boton(x, y, ancho, alto, texto, tecla_atajo):
    return {"rect": pygame.Rect(x, y, ancho, alto), "texto": texto, "tecla": tecla_atajo}


def dibujar_boton(superficie, boton, fuente, mouse_pos):
    esta_sobre = boton["rect"].collidepoint(mouse_pos)
    color_fondo = COLOR_BOTON_HOVER if esta_sobre else COLOR_BOTON
    color_borde = COLOR_TITULO if esta_sobre else (50, 60, 100)

    pygame.draw.rect(superficie, color_fondo, boton["rect"], border_radius=8)
    pygame.draw.rect(superficie, color_borde, boton["rect"], width=2 if esta_sobre else 1, border_radius=8)

    color_texto = COLOR_AMARILLO if esta_sobre else COLOR_TEXTO
    txt_surf = fuente.render(f"{boton['tecla']}  {boton['texto']}", True, color_texto)
    superficie.blit(txt_surf, txt_surf.get_rect(center=boton["rect"].center))


def mostrar_menu_principal(pantalla, reloj, personaje_actual="Astra"):
    """
    Bucle del Menú Principal.
    Retorna (accion, nave_seleccionada), donde accion es "jugar" o "salir".
    """
    fuente_titulo = pygame.font.SysFont("Consolas", 46, bold=True)
    fuente_subtitulo = pygame.font.SysFont("Consolas", 17, bold=True)
    fuente_botones = pygame.font.SysFont("Consolas", 18, bold=True)
    fuente_seccion = pygame.font.SysFont("Consolas", 15, bold=True)
    fuente_texto = pygame.font.SysFont("Consolas", 13)

    nave_seleccionada = "Nova" if str(personaje_actual).lower() in ["nova", "sara"] else "Astra"

    # Estrellas de fondo para el menú
    import random
    estrellas_menu = [{"x": random.randint(0, ANCHO), "y": random.randint(0, ALTO), "v": random.uniform(0.5, 1.8)} for _ in range(50)]

    ancho_btn, alto_btn = 460, 48
    centro_x = (ANCHO - ancho_btn) // 2
    botones = [
        crear_boton(centro_x, 195, ancho_btn, alto_btn, "COMENZAR MISIÓN ESPACIAL", "[ 1 ]"),
        crear_boton(centro_x, 252, ancho_btn, alto_btn, "ELEGIR NAVE (Astra / Nova)", "[ 2 ]"),
        crear_boton(centro_x, 309, ancho_btn, alto_btn, "CONSULTAR ESTADÍSTICAS Y GRÁFICO", "[ 3 ]"),
        crear_boton(centro_x, 366, ancho_btn, alto_btn, "SALIR DEL JUEGO", "[ 4 ]")
    ]

    while True:
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir", nave_seleccionada

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botones[0]["rect"].collidepoint(pos_mouse):
                    return "jugar", nave_seleccionada
                elif botones[1]["rect"].collidepoint(pos_mouse):
                    nave_seleccionada = personajes.mostrar_pantalla_seleccion(pantalla, reloj, nave_seleccionada)
                elif botones[2]["rect"].collidepoint(pos_mouse):
                    # Abre la pantalla de estadísticas integrada
                    estadisticas.mostrar_pantalla_estadisticas(pantalla, reloj)
                elif botones[3]["rect"].collidepoint(pos_mouse):
                    return "salir", nave_seleccionada

            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_1, pygame.K_RETURN, pygame.K_SPACE):
                    return "jugar", nave_seleccionada
                elif evento.key in (pygame.K_2, pygame.K_p):
                    nave_seleccionada = personajes.mostrar_pantalla_seleccion(pantalla, reloj, nave_seleccionada)
                elif evento.key in (pygame.K_3, pygame.K_e):
                    estadisticas.mostrar_pantalla_estadisticas(pantalla, reloj)
                elif evento.key in (pygame.K_4, pygame.K_ESCAPE, pygame.K_s, pygame.K_q):
                    return "salir", nave_seleccionada

        # Actualizar estrellas del menú
        pantalla.fill(COLOR_ESPACIO)
        for est in estrellas_menu:
            est["y"] += est["v"]
            if est["y"] > ALTO:
                est["y"] = 0
                est["x"] = random.randint(0, ANCHO)
            pygame.draw.circle(pantalla, (200, 205, 230), (int(est["x"]), int(est["y"])), 1)

        # 1. TÍTULO NEÓN CON SOMBRA
        surf_sombra = fuente_titulo.render("RETROTRACK", True, COLOR_TITULO_SOMBRA)
        surf_titulo = fuente_titulo.render("RETROTRACK", True, COLOR_TITULO)
        pantalla.blit(surf_sombra, (ANCHO // 2 - surf_titulo.get_width() // 2 + 3, 33))
        pantalla.blit(surf_titulo, (ANCHO // 2 - surf_titulo.get_width() // 2, 30))

        surf_sub = fuente_subtitulo.render("MISIÓN ESPACIAL EN 2D & EVOLUCIÓN ESTADÍSTICA", True, COLOR_TEXTO)
        pantalla.blit(surf_sub, (ANCHO // 2 - surf_sub.get_width() // 2, 85))
        pygame.draw.line(pantalla, COLOR_TITULO, (140, 115), (ANCHO - 140, 115), 2)

        # 2. RÉCORD Y NAVE ACTIVA
        record_historico = historial.obtener_mejor_puntuacion()
        txt_record = f"★ Récord Espacial: {record_historico} pts ★" if record_historico > 0 else "¡Bienvenido! Iniciá tu primera misión para inaugurar el récord."
        surf_rec = fuente_seccion.render(txt_record, True, COLOR_AMARILLO)
        pantalla.blit(surf_rec, (ANCHO // 2 - surf_rec.get_width() // 2, 130))

        color_nave = COLOR_MAGENTA if nave_seleccionada == "Nova" else COLOR_CIAN
        txt_nave = f"Nave Activa: {nave_seleccionada.upper()}  (Presioná [2] para cambiar)"
        surf_nave = fuente_seccion.render(txt_nave, True, color_nave)
        pantalla.blit(surf_nave, (ANCHO // 2 - surf_nave.get_width() // 2, 160))

        # 3. BOTONES
        for btn in botones:
            dibujar_boton(pantalla, btn, fuente_botones, pos_mouse)

        # 4. INSTRUCCIONES
        panel_y = 430
        panel_rect = pygame.Rect(centro_x, panel_y, ancho_btn, 140)
        pygame.draw.rect(pantalla, (16, 18, 36), panel_rect, border_radius=8)
        pygame.draw.rect(pantalla, (45, 55, 95), panel_rect, width=1, border_radius=8)

        tit_inst = fuente_seccion.render("--- INSTRUCCIONES DE VUELO ---", True, COLOR_TITULO)
        pantalla.blit(tit_inst, (panel_rect.centerx - tit_inst.get_width() // 2, panel_y + 10))

        instrucciones = [
            "• Controles: Flechas [ ← ] [ → ] o teclas [ A ] y [ D ] para maniobrar.",
            "• Objetivo: Esquivar los asteroides y meteoros que caen en el sector.",
            "• Dificultad: La velocidad de caída se incrementa con el tiempo.",
            "• Gráficos: Presioná [ 3 ] para ver tu evolución con Matplotlib."
        ]
        for i, inst in enumerate(instrucciones):
            surf_i = fuente_texto.render(inst, True, COLOR_TEXTO_MUTED)
            pantalla.blit(surf_i, (panel_rect.x + 18, panel_y + 36 + i * 23))

        pygame.display.flip()
        reloj.tick(FPS)
