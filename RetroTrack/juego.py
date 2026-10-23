"""
==============================================================================
Módulo del Videojuego - RetroTrack (Temática Urbana)
==============================================================================
En esta versión, el protagonista es un chico que camina por la vereda de la ciudad
y debe esquivar diferentes objetos cotidianos que caen desde los balcones de
los edificios (macetas con plantas, pelotas, yunques, ladrillos y cajas de cartón).

Mantiene las mecánicas obligatorias:
- Bucle principal a 60 FPS con Pygame.
- Controles: Flechas [←] [→] o teclas [A] y [D].
- Personaje con animación de caminata dibujado con formas geométricas vectoriales.
- Varios tipos de objetos con diseños y colores distintivos.
- Dificultad progresiva en base al tiempo sobrevivido.
- Detección precisa de colisiones con 'colliderect'.
- Registro automático en CSV a través del módulo 'estadisticas.py'.
==============================================================================
"""

import math
import random
import time
import pygame
import estadisticas

# ==============================================================================
# CONSTANTES VISUALES Y GEOMETRÍA
# ==============================================================================
ANCHO = 800
ALTO = 600
FPS = 60
POS_PISO = 540  # Nivel del suelo / vereda

# Paleta de colores urbanos / retro
COLOR_CIELO = (18, 16, 38)            # Azul violeta noche urbana
COLOR_EDIFICIO_LEJOS = (28, 25, 52)   # Silueta de edificios traseros
COLOR_EDIFICIO_CERCA = (40, 36, 72)   # Silueta de edificios delanteros
COLOR_VENTANA_LUZ = (255, 230, 110)   # Ventanas encendidas
COLOR_VEREDA = (70, 75, 90)           # Baldosas de la vereda
COLOR_CORDON = (130, 135, 150)        # Cordón de la vereda
COLOR_CALLE = (35, 38, 48)            # Asfalto inferior
COLOR_LINEAS_HUD = (50, 60, 100)
COLOR_TEXTO = (245, 245, 255)
COLOR_TEXTO_MUTED = (165, 175, 205)
COLOR_AMARILLO = (255, 220, 40)
COLOR_ROJO_ALERTA = (255, 60, 80)
COLOR_CIAN = (0, 240, 255)
COLOR_VERDE = (60, 240, 100)


# ==============================================================================
# CLASE: FONDO URBANO (CIUDAD CON SILUETAS Y VENTANAS)
# ==============================================================================
class FondoCiudad:
    """
    Genera un paisaje urbano procedural con cielo nocturno, luna, edificios
    con ventanitas iluminadas y la vereda por donde corre el protagonista.
    """
    def __init__(self):
        # Generar edificios de fondo (capa lejana y cercana)
        self.edificios_lejos = []
        x = 0
        while x < ANCHO:
            w = random.randint(55, 95)
            h = random.randint(180, 320)
            self.edificios_lejos.append((x, POS_PISO - h, w, h))
            x += w - 5

        self.edificios_cerca = []
        x = 0
        while x < ANCHO:
            w = random.randint(65, 110)
            h = random.randint(120, 240)
            # Lista de ventanitas encendidas
            ventanas = []
            for vx in range(x + 10, x + w - 10, 18):
                for vy in range(POS_PISO - h + 15, POS_PISO - 15, 28):
                    if random.random() > 0.45:
                        ventanas.append((vx, vy))
            self.edificios_cerca.append((x, POS_PISO - h, w, h, ventanas))
            x += w - 5

        # Estrellas y luna
        self.estrellas = [(random.randint(0, ANCHO), random.randint(10, 220)) for _ in range(40)]

    def dibujar(self, superficie: pygame.Surface):
        # 1. Cielo
        superficie.fill(COLOR_CIELO)

        # 2. Estrellas tenues y luna
        for ex, ey in self.estrellas:
            superficie.set_at((ex, ey), (190, 190, 220))

        # Luna retro
        pygame.draw.circle(superficie, (255, 250, 210), (700, 90), 32)
        pygame.draw.circle(superficie, COLOR_CIELO, (712, 85), 28)

        # 3. Edificios de fondo
        for x, y, w, h in self.edificios_lejos:
            pygame.draw.rect(superficie, COLOR_EDIFICIO_LEJOS, (x, y, w, h))

        # 4. Edificios del primer plano con ventanas
        for x, y, w, h, ventanas in self.edificios_cerca:
            pygame.draw.rect(superficie, COLOR_EDIFICIO_CERCA, (x, y, w, h))
            pygame.draw.rect(superficie, (55, 50, 95), (x, y, w, h), 1)
            for vx, vy in ventanas:
                pygame.draw.rect(superficie, COLOR_VENTANA_LUZ, (vx, vy, 9, 13))

        # 5. Vereda y asfalto inferior
        pygame.draw.rect(superficie, COLOR_VEREDA, (0, POS_PISO, ANCHO, 28))
        pygame.draw.line(superficie, COLOR_CORDON, (0, POS_PISO), (ANCHO, POS_PISO), 2)
        pygame.draw.line(superficie, (95, 100, 120), (0, POS_PISO + 28), (ANCHO, POS_PISO + 28), 2)
        pygame.draw.rect(superficie, COLOR_CALLE, (0, POS_PISO + 30, ANCHO, ALTO - POS_PISO - 30))

        # Marcas de baldosas
        for bx in range(0, ANCHO, 40):
            pygame.draw.line(superficie, (60, 65, 80), (bx, POS_PISO), (bx, POS_PISO + 28), 1)


# ==============================================================================
# CLASE: JUGADOR (EL CHICO)
# ==============================================================================
class Jugador:
    """
    Representa al chico que corre por la vereda esquivando objetos.
    Se dibuja con figuras geométricas:
    - Cabeza con gorra roja/visera.
    - Ojos y rostro.
    - Remera azul deportiva.
    - Pantalón y zapatillas con animación de zancadas al caminar.
    """
    def __init__(self, x: float, y: float):
        self.ancho = 32
        self.alto = 54
        self.x = x
        self.y = y
        self.velocidad = 7.5
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
        # Variables de animación
        self.caminando = False
        self.anim_paso = 0
        self.mirando_derecha = True

    def mover(self, teclas):
        dx = 0
        self.caminando = False

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= self.velocidad
            self.mirando_derecha = False
            self.caminando = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += self.velocidad
            self.mirando_derecha = True
            self.caminando = True

        self.x += dx

        # Mantener dentro de los bordes laterales
        if self.x < 15:
            self.x = 15
        elif self.x > ANCHO - self.ancho - 15:
            self.x = ANCHO - self.ancho - 15

        self.rect.topleft = (int(self.x), int(self.y))

        if self.caminando:
            self.anim_paso += 1
        else:
            self.anim_paso = 0

    def dibujar(self, superficie: pygame.Surface):
        x = int(self.x)
        y = int(self.y)

        # Colores del personaje
        color_piel = (255, 218, 185)       # Piel clara
        color_gorra = (230, 45, 50)         # Gorra roja
        color_remera = (40, 140, 240)       # Remera azul
        color_pantalon = (45, 55, 80)       # Pantalón azul marino
        color_zapatillas = (245, 245, 245)  # Zapatillas blancas

        # 1. PIERNAS Y ZAPATILLAS (con animación de balanceo si camina)
        offset_pierna = math.sin(self.anim_paso * 0.35) * 6 if self.caminando else 0

        # Pierna izquierda
        p1_x = x + 8 - offset_pierna
        pygame.draw.line(superficie, color_pantalon, (x + 10, y + 36), (p1_x, y + 48), 4)
        pygame.draw.rect(superficie, color_zapatillas, (p1_x - 3, y + 47, 8, 5), border_radius=2)

        # Pierna derecha
        p2_x = x + 20 + offset_pierna
        pygame.draw.line(superficie, color_pantalon, (x + 22, y + 36), (p2_x, y + 48), 4)
        pygame.draw.rect(superficie, color_zapatillas, (p2_x - 2, y + 47, 8, 5), border_radius=2)

        # 2. TORSO / REMERA
        torso_rect = pygame.Rect(x + 6, y + 18, 20, 18)
        pygame.draw.rect(superficie, color_remera, torso_rect, border_radius=4)
        # Detalle de cuello blanco
        pygame.draw.rect(superficie, (255, 255, 255), (x + 12, y + 18, 8, 3))

        # Brazos
        offset_brazo = -offset_pierna
        pygame.draw.line(superficie, color_remera, (x + 6, y + 21), (x + 3 - offset_brazo, y + 30), 4)
        pygame.draw.circle(superficie, color_piel, (int(x + 3 - offset_brazo), int(y + 31)), 3)
        pygame.draw.line(superficie, color_remera, (x + 26, y + 21), (x + 29 + offset_brazo, y + 30), 4)
        pygame.draw.circle(superficie, color_piel, (int(x + 29 + offset_brazo), int(y + 31)), 3)

        # 3. CABEZA
        cabeza_centro = (x + 16, y + 10)
        pygame.draw.circle(superficie, color_piel, cabeza_centro, 9)

        # Ojos mirando en la dirección del movimiento
        ojo_x = cabeza_centro[0] + (3 if self.mirando_derecha else -3)
        pygame.draw.circle(superficie, (20, 20, 40), (ojo_x, y + 9), 2)

        # 4. GORRA CON VISERA
        # Copa de la gorra
        pygame.draw.ellipse(superficie, color_gorra, (x + 7, y - 1, 18, 10))
        # Visera apuntando a donde mira
        if self.mirando_derecha:
            pygame.draw.polygon(superficie, color_gorra, [(x + 16, y + 5), (x + 27, y + 5), (x + 25, y + 8), (x + 16, y + 7)])
        else:
            pygame.draw.polygon(superficie, color_gorra, [(x + 16, y + 5), (x + 5, y + 5), (x + 7, y + 8), (x + 16, y + 7)])


# ==============================================================================
# CLASE: OBSTÁCULO (OBJETOS URBANOS QUE CAEN)
# ==============================================================================
class Obstaculo:
    """
    Representa uno de los distintos objetos que caen desde lo alto:
    0 = Maceta con planta (terracota + hojas verdes)
    1 = Pelota de básquetbol / fútbol
    2 = Yunque / Pesa pesada de metal
    3 = Ladrillo de obra
    4 = Caja de cartón de encomienda
    """
    NOMBRES_OBJETOS = ["Maceta", "Pelota", "Yunque", "Ladrillo", "Caja"]

    def __init__(self, velocidad_base: float):
        self.tipo = random.randint(0, 4)
        self.ancho = 34
        self.alto = 34

        # Posición horizontal aleatoria
        self.x = random.randint(20, ANCHO - self.ancho - 20)
        self.y = -self.alto

        # Velocidad de caída
        self.velocidad = velocidad_base + random.uniform(-0.4, 0.9)
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def actualizar(self):
        self.y += self.velocidad
        self.rect.topleft = (int(self.x), int(self.y))

    def fuera_de_pantalla(self) -> bool:
        """Determina si el objeto tocó el piso de la vereda."""
        return self.y >= POS_PISO - 6

    def dibujar(self, superficie: pygame.Surface):
        x, y = int(self.x), int(self.y)
        w, h = self.ancho, self.alto

        if self.tipo == 0:
            # 🪴 MACETA CON PLANTA
            color_maceta = (195, 90, 45)
            # Maceta en forma de trapecio
            pygame.draw.polygon(superficie, color_maceta, [
                (x + 4, y + 12), (x + w - 4, y + 12),
                (x + w - 8, y + h), (x + 8, y + h)
            ])
            # Borde superior de la maceta
            pygame.draw.rect(superficie, (170, 75, 35), (x + 2, y + 10, w - 4, 5), border_radius=2)
            # Hojitas verdes brotando arriba
            pygame.draw.circle(superficie, (45, 185, 65), (x + 12, y + 6), 6)
            pygame.draw.circle(superficie, (60, 215, 80), (x + 22, y + 6), 6)
            pygame.draw.circle(superficie, (255, 230, 80), (x + 17, y + 4), 3)

        elif self.tipo == 1:
            # 🏀 PELOTA DEPORTIVA
            color_pelota = (255, 110, 20)
            centro = (x + w // 2, y + h // 2)
            radio = w // 2 - 2
            pygame.draw.circle(superficie, color_pelota, centro, radio)
            pygame.draw.circle(superficie, (30, 30, 30), centro, radio, 2)
            # Líneas de la pelota
            pygame.draw.line(superficie, (30, 30, 30), (centro[0] - radio, centro[1]), (centro[0] + radio, centro[1]), 2)
            pygame.draw.arc(superficie, (30, 30, 30), (centro[0] - radio + 2, centro[1] - radio, radio * 2 - 4, radio * 2), 0, math.pi, 2)

        elif self.tipo == 2:
            # ⚙️ YUNQUE METÁLICO PESADO
            color_metal = (110, 115, 130)
            color_borde = (60, 65, 75)
            # Parte superior ancha
            pygame.draw.rect(superficie, color_metal, (x + 2, y + 8, w - 4, 9), border_radius=2)
            # Cuello central
            pygame.draw.rect(superficie, color_metal, (x + 10, y + 17, w - 20, 8))
            # Base pesada
            pygame.draw.rect(superficie, color_metal, (x + 5, y + 25, w - 10, 9), border_radius=2)
            # Brillo metálico
            pygame.draw.line(superficie, (180, 185, 205), (x + 4, y + 9), (x + w - 6, y + 9), 1)

        elif self.tipo == 3:
            # 🧱 LADRILLO DE CONSTRUCCIÓN
            color_ladrillo = (185, 60, 45)
            pygame.draw.rect(superficie, color_ladrillo, (x + 3, y + 8, w - 6, h - 16), border_radius=3)
            pygame.draw.rect(superficie, (130, 35, 25), (x + 3, y + 8, w - 6, h - 16), 2, border_radius=3)
            # Orificios típicos de ladrillo hueco
            for ox in [x + 8, x + 16, x + 24]:
                pygame.draw.rect(superficie, (90, 20, 15), (ox, y + 14, 4, 6))

        else:
            # 📦 CAJA DE CARTÓN
            color_carton = (195, 150, 95)
            pygame.draw.rect(superficie, color_carton, (x + 3, y + 3, w - 6, h - 6), border_radius=2)
            pygame.draw.rect(superficie, (140, 100, 60), (x + 3, y + 3, w - 6, h - 6), 2, border_radius=2)
            # Cinta de embalaje
            pygame.draw.line(superficie, (150, 105, 55), (x + w // 2, y + 3), (x + w // 2, y + h - 3), 3)


# ==============================================================================
# BUCLE PRINCIPAL DE LA PARTIDA
# ==============================================================================
def iniciar_partida(pantalla: pygame.Surface, reloj: pygame.time.Clock) -> str:
    """
    Ejecuta una partida completa del juego del chico esquivando objetos.
    
    Retorna:
        str: 'menu' si vuelve al menú principal, o 'salir' si cierra el juego.
    """
    # Fuentes del sistema
    fuente_hud = pygame.font.SysFont("Consolas", 18, bold=True)
    fuente_grande = pygame.font.SysFont("Consolas", 38, bold=True)
    fuente_subtitulo = pygame.font.SysFont("Consolas", 22, bold=True)
    fuente_instruccion = pygame.font.SysFont("Consolas", 16)

    # Inicializar objetos de la escena urbana
    fondo = FondoCiudad()
    # Ubicar al chico parado en la vereda
    jugador = Jugador(ANCHO / 2 - 16, POS_PISO - 50)
    obstaculos: list[Obstaculo] = []

    # Variables de tiempo y puntaje
    tiempo_inicio = time.time()
    tiempo_supervivencia = 0.0
    puntaje = 0
    objetos_esquivados = 0

    # Récord histórico cargado desde el CSV
    record_historico = estadisticas.obtener_mejor_puntaje()

    # Dificultad progresiva
    velocidad_base = 4.2
    intervalo_generacion_ms = 920
    ultimo_obstaculo_ms = pygame.time.get_ticks()

    partida_activa = True
    en_game_over = False
    resultado_guardado = False

    while True:
        tiempo_actual_ms = pygame.time.get_ticks()

        # ======================================================================
        # 1. GESTIÓN DE EVENTOS
        # ======================================================================
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN:
                if en_game_over:
                    # [R] Reiniciar partida
                    if evento.key == pygame.K_r:
                        return iniciar_partida(pantalla, reloj)
                    # [M] o [ENTER] Volver al menú
                    elif evento.key in (pygame.K_m, pygame.K_RETURN, pygame.K_SPACE):
                        return "menu"
                    # [Q] o [ESC] Salir
                    elif evento.key in (pygame.K_q, pygame.K_ESCAPE):
                        return "salir"
                else:
                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

        # ======================================================================
        # 2. ACTUALIZACIÓN DEL JUEGO
        # ======================================================================
        if partida_activa:
            tiempo_supervivencia = time.time() - tiempo_inicio

            # Aumento de dificultad por tiempo:
            # Cada 7 segundos aumenta el nivel, velocidad y frecuencia
            nivel_dificultad = 1 + int(tiempo_supervivencia // 7)
            velocidad_actual = velocidad_base + (nivel_dificultad - 1) * 0.75
            intervalo_actual_ms = max(380, intervalo_generacion_ms - (nivel_dificultad - 1) * 70)

            # Puntaje: 10 pts por segundo + 25 pts por objeto esquivado
            puntaje = int(tiempo_supervivencia * 10) + (objetos_esquivados * 25)

            # Mover personaje
            teclas = pygame.key.get_pressed()
            jugador.mover(teclas)

            # Generar nuevos objetos desde los balcones
            if tiempo_actual_ms - ultimo_obstaculo_ms >= intervalo_actual_ms:
                obstaculos.append(Obstaculo(velocidad_actual))
                ultimo_obstaculo_ms = tiempo_actual_ms

            # Actualizar y verificar colisiones
            for obs in obstaculos[:]:
                obs.actualizar()

                # Colisión entre el chico y el objeto
                if jugador.rect.colliderect(obs.rect):
                    partida_activa = False
                    en_game_over = True
                    break

                # Si el objeto llegó al suelo sin tocar al chico
                if obs.fuera_de_pantalla():
                    obstaculos.remove(obs)
                    objetos_esquivados += 1

        # ======================================================================
        # 3. GUARDADO AUTOMÁTICO EN CSV POST-COLISIÓN
        # ======================================================================
        if en_game_over and not resultado_guardado:
            estadisticas.guardar_partida(
                duracion_segundos=tiempo_supervivencia,
                puntaje=puntaje
            )
            resultado_guardado = True

        # ======================================================================
        # 4. RENDERIZADO VISUAL
        # ======================================================================
        # Fondo urbano
        fondo.dibujar(pantalla)

        # Dibujar objetos cayendo
        for obs in obstaculos:
            obs.dibujar(pantalla)

        # Dibujar al chico si sigue en pie o efecto de golpe si perdió
        if partida_activa:
            jugador.dibujar(pantalla)
        else:
            # Efecto cómico retro tipo "¡OUCH!" con círculos de impacto
            cx, cy = jugador.rect.centerx, jugador.rect.centery
            pygame.draw.circle(pantalla, COLOR_AMARILLO, (cx, cy), 24, 3)
            pygame.draw.circle(pantalla, COLOR_ROJO_ALERTA, (cx, cy), 14, 2)
            jugador.dibujar(pantalla)

        # ----------------------------------------------------------------------
        # Barra superior HUD
        # ----------------------------------------------------------------------
        pygame.draw.rect(pantalla, (20, 20, 38), (0, 0, ANCHO, 42))
        pygame.draw.line(pantalla, COLOR_LINEAS_HUD, (0, 42), (ANCHO, 42), 2)

        txt_pts = fuente_hud.render(f"PUNTOS: {puntaje:05d}", True, COLOR_AMARILLO)
        txt_tiempo = fuente_hud.render(f"TIEMPO: {tiempo_supervivencia:.1f}s", True, COLOR_CIAN)
        txt_nivel = fuente_hud.render(f"NIVEL: {nivel_dificultad if partida_activa else 1}", True, COLOR_VERDE)
        txt_record = fuente_hud.render(f"RÉCORD: {max(record_historico, puntaje):05d}", True, COLOR_TEXTO_MUTED)

        pantalla.blit(txt_pts, (20, 12))
        pantalla.blit(txt_tiempo, (220, 12))
        pantalla.blit(txt_nivel, (410, 12))
        pantalla.blit(txt_record, (600, 12))

        # ----------------------------------------------------------------------
        # Pantalla de GAME OVER
        # ----------------------------------------------------------------------
        if en_game_over:
            superficie_oscura = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            superficie_oscura.fill((12, 14, 28, 215))
            pantalla.blit(superficie_oscura, (0, 0))

            recuadro_ancho, recuadro_alto = 520, 340
            rx = (ANCHO - recuadro_ancho) // 2
            ry = (ALTO - recuadro_alto) // 2
            pygame.draw.rect(pantalla, (25, 26, 48), (rx, ry, recuadro_ancho, recuadro_alto), border_radius=10)
            pygame.draw.rect(pantalla, COLOR_ROJO_ALERTA, (rx, ry, recuadro_ancho, recuadro_alto), width=3, border_radius=10)

            texto_go = fuente_grande.render("¡GAME OVER!", True, COLOR_ROJO_ALERTA)
            pantalla.blit(texto_go, (ANCHO // 2 - texto_go.get_width() // 2, ry + 25))

            texto_res_pts = fuente_subtitulo.render(f"Puntaje Final: {puntaje} pts", True, COLOR_AMARILLO)
            texto_res_tiempo = fuente_subtitulo.render(f"Tiempo Sobrevivido: {tiempo_supervivencia:.2f} s", True, COLOR_CIAN)
            pantalla.blit(texto_res_pts, (ANCHO // 2 - texto_res_pts.get_width() // 2, ry + 85))
            pantalla.blit(texto_res_tiempo, (ANCHO // 2 - texto_res_tiempo.get_width() // 2, ry + 120))

            if puntaje > record_historico and record_historico > 0:
                texto_nuevo_rec = fuente_subtitulo.render("★ ¡NUEVO RÉCORD HISTÓRICO! ★", True, COLOR_VERDE)
                pantalla.blit(texto_nuevo_rec, (ANCHO // 2 - texto_nuevo_rec.get_width() // 2, ry + 160))
            else:
                texto_guardado = fuente_instruccion.render("Partida registrada en historial_partidas.csv", True, COLOR_TEXTO_MUTED)
                pantalla.blit(texto_guardado, (ANCHO // 2 - texto_guardado.get_width() // 2, ry + 165))

            pygame.draw.line(pantalla, COLOR_LINEAS_HUD, (rx + 30, ry + 205), (rx + recuadro_ancho - 30, ry + 205), 1)

            opcion1 = fuente_instruccion.render("[ R ]  Jugar de nuevo", True, COLOR_TEXTO)
            opcion2 = fuente_instruccion.render("[ M ] o [ ENTER ]  Volver al Menú Principal", True, COLOR_TEXTO)
            opcion3 = fuente_instruccion.render("[ ESC ] o [ Q ]  Salir del Juego", True, COLOR_TEXTO_MUTED)

            pantalla.blit(opcion1, (ANCHO // 2 - opcion1.get_width() // 2, ry + 225))
            pantalla.blit(opcion2, (ANCHO // 2 - opcion2.get_width() // 2, ry + 255))
            pantalla.blit(opcion3, (ANCHO // 2 - opcion3.get_width() // 2, ry + 285))

        pygame.display.flip()
        reloj.tick(FPS)
