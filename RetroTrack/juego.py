# ==============================================================================
# MÓDULO: juego.py - Mecánicas de Vuelo Espacial y Esquive de Asteroides
# ==============================================================================
# En este módulo se ejecuta la misión espacial en tiempo real:
# 1. El jugador pilota su nave estelar (Astra o Nova) en la parte inferior.
# 2. Esquiva asteroides y meteoros que caen a través del campo de estrellas.
# 3. Detección precisa de colisiones con 'colliderect'.
# 4. Aumento progresivo de la velocidad y cantidad de asteroides.
# 5. Registro automático de la misión en 'historial.csv'.
# ==============================================================================

import math
import random
import time
import pygame

import historial
import personajes

# ==============================================================================
# CONSTANTES ESPACIALES
# ==============================================================================
ANCHO = 800
ALTO = 600
FPS = 60

COLOR_ESPACIO = (8, 9, 20)
COLOR_TEXTO = (245, 245, 255)
COLOR_TEXTO_MUTED = (160, 170, 200)
COLOR_CIAN = (0, 240, 255)
COLOR_MAGENTA = (255, 40, 130)
COLOR_AMARILLO = (255, 220, 40)
COLOR_ROJO_ALERTA = (255, 50, 80)
COLOR_VERDE = (60, 240, 100)


def crear_campo_estrellas():
    """Crea una lista de estrellas con posiciones y velocidades de desplazamiento."""
    estrellas = []
    for _ in range(75):
        estrellas.append({
            "x": random.randint(0, ANCHO),
            "y": random.randint(0, ALTO),
            "velocidad": random.uniform(0.8, 3.2),
            "radio": random.choice([1, 1, 2, 2, 3]),
            "brillo": random.randint(140, 255)
        })
    return estrellas


def actualizar_y_dibujar_estrellas(pantalla, estrellas):
    """Mueve las estrellas hacia abajo para crear la sensación de avance espacial."""
    pantalla.fill(COLOR_ESPACIO)
    for est in estrellas:
        est["y"] += est["velocidad"]
        if est["y"] > ALTO:
            est["y"] = 0
            est["x"] = random.randint(0, ANCHO)
        
        color = (est["brillo"], est["brillo"], est["brillo"])
        pygame.draw.circle(pantalla, color, (int(est["x"]), int(est["y"])), est["radio"])


def crear_asteroide(velocidad_base):
    """
    Crea un nuevo asteroide que cae desde la parte superior.
    Tipos de asteroides:
    0 = Asteroide Rocoso (polígono marrón/gris con cráteres)
    1 = Meteoro Incandescente (fuego espacial naranja y rojo)
    2 = Asteroide de Cristal / Hielo (cian y blanco brillante)
    3 = Chatarra Espacial / Satélite destruido (bloque metálico con luz)
    """
    tipo = random.randint(0, 3)
    ancho = random.randint(32, 44)
    alto = ancho
    x = random.randint(15, ANCHO - ancho - 15)
    y = -alto
    velocidad = velocidad_base + random.uniform(-0.4, 0.9)

    return {
        "rect": pygame.Rect(x, y, ancho, alto),
        "tipo": tipo,
        "velocidad": velocidad
    }


def dibujar_asteroide(pantalla, asteroide):
    """Dibuja el asteroide o meteoro con estilo arcade."""
    r = asteroide["rect"]
    x, y, w, h = r.x, r.y, r.width, r.height
    cx, cy = r.center

    if asteroide["tipo"] == 0:
        # 🌑 ASTEROIDE ROCOSO
        puntos_roca = [
            (cx, y), (x + w - 4, y + 8), (x + w, cy),
            (x + w - 6, y + h - 4), (cx, y + h),
            (x + 5, y + h - 8), (x, cy), (x + 6, y + 6)
        ]
        pygame.draw.polygon(pantalla, (65, 55, 60), puntos_roca)
        pygame.draw.polygon(pantalla, (115, 105, 110), puntos_roca, 2)
        # Pequeños cráteres
        pygame.draw.circle(pantalla, (45, 38, 42), (cx - 4, cy - 3), 4)
        pygame.draw.circle(pantalla, (45, 38, 42), (cx + 5, cy + 4), 3)

    elif asteroide["tipo"] == 1:
        # 🔥 METEORO INCANDESCENTE
        # Estela exterior de fuego
        pygame.draw.circle(pantalla, (255, 60, 20), (cx, cy), w // 2)
        pygame.draw.circle(pantalla, (255, 150, 30), (cx, cy), w // 2 - 3)
        # Núcleo ardiente amarillo
        pygame.draw.circle(pantalla, (255, 235, 80), (cx, cy), w // 2 - 7)

    elif asteroide["tipo"] == 2:
        # 💎 ASTEROIDE DE CRISTAL / HIELO
        puntos_cristal = [
            (cx, y + 2), (x + w - 3, cy - 4), (x + w - 5, y + h - 3),
            (cx, y + h), (x + 5, y + h - 4), (x + 3, cy)
        ]
        pygame.draw.polygon(pantalla, (25, 65, 95), puntos_cristal)
        pygame.draw.polygon(pantalla, COLOR_CIAN, puntos_cristal, 2)
        pygame.draw.line(pantalla, (200, 245, 255), (cx, y + 4), (cx, y + h - 4), 1)

    else:
        # 🛰️ CHATARRA ESPACIAL
        pygame.draw.rect(pantalla, (60, 65, 85), (x + 4, y + 4, w - 8, h - 8), border_radius=4)
        pygame.draw.rect(pantalla, (140, 150, 180), (x + 4, y + 4, w - 8, h - 8), 2, border_radius=4)
        # Luz de baliza roja
        pygame.draw.circle(pantalla, COLOR_ROJO_ALERTA, (cx, cy), 4)


def iniciar_partida(pantalla, reloj, nombre_personaje="Astra"):
    """
    Ejecuta una misión espacial de RetroTrack.
    Retorna la siguiente acción ("reiniciar", "cambiar_personaje", "menu", "salir").
    """
    fuente_hud = pygame.font.SysFont("Consolas", 18, bold=True)
    fuente_alerta = pygame.font.SysFont("Consolas", 42, bold=True)
    fuente_resumen = pygame.font.SysFont("Consolas", 22, bold=True)
    fuente_botones = pygame.font.SysFont("Consolas", 16, bold=True)

    # Inicializar la nave del jugador
    nave_ancho = personajes.ANCHO_PERSONAJE
    nave_alto = personajes.ALTO_PERSONAJE
    nave_x = (ANCHO - nave_ancho) // 2
    nave_y = ALTO - nave_alto - 25
    nave_velocidad = 7.5
    nave_rect = pygame.Rect(nave_x, nave_y, nave_ancho, nave_alto)

    # Estrellas y asteroides
    estrellas = crear_campo_estrellas()
    asteroides = []
    velocidad_base = 4.2
    intervalo_generacion_ms = 900
    ultimo_asteroide_ms = pygame.time.get_ticks()

    # Métricas de la partida
    tiempo_inicio = time.time()
    tiempo_supervivencia = 0.0
    puntuacion = 0
    asteroides_esquivados = 0
    record_actual = historial.obtener_mejor_puntuacion()

    en_mision = True
    resultado_guardado = False
    anim_propulsor = 0

    while True:
        tiempo_actual_ms = pygame.time.get_ticks()
        pos_mouse = pygame.mouse.get_pos()
        anim_propulsor += 1

        # ======================================================================
        # 1. EVENTOS
        # ======================================================================
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN:
                if not en_mision:
                    if evento.key == pygame.K_r:
                        return "reiniciar"
                    elif evento.key == pygame.K_p:
                        return "cambiar_personaje"
                    elif evento.key in (pygame.K_m, pygame.K_ESCAPE):
                        return "menu"
                    elif evento.key == pygame.K_s:
                        return "salir"
                else:
                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if not en_mision:
                    rx = (ANCHO - 500) // 2
                    ry = (ALTO - 330) // 2
                    btn_r = pygame.Rect(rx + 30, ry + 215, 210, 42)
                    btn_p = pygame.Rect(rx + 260, ry + 215, 210, 42)
                    btn_m = pygame.Rect(rx + 30, ry + 270, 210, 42)
                    btn_s = pygame.Rect(rx + 260, ry + 270, 210, 42)

                    if btn_r.collidepoint(pos_mouse):
                        return "reiniciar"
                    elif btn_p.collidepoint(pos_mouse):
                        return "cambiar_personaje"
                    elif btn_m.collidepoint(pos_mouse):
                        return "menu"
                    elif btn_s.collidepoint(pos_mouse):
                        return "salir"

        # ======================================================================
        # 2. FÍSICA Y ACTUALIZACIÓN
        # ======================================================================
        if en_mision:
            tiempo_supervivencia = time.time() - tiempo_inicio

            # Dificultad progresiva en el espacio
            nivel_dificultad = 1 + int(tiempo_supervivencia // 7)
            velocidad_actual = velocidad_base + (nivel_dificultad - 1) * 0.75
            intervalo_actual_ms = max(360, intervalo_generacion_ms - (nivel_dificultad - 1) * 70)

            # Puntuación: 10 pts/segundo + 25 pts por asteroide evadido
            puntuacion = int(tiempo_supervivencia * 10) + (asteroides_esquivados * 25)

            # Movimiento de la nave
            teclas = pygame.key.get_pressed()
            dx = 0
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                dx -= nave_velocidad
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                dx += nave_velocidad

            nave_x += dx

            # Mantener dentro de la pantalla
            if nave_x < 15:
                nave_x = 15
            elif nave_x > ANCHO - nave_ancho - 15:
                nave_x = ANCHO - nave_ancho - 15

            nave_rect.topleft = (int(nave_x), int(nave_y))

            # Generar asteroides
            if tiempo_actual_ms - ultimo_asteroide_ms >= intervalo_actual_ms:
                asteroides.append(crear_asteroide(velocidad_actual))
                ultimo_asteroide_ms = tiempo_actual_ms

            # Mover asteroides
            for ast in asteroides[:]:
                ast["rect"].y += ast["velocidad"]

                # Detección de colisión entre la nave y el asteroide
                if nave_rect.colliderect(ast["rect"]):
                    en_mision = False
                    break

                # Asteroide esquivado con éxito al salir por la parte inferior
                if ast["rect"].y > ALTO:
                    asteroides.remove(ast)
                    asteroides_esquivados += 1

        # ======================================================================
        # 3. GUARDADO AUTOMÁTICO
        # ======================================================================
        if not en_mision and not resultado_guardado:
            historial.guardar_partida(
                tiempo_segundos=tiempo_supervivencia,
                puntuacion=puntuacion,
                nombre_personaje=nombre_personaje
            )
            resultado_guardado = True

        # ======================================================================
        # 4. RENDERIZADO VISUAL
        # ======================================================================
        actualizar_y_dibujar_estrellas(pantalla, estrellas)

        # Dibujar asteroides
        for ast in asteroides:
            dibujar_asteroide(pantalla, ast)

        # Dibujar la nave estelar
        if en_mision:
            personajes.dibujar_personaje(pantalla, nave_x, nave_y, nombre_personaje, anim_propulsor)
        else:
            # Explosión de plasma espacial
            cx, cy = nave_rect.centerx, nave_rect.centery
            pygame.draw.circle(pantalla, COLOR_AMARILLO, (cx, cy), 30, 3)
            pygame.draw.circle(pantalla, COLOR_ROJO_ALERTA, (cx, cy), 18, 2)
            personajes.dibujar_personaje(pantalla, nave_x, nave_y, nombre_personaje, 0)

        # HUD superior
        pygame.draw.rect(pantalla, (12, 14, 28), (0, 0, ANCHO, 44))
        pygame.draw.line(pantalla, COLOR_CIAN, (0, 44), (ANCHO, 44), 2)

        color_nave = COLOR_MAGENTA if str(nombre_personaje).lower() in ["nova", "sara"] else COLOR_CIAN
        pantalla.blit(fuente_hud.render(f"PUNTOS: {puntuacion:05d}", True, COLOR_AMARILLO), (20, 12))
        pantalla.blit(fuente_hud.render(f"TIEMPO: {tiempo_supervivencia:.1f}s", True, COLOR_CIAN), (220, 12))
        pantalla.blit(fuente_hud.render(f"SECTOR: {nivel_dificultad if en_mision else 1}", True, COLOR_VERDE), (410, 12))
        pantalla.blit(fuente_hud.render(f"NAVE: {nombre_personaje.upper()}", True, color_nave), (600, 12))

        # Panel de GAME OVER
        if not en_mision:
            filtro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            filtro.fill((8, 10, 22, 220))
            pantalla.blit(filtro, (0, 0))

            rx = (ANCHO - 500) // 2
            ry = (ALTO - 330) // 2
            r_go = pygame.Rect(rx, ry, 500, 330)
            pygame.draw.rect(pantalla, (18, 20, 40), r_go, border_radius=12)
            pygame.draw.rect(pantalla, COLOR_ROJO_ALERTA, r_go, width=3, border_radius=12)

            t_go = fuente_alerta.render("¡MISIÓN FALLIDA!", True, COLOR_ROJO_ALERTA)
            pantalla.blit(t_go, (r_go.centerx - t_go.get_width() // 2, ry + 20))
            pantalla.blit(fuente_resumen.render(f"Puntuación Final: {puntuacion} pts", True, COLOR_AMARILLO), (rx + 60, ry + 80))
            pantalla.blit(fuente_resumen.render(f"Tiempo en Órbita: {tiempo_supervivencia:.2f} s", True, COLOR_CIAN), (rx + 60, ry + 115))

            if puntuacion > record_actual and record_actual > 0:
                t_rec = fuente_botones.render("★ ¡NUEVO RÉCORD ESPACIAL! ★", True, COLOR_VERDE)
            else:
                t_rec = fuente_botones.render("Misión registrada en datos/historial.csv", True, COLOR_TEXTO_MUTED)
            pantalla.blit(t_rec, (r_go.centerx - t_rec.get_width() // 2, ry + 160))

            # Botones
            btn_r = pygame.Rect(rx + 30, ry + 215, 210, 42)
            btn_p = pygame.Rect(rx + 260, ry + 215, 210, 42)
            btn_m = pygame.Rect(rx + 30, ry + 270, 210, 42)
            btn_s = pygame.Rect(rx + 260, ry + 270, 210, 42)

            hov_r = btn_r.collidepoint(pos_mouse)
            pygame.draw.rect(pantalla, (0, 160, 180) if hov_r else (0, 100, 120), btn_r, border_radius=6)
            pantalla.blit(fuente_botones.render("Reintentar [R]", True, COLOR_TEXTO), (btn_r.centerx - 65, btn_r.centery - 8))

            hov_p = btn_p.collidepoint(pos_mouse)
            pygame.draw.rect(pantalla, (180, 40, 100) if hov_p else (120, 25, 70), btn_p, border_radius=6)
            pantalla.blit(fuente_botones.render("Elegir Nave [P]", True, COLOR_TEXTO), (btn_p.centerx - 65, btn_p.centery - 8))

            hov_m = btn_m.collidepoint(pos_mouse)
            pygame.draw.rect(pantalla, (55, 60, 85) if hov_m else (35, 40, 60), btn_m, border_radius=6)
            pantalla.blit(fuente_botones.render("Menú Principal [M]", True, COLOR_TEXTO), (btn_m.centerx - 75, btn_m.centery - 8))

            hov_s = btn_s.collidepoint(pos_mouse)
            pygame.draw.rect(pantalla, (55, 60, 85) if hov_s else (35, 40, 60), btn_s, border_radius=6)
            pantalla.blit(fuente_botones.render("Salir del Juego [S]", True, COLOR_TEXTO_MUTED), (btn_s.centerx - 80, btn_s.centery - 8))

        pygame.display.flip()
        reloj.tick(FPS)
