# ==============================================================================
# MÓDULO: personajes.py - Naves Espaciales Jugables y Pantalla de Selección
# ==============================================================================
# Este módulo define las dos naves espaciales jugables de RetroTrack:
# 1. Astra (Nave interceptora cian - Piloto Alex).
# 2. Nova (Nave de combate magenta - Piloto Sara).
# Ambas poseen idénticas capacidades de maniobra y dimensiones de colisión,
# pero con diseños vectoriales y colores distintivos con propulsores de plasma.
# ==============================================================================

import pygame

# Dimensiones estándar del área de colisión de las naves
ANCHO_PERSONAJE = 44
ALTO_PERSONAJE = 40

# Paleta de colores espacial neón
COLOR_CIAN = (0, 240, 255)
COLOR_MAGENTA = (255, 40, 130)
COLOR_AMARILLO = (255, 220, 40)
COLOR_NARANJA = (255, 110, 20)
COLOR_BLANCO = (250, 250, 255)
COLOR_TEXTO_MUTED = (160, 170, 200)

LISTA_NAVES = [
    {
        "id": "alex",
        "nombre": "Astra",
        "piloto": "Alex",
        "tipo": "Interceptor Espacial",
        "descripcion": "Caza estelar aerodinámico con alas delta y propulsor de plasma cian.",
        "color_tema": COLOR_CIAN
    },
    {
        "id": "sara",
        "nombre": "Nova",
        "piloto": "Sara",
        "tipo": "Caza de Asalto",
        "descripcion": "Nave de combate con alas en flecha y doble propulsor magenta neón.",
        "color_tema": COLOR_MAGENTA
    }
]


def obtener_lista_personajes():
    """Devuelve la lista de naves disponibles."""
    return LISTA_NAVES


def dibujar_nave_astra(superficie, x, y, anim_propulsor=0):
    """
    Dibuja la nave espacial Astra (Cian):
    - Alas delta y morro afilado.
    - Cabina cian brillante.
    - Fuego de propulsión de plasma animado en la parte trasera.
    """
    x, y = int(x), int(y)
    w, h = ANCHO_PERSONAJE, ALTO_PERSONAJE

    # Llama del propulsor con efecto de parpadeo
    largo_fuego = 8 + (anim_propulsor % 4) * 3
    puntos_fuego = [
        (x + w // 2 - 5, y + h - 2),
        (x + w // 2 + 5, y + h - 2),
        (x + w // 2, y + h + largo_fuego)
    ]
    pygame.draw.polygon(superficie, COLOR_NARANJA, puntos_fuego)
    pygame.draw.polygon(superficie, COLOR_AMARILLO, [
        (x + w // 2 - 2, y + h - 2),
        (x + w // 2 + 2, y + h - 2),
        (x + w // 2, y + h + int(largo_fuego * 0.6))
    ])

    # Cuerpo principal de la nave (triángulo con alas aerodinámicas)
    punta = (x + w // 2, y)
    ala_izq = (x, y + h)
    centro_trasero = (x + w // 2, y + h - 6)
    ala_der = (x + w, y + h)

    # Relleno del fuselaje
    pygame.draw.polygon(superficie, (20, 45, 75), [punta, ala_izq, centro_trasero, ala_der])
    # Borde de neón cian
    pygame.draw.polygon(superficie, COLOR_CIAN, [punta, ala_izq, centro_trasero, ala_der], 2)

    # Cabina de mando
    pygame.draw.ellipse(superficie, COLOR_CIAN, (x + w // 2 - 4, y + 10, 8, 14))
    pygame.draw.ellipse(superficie, COLOR_BLANCO, (x + w // 2 - 2, y + 12, 4, 8))


def dibujar_nave_nova(superficie, x, y, anim_propulsor=0):
    """
    Dibuja la nave espacial Nova (Magenta):
    - Alas en flecha invertida angulares.
    - Cabina dorada.
    - Doble propulsor de plasma magenta animado.
    """
    x, y = int(x), int(y)
    w, h = ANCHO_PERSONAJE, ALTO_PERSONAJE

    # Doble propulsor de plasma
    largo_fuego = 7 + (anim_propulsor % 4) * 3
    # Propulsor izquierdo
    pygame.draw.polygon(superficie, COLOR_MAGENTA, [
        (x + 9, y + h - 2), (x + 15, y + h - 2), (x + 12, y + h + largo_fuego)
    ])
    # Propulsor derecho
    pygame.draw.polygon(superficie, COLOR_MAGENTA, [
        (x + w - 15, y + h - 2), (x + w - 9, y + h - 2), (x + w - 12, y + h + largo_fuego)
    ])

    # Fuselaje angular en flecha
    puntos_nave = [
        (x + w // 2, y),             # Morro
        (x + w - 4, y + h - 8),      # Punta ala derecha
        (x + w - 8, y + h),          # Borde ala derecha
        (x + w // 2 + 5, y + h - 4), # Turbina derecha
        (x + w // 2, y + h - 8),     # Centro trasero
        (x + w // 2 - 5, y + h - 4), # Turbina izquierda
        (x + 8, y + h),              # Borde ala izquierda
        (x + 4, y + h - 8)           # Punta ala izquierda
    ]

    pygame.draw.polygon(superficie, (50, 20, 45), puntos_nave)
    pygame.draw.polygon(superficie, COLOR_MAGENTA, puntos_nave, 2)

    # Cabina de mando dorada
    pygame.draw.ellipse(superficie, COLOR_AMARILLO, (x + w // 2 - 5, y + 11, 10, 13))
    pygame.draw.ellipse(superficie, COLOR_BLANCO, (x + w // 2 - 2, y + 13, 4, 7))


def dibujar_personaje(superficie, x, y, nombre_personaje, anim_paso=0, caminando=False, mirando_derecha=True):
    """
    Dibuja la nave correspondiente según el nombre ('Astra', 'Nova', 'Alex' o 'Sara').
    """
    nombre = str(nombre_personaje).lower()
    if nombre in ["nova", "sara"]:
        dibujar_nave_nova(superficie, x, y, anim_propulsor=anim_paso)
    else:
        dibujar_nave_astra(superficie, x, y, anim_propulsor=anim_paso)


def mostrar_pantalla_seleccion(pantalla, reloj, personaje_actual="Astra"):
    """
    Pantalla interactiva para elegir entre las naves Astra y Nova.
    Permite confirmar la nave para la siguiente misión espacial.
    """
    fuente_titulo = pygame.font.SysFont("Consolas", 34, bold=True)
    fuente_nombre = pygame.font.SysFont("Consolas", 24, bold=True)
    fuente_info = pygame.font.SysFont("Consolas", 15)
    fuente_boton = pygame.font.SysFont("Consolas", 18, bold=True)

    seleccionado = "Nova" if str(personaje_actual).lower() in ["nova", "sara"] else "Astra"

    tarjeta_astra = pygame.Rect(120, 140, 240, 290)
    tarjeta_nova = pygame.Rect(440, 140, 240, 290)
    boton_confirmar = pygame.Rect(200, 470, 180, 50)
    boton_volver = pygame.Rect(420, 470, 180, 50)

    anim_contador = 0
    while True:
        anim_contador += 1
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return seleccionado
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    seleccionado = "Astra"
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    seleccionado = "Nova"
                elif evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    return seleccionado
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if tarjeta_astra.collidepoint(pos_mouse):
                    seleccionado = "Astra"
                elif tarjeta_nova.collidepoint(pos_mouse):
                    seleccionado = "Nova"
                elif boton_confirmar.collidepoint(pos_mouse) or boton_volver.collidepoint(pos_mouse):
                    return seleccionado

        # Fondo espacial oscuro
        pantalla.fill((10, 12, 24))

        tit = fuente_titulo.render("SELECCIÓN DE NAVE ESPACIAL", True, COLOR_CIAN)
        pantalla.blit(tit, (pantalla.get_width() // 2 - tit.get_width() // 2, 40))

        sub = fuente_info.render("Elegí tu nave estelar para esquivar los asteroides del sector", True, COLOR_TEXTO_MUTED)
        pantalla.blit(sub, (pantalla.get_width() // 2 - sub.get_width() // 2, 85))

        # --- Tarjeta Astra ---
        es_a = (seleccionado == "Astra")
        pygame.draw.rect(pantalla, (20, 30, 55) if es_a else (16, 18, 35), tarjeta_astra, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_CIAN if es_a else (45, 55, 85), tarjeta_astra, width=3 if es_a else 1, border_radius=10)
        
        # Dibujar nave Astra en el centro
        dibujar_nave_astra(pantalla, tarjeta_astra.centerx - ANCHO_PERSONAJE // 2, tarjeta_astra.y + 45, anim_contador)
        
        t_na = fuente_nombre.render("ASTRA", True, COLOR_CIAN)
        pantalla.blit(t_na, (tarjeta_astra.centerx - t_na.get_width() // 2, tarjeta_astra.y + 115))
        pantalla.blit(fuente_info.render("Piloto: Alex", True, COLOR_BLANCO), (tarjeta_astra.centerx - 45, tarjeta_astra.y + 155))
        pantalla.blit(fuente_info.render("Interceptor Aerodinámico", True, COLOR_TEXTO_MUTED), (tarjeta_astra.centerx - 90, tarjeta_astra.y + 185))
        pantalla.blit(fuente_info.render("Propulsor de plasma cian", True, COLOR_TEXTO_MUTED), (tarjeta_astra.centerx - 85, tarjeta_astra.y + 210))
        
        if es_a:
            t_sa = fuente_boton.render("[ SELECCIONADA ]", True, COLOR_AMARILLO)
            pantalla.blit(t_sa, (tarjeta_astra.centerx - t_sa.get_width() // 2, tarjeta_astra.bottom - 38))

        # --- Tarjeta Nova ---
        es_n = (seleccionado == "Nova")
        pygame.draw.rect(pantalla, (45, 20, 40) if es_n else (16, 18, 35), tarjeta_nova, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_MAGENTA if es_n else (45, 55, 85), tarjeta_nova, width=3 if es_n else 1, border_radius=10)
        
        # Dibujar nave Nova en el centro
        dibujar_nave_nova(pantalla, tarjeta_nova.centerx - ANCHO_PERSONAJE // 2, tarjeta_nova.y + 45, anim_contador)
        
        t_nn = fuente_nombre.render("NOVA", True, COLOR_MAGENTA)
        pantalla.blit(t_nn, (tarjeta_nova.centerx - t_nn.get_width() // 2, tarjeta_nova.y + 115))
        pantalla.blit(fuente_info.render("Piloto: Sara", True, COLOR_BLANCO), (tarjeta_nova.centerx - 45, tarjeta_nova.y + 155))
        pantalla.blit(fuente_info.render("Caza de Asalto Estelar", True, COLOR_TEXTO_MUTED), (tarjeta_nova.centerx - 85, tarjeta_nova.y + 185))
        pantalla.blit(fuente_info.render("Doble propulsor magenta", True, COLOR_TEXTO_MUTED), (tarjeta_nova.centerx - 85, tarjeta_nova.y + 210))
        
        if es_n:
            t_sn = fuente_boton.render("[ SELECCIONADA ]", True, COLOR_AMARILLO)
            pantalla.blit(t_sn, (tarjeta_nova.centerx - t_sn.get_width() // 2, tarjeta_nova.bottom - 38))

        # Botones inferiores
        hov_c = boton_confirmar.collidepoint(pos_mouse)
        pygame.draw.rect(pantalla, (0, 180, 200) if hov_c else (0, 130, 150), boton_confirmar, border_radius=8)
        t_c = fuente_boton.render("Confirmar [↵]", True, COLOR_BLANCO)
        pantalla.blit(t_c, (boton_confirmar.centerx - t_c.get_width() // 2, boton_confirmar.centery - t_c.get_height() // 2))

        hov_v = boton_volver.collidepoint(pos_mouse)
        pygame.draw.rect(pantalla, (60, 65, 90) if hov_v else (40, 45, 70), boton_volver, border_radius=8)
        t_v = fuente_boton.render("Volver [ESC]", True, COLOR_BLANCO)
        pantalla.blit(t_v, (boton_volver.centerx - t_v.get_width() // 2, boton_volver.centery - t_v.get_height() // 2))

        pygame.display.flip()
        reloj.tick(60)
