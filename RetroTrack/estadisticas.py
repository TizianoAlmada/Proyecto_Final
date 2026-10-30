# ==============================================================================
# MÓDULO: estadisticas.py - Procesamiento de Datos y Pantalla de Gráficos
# ==============================================================================
# Este módulo se encarga de:
# 1. Leer las partidas guardadas usando 'historial.py'.
# 2. Calcular estadísticas descriptivas (total, promedio, récord).
# 3. Generar un gráfico visual con Matplotlib (backend Agg, 100% compatible con .exe).
# 4. Mostrar el gráfico directamente dentro de una pantalla integrada en Pygame.
# ==============================================================================

import os
import tempfile
import pygame

# Configurar carpeta temporal para Matplotlib
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib_retrotrack"))

# Forzar backend 'Agg' para que Matplotlib genere imágenes sin depender de ventanas externas
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import historial

NOMBRE_IMAGEN_GRAFICO = "estadisticas.png"

# Colores para la pantalla de estadísticas en Pygame
COLOR_FONDO = (10, 12, 24)
COLOR_CIAN = (0, 240, 255)
COLOR_MAGENTA = (255, 40, 130)
COLOR_AMARILLO = (255, 220, 40)
COLOR_TEXTO = (245, 245, 255)
COLOR_TEXTO_MUTED = (160, 170, 205)


def obtener_ruta_imagen_grafico():
    """Retorna la ruta completa donde se guarda estadisticas.png."""
    carpeta = historial.obtener_carpeta_datos()
    return os.path.join(carpeta, NOMBRE_IMAGEN_GRAFICO)


def obtener_resumen_estadisticas():
    """Calcula un resumen descriptivo del rendimiento."""
    partidas = historial.leer_partidas()
    
    if not partidas:
        return {
            "hay_datos": False,
            "total_partidas": 0,
            "puntuacion_promedio": 0,
            "tiempo_promedio": 0,
            "mejor_puntuacion": 0,
            "mejor_tiempo": 0,
            "mensaje": "Aún no hay suficientes partidas registradas."
        }

    total = len(partidas)
    suma_puntos = sum(p["puntuacion"] for p in partidas)
    suma_tiempos = sum(p["tiempo_segundos"] for p in partidas)

    return {
        "hay_datos": True,
        "total_partidas": total,
        "puntuacion_promedio": round(suma_puntos / total, 1),
        "tiempo_promedio": round(suma_tiempos / total, 1),
        "mejor_puntuacion": max(p["puntuacion"] for p in partidas),
        "mejor_tiempo": max(p["tiempo_segundos"] for p in partidas),
        "primera_puntuacion": partidas[0]["puntuacion"],
        "ultima_puntuacion": partidas[-1]["puntuacion"],
        "diferencia": partidas[-1]["puntuacion"] - partidas[0]["puntuacion"]
    }


def generar_grafico_estadisticas():
    """
    Genera el archivo 'estadisticas.png' con Matplotlib usando datos reales de historial.csv.
    Retorna (True, ruta) si hay datos o (False, ruta) si está vacío.
    """
    partidas = historial.leer_partidas()
    ruta_imagen = obtener_ruta_imagen_grafico()

    plt.close("all")

    # Tamaño optimizado para entrar en la ventana de 800x600 de Pygame (740x360 px)
    fig, ax = plt.subplots(figsize=(7.4, 3.6), dpi=100)
    fig.patch.set_facecolor("#101226")
    ax.set_facecolor("#161834")

    # Si no hay partidas
    if not partidas:
        ax.text(
            0.5, 0.5,
            "Aún no hay partidas registradas en RetroTrack.\n\n¡Completá tu primera misión para ver tu evolución acá!",
            ha="center", va="center", color="#00f0ff", fontsize=12, fontweight="bold",
            transform=ax.transAxes
        )
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("RetroTrack - Historial de Misiones Espaciales", color="#ffffff", fontsize=13, pad=12)
        for spine in ax.spines.values():
            spine.set_color("#2a2e55")

        plt.tight_layout()
        plt.savefig(ruta_imagen, facecolor=fig.get_facecolor(), edgecolor="none")
        plt.close(fig)
        return False, ruta_imagen

    # Si hay partidas
    numeros_partida = list(range(1, len(partidas) + 1))
    puntuaciones = [p["puntuacion"] for p in partidas]

    # Graficar puntos
    ax.plot(
        numeros_partida, puntuaciones,
        marker="o", markersize=6, color="#00f0ff", linewidth=2.2,
        label="Puntos conseguidos"
    )

    # Línea de tendencia si hay 2 o más partidas
    if len(puntuaciones) >= 2:
        n = len(numeros_partida)
        sum_x = sum(numeros_partida)
        sum_y = sum(puntuaciones)
        sum_xy = sum(x * y for x, y in zip(numeros_partida, puntuaciones))
        sum_x2 = sum(x ** 2 for x in numeros_partida)
        denom = (n * sum_x2 - sum_x ** 2)
        if denom != 0:
            m = (n * sum_xy - sum_x * sum_y) / denom
            b = (sum_y - m * sum_x) / n
            tendencia = [m * x + b for x in numeros_partida]
            signo = "+" if m >= 0 else ""
            ax.plot(
                numeros_partida, tendencia,
                linestyle="--", color="#ff2882", linewidth=1.8,
                label=f"Tendencia ({signo}{m:.1f} pts/misión)"
            )

    ax.set_title("Evolución de Puntuación Espacial por Partida", color="#ffffff", fontsize=12, fontweight="bold", pad=10)
    ax.set_xlabel("Número de Partida", color="#d0d0e0", fontsize=10)
    ax.set_ylabel("Puntos Obtenidos", color="#d0d0e0", fontsize=10)
    ax.set_xticks(numeros_partida)
    ax.tick_params(colors="#c0c0d8")
    ax.grid(True, linestyle=":", alpha=0.35, color="#8080a0")
    ax.legend(facecolor="#181a33", edgecolor="#00f0ff", labelcolor="#ffffff", loc="upper left")

    for spine in ax.spines.values():
        spine.set_color("#3a3e66")

    plt.tight_layout()
    plt.savefig(ruta_imagen, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)

    return True, ruta_imagen


def mostrar_pantalla_estadisticas(pantalla, reloj):
    """
    Muestra la pantalla de estadísticas directamente dentro de Pygame.
    Carga la imagen generada por Matplotlib y muestra las métricas clave.
    Garantiza compatibilidad absoluta con el ejecutable .exe de Windows.
    """
    fuente_titulo = pygame.font.SysFont("Consolas", 32, bold=True)
    fuente_sub = pygame.font.SysFont("Consolas", 15)
    fuente_metricas = pygame.font.SysFont("Consolas", 16, bold=True)
    fuente_boton = pygame.font.SysFont("Consolas", 18, bold=True)

    # Generar el gráfico actualizado
    generar_grafico_estadisticas()
    resumen = obtener_resumen_estadisticas()
    ruta_grafico = obtener_ruta_imagen_grafico()

    # Cargar la imagen del gráfico generada por Matplotlib
    surf_grafico = None
    if os.path.exists(ruta_grafico):
        try:
            surf_grafico = pygame.image.load(ruta_grafico)
        except Exception as e:
            print(f"[Estadísticas] No se pudo cargar la imagen: {e}")

    boton_volver = pygame.Rect(280, 530, 240, 46)

    viendo_estadisticas = True
    while viendo_estadisticas:
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_m):
                    return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_volver.collidepoint(pos_mouse):
                    return

        # Dibujar pantalla
        pantalla.fill(COLOR_FONDO)

        # Título
        tit = fuente_titulo.render("ESTADÍSTICAS Y EVOLUCIÓN DEL PILOTO", True, COLOR_CIAN)
        pantalla.blit(tit, (pantalla.get_width() // 2 - tit.get_width() // 2, 20))

        sub = fuente_sub.render("Datos obtenidos directamente de 'datos/historial.csv'", True, COLOR_TEXTO_MUTED)
        pantalla.blit(sub, (pantalla.get_width() // 2 - sub.get_width() // 2, 60))

        # Panel de métricas en recuadro
        rect_metricas = pygame.Rect(30, 85, 740, 50)
        pygame.draw.rect(pantalla, (20, 22, 45), rect_metricas, border_radius=8)
        pygame.draw.rect(pantalla, (50, 60, 95), rect_metricas, width=1, border_radius=8)

        if resumen["hay_datos"]:
            txt_m = (
                f"Misiones: {resumen['total_partidas']}  |  "
                f"Récord: {resumen['mejor_puntuacion']} pts  |  "
                f"Promedio: {resumen['puntuacion_promedio']} pts  |  "
                f"Mayor Tiempo: {resumen['mejor_tiempo']}s"
            )
            color_m = COLOR_AMARILLO
        else:
            txt_m = "Aún no hay partidas registradas. ¡Jugá tu primera partida para ver tus datos!"
            color_m = COLOR_CIAN

        surf_m = fuente_metricas.render(txt_m, True, color_m)
        pantalla.blit(surf_m, (rect_metricas.centerx - surf_m.get_width() // 2, rect_metricas.centery - surf_m.get_height() // 2))

        # Dibujar la imagen del gráfico de Matplotlib
        if surf_grafico:
            pantalla.blit(surf_grafico, (30, 150))
        else:
            rect_vacio = pygame.Rect(30, 150, 740, 360)
            pygame.draw.rect(pantalla, (18, 20, 38), rect_vacio, border_radius=8)
            t_sin = fuente_metricas.render("Generando gráfico estadístico...", True, COLOR_TEXTO_MUTED)
            pantalla.blit(t_sin, (rect_vacio.centerx - t_sin.get_width() // 2, rect_vacio.centery - t_sin.get_height() // 2))

        # Botón Volver
        hov = boton_volver.collidepoint(pos_mouse)
        pygame.draw.rect(pantalla, (0, 160, 180) if hov else (0, 110, 130), boton_volver, border_radius=8)
        pygame.draw.rect(pantalla, COLOR_CIAN, boton_volver, width=2, border_radius=8)
        t_btn = fuente_boton.render("Volver al Menú [ESC]", True, COLOR_TEXTO)
        pantalla.blit(t_btn, (boton_volver.centerx - t_btn.get_width() // 2, boton_volver.centery - t_btn.get_height() // 2))

        pygame.display.flip()
        reloj.tick(60)


# Para mantener compatibilidad con cualquier llamada previa
def mostrar_grafico_en_ventana():
    generar_grafico_estadisticas()
