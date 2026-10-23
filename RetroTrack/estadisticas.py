"""
==============================================================================
Módulo de Estadísticas y Análisis de Rendimiento - RetroTrack
==============================================================================
Este módulo se encarga de:
1. Guardar de forma persistente cada partida jugada en un archivo CSV.
2. Leer y procesar el historial de partidas utilizando la librería Pandas.
3. Calcular métricas clave del rendimiento del jugador (promedios, máximos, evolución).
4. Generar gráficos interactivos mediante Matplotlib para visualizar el progreso.

Diseñado con un enfoque pedagógico, claro y modular para estudiantes de programación.
==============================================================================
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# Configurar el directorio temporal para caché de Matplotlib antes de importarlo.
# Esto previene problemas de permisos en Windows y acelera el inicio.
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib_retrotrack"))
import matplotlib.pyplot as plt

# Ruta absoluta al archivo CSV dentro de la misma carpeta de este script
RUTA_CARPETA = Path(__file__).resolve().parent
RUTA_CSV = RUTA_CARPETA / "historial_partidas.csv"

# Nombres de las columnas requeridas en el archivo CSV
COLUMNAS_CSV = ["fecha", "duracion_segundos", "puntaje"]


def guardar_partida(duracion_segundos: float, puntaje: int) -> bool:
    """
    Guarda el resultado de una partida en el archivo 'historial_partidas.csv'.
    
    Si el archivo no existe, lo crea e inserta los nombres de columnas (encabezado).
    Si ya existe, agrega la nueva fila al final sin borrar los registros anteriores (modo 'append').

    Parámetros:
        duracion_segundos (float): Tiempo total sobrevivido en segundos.
        puntaje (int): Puntos obtenidos por el jugador.

    Retorna:
        bool: True si se guardó con éxito, False en caso de error.
    """
    try:
        # Validar y formatear los datos de la partida
        duracion_limpia = round(float(duracion_segundos), 2)
        puntaje_limpio = int(puntaje)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Comprobar si el archivo ya existe y si tiene contenido
        archivo_existe = RUTA_CSV.exists() and RUTA_CSV.stat().st_size > 0

        # Abrir el archivo en modo "a" (append = agregar al final) con codificación UTF-8
        with open(RUTA_CSV, mode="a", encoding="utf-8", newline="") as archivo:
            # Si el archivo es nuevo o estaba vacío, escribimos el encabezado
            if not archivo_existe:
                archivo.write(",".join(COLUMNAS_CSV) + "\n")
            
            # Escribir la nueva fila con los datos de la partida
            linea = f"{fecha_actual},{duracion_limpia},{puntaje_limpio}\n"
            archivo.write(linea)

        print(f"[RetroTrack] Partida guardada exitosamente: {fecha_actual} | {duracion_limpia}s | {puntaje_limpio} pts")
        return True

    except Exception as e:
        print(f"[RetroTrack] Error al intentar guardar la partida en CSV: {e}")
        return False


def cargar_datos() -> pd.DataFrame | None:
    """
    Lee el archivo CSV de historial de partidas y lo convierte en un DataFrame de Pandas.

    Retorna:
        pd.DataFrame | None: El DataFrame con las partidas registradas, o None si no hay datos.
    """
    if not RUTA_CSV.exists():
        return None

    try:
        df = pd.read_csv(RUTA_CSV)
        # Verificar si el archivo está vacío o si le faltan filas
        if df.empty or len(df) == 0:
            return None
        
        # Validar que existan las columnas obligatorias
        for col in COLUMNAS_CSV:
            if col not in df.columns:
                print(f"[RetroTrack] Advertencia: la columna '{col}' no existe en el archivo CSV.")
                return None

        # Asegurar tipos de datos numéricos correctos
        df["duracion_segundos"] = pd.to_numeric(df["duracion_segundos"], errors="coerce").fillna(0.0)
        df["puntaje"] = pd.to_numeric(df["puntaje"], errors="coerce").fillna(0).astype(int)

        return df

    except pd.errors.EmptyDataError:
        # El archivo existe pero está completamente en blanco
        return None
    except Exception as e:
        print(f"[RetroTrack] Error al leer el archivo CSV con Pandas: {e}")
        return None


def calcular_metricas(df: pd.DataFrame | None = None) -> dict:
    """
    Calcula estadísticas descriptivas del rendimiento del jugador usando Pandas.

    Parámetros:
        df (pd.DataFrame | None): DataFrame con los datos. Si es None, lo carga automáticamente.

    Retorna:
        dict: Diccionario con todas las métricas calculadas o con 'hay_datos': False.
    """
    if df is None:
        df = cargar_datos()

    if df is None or df.empty:
        return {
            "hay_datos": False,
            "mensaje": "Aún no hay partidas registradas. ¡Jugá tu primera partida en RetroTrack para ver tus estadísticas!"
        }

    total_partidas = len(df)
    tiempo_promedio = round(float(df["duracion_segundos"].mean()), 2)
    puntaje_promedio = round(float(df["puntaje"].mean()), 2)
    mejor_puntaje = int(df["puntaje"].max())
    mayor_tiempo = round(float(df["duracion_segundos"].max()), 2)

    # Análisis de evolución entre partidas
    primer_puntaje = int(df["puntaje"].iloc[0])
    ultimo_puntaje = int(df["puntaje"].iloc[-1])
    diferencia_puntaje = ultimo_puntaje - primer_puntaje

    # Comparación entre las primeras y últimas partidas si hay suficientes registros
    if total_partidas >= 4:
        mitad = total_partidas // 2
        promedio_primera_mitad = round(float(df["puntaje"].iloc[:mitad].mean()), 2)
        promedio_segunda_mitad = round(float(df["puntaje"].iloc[mitad:].mean()), 2)
        mejora_promedio = round(promedio_segunda_mitad - promedio_primera_mitad, 2)
    else:
        mejora_promedio = diferencia_puntaje

    return {
        "hay_datos": True,
        "total_partidas": total_partidas,
        "tiempo_promedio": tiempo_promedio,
        "puntaje_promedio": puntaje_promedio,
        "mejor_puntaje": mejor_puntaje,
        "mayor_tiempo": mayor_tiempo,
        "primer_puntaje": primer_puntaje,
        "ultimo_puntaje": ultimo_puntaje,
        "diferencia_puntaje": diferencia_puntaje,
        "mejora_promedio": mejora_promedio
    }


def obtener_mejor_puntaje() -> int:
    """
    Devuelve el récord histórico de puntaje registrado en el CSV.
    Retorna 0 si aún no hay partidas.
    """
    df = cargar_datos()
    if df is None or df.empty:
        return 0
    return int(df["puntaje"].max())


def mostrar_resumen_consola() -> dict:
    """
    Imprime en la consola un informe visual con las métricas calculadas por Pandas.
    Retorna el diccionario de métricas.
    """
    metricas = calcular_metricas()
    print("\n" + "=" * 60)
    print("             RETROTRACK - ESTADÍSTICAS DEL JUGADOR          ")
    print("=" * 60)

    if not metricas["hay_datos"]:
        print(f"\n  [!] {metricas['mensaje']}\n")
        print("=" * 60 + "\n")
        return metricas

    print(f" * Total de partidas jugadas:        {metricas['total_partidas']}")
    print(f" * Mejor puntaje histórico:          {metricas['mejor_puntaje']} pts")
    print(f" * Mayor tiempo de supervivencia:    {metricas['mayor_tiempo']} segundos")
    print(f" * Puntaje promedio:                 {metricas['puntaje_promedio']} pts")
    print(f" * Tiempo promedio sobrevivido:      {metricas['tiempo_promedio']} segundos")
    print("-" * 60)
    print(f" * Puntaje en la primera partida:    {metricas['primer_puntaje']} pts")
    print(f" * Puntaje en la última partida:     {metricas['ultimo_puntaje']} pts")
    
    dif = metricas["diferencia_puntaje"]
    signo = "+" if dif > 0 else ""
    print(f" * Evolución global (última - 1ra):  {signo}{dif} pts")
    print("=" * 60 + "\n")

    return metricas


def mostrar_graficos():
    """
    Genera y despliega dos gráficos con Matplotlib basados en los datos reales del CSV:
    1. Evolución del puntaje a lo largo de las partidas (con línea de tendencia).
    2. Tiempo de supervivencia a lo largo de las partidas (con línea de tendencia).

    Si no hay datos, muestra una ventana informativa invitando al jugador a comenzar.
    """
    df = cargar_datos()

    # Configuración de estética retro / limpia para Matplotlib
    plt.close("all")  # Cerrar cualquier ventana previa abierta
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.canvas.manager.set_window_title("RetroTrack - Rendimiento del Jugador (Matplotlib)")

    # Color de fondo general oscuro con estilo arcade
    fig.patch.set_facecolor("#12121e")
    ax1.set_facecolor("#1a1a2e")
    ax2.set_facecolor("#1a1a2e")

    if df is None or df.empty:
        # Caso sin partidas: mostrar mensaje pedagógico en ambos paneles
        for ax in (ax1, ax2):
            ax.text(
                0.5, 0.5,
                "Aún no hay partidas registradas.\n\n¡Jugá tu primera partida en RetroTrack\npara generar tus propios gráficos!",
                horizontalalignment="center",
                verticalalignment="center",
                color="#00ffff",
                fontsize=13,
                fontweight="bold",
                transform=ax.transAxes
            )
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color("#393e46")

        fig.suptitle("RetroTrack - Historial de Rendimiento", color="#ffffff", fontsize=15, fontweight="bold")
        plt.tight_layout()
        plt.show()
        return

    # Eje X: Número de partida ordenado secuencialmente (1, 2, 3, ..., N)
    numero_partidas = np.arange(1, len(df) + 1)
    puntajes = df["puntaje"].values
    tiempos = df["duracion_segundos"].values

    # -------------------------------------------------------------
    # Gráfico 1: Evolución del Puntaje
    # -------------------------------------------------------------
    ax1.plot(numero_partidas, puntajes, marker="o", markersize=7, color="#00ffcc",
             linewidth=2.2, label="Puntaje obtenido")

    # Si hay 2 o más partidas, calculamos una línea de tendencia lineal simple con numpy.polyfit
    if len(df) >= 2:
        coeficientes_puntaje = np.polyfit(numero_partidas, puntajes, deg=1)
        funcion_tendencia_puntaje = np.poly1d(coeficientes_puntaje)
        valores_tendencia_p = funcion_tendencia_puntaje(numero_partidas)
        pendiente_p = coeficientes_puntaje[0]
        ax1.plot(
            numero_partidas, valores_tendencia_p,
            linestyle="--", color="#ff007f", linewidth=1.8,
            label=f"Tendencia ({pendiente_p:+.1f} pts/partida)"
        )

    ax1.set_title("Evolución del Puntaje por Partida", color="#ffffff", fontsize=12, fontweight="bold", pad=10)
    ax1.set_xlabel("Número de Partida", color="#e0e0e0", fontsize=10)
    ax1.set_ylabel("Puntos Obtenidos", color="#e0e0e0", fontsize=10)
    ax1.set_xticks(numero_partidas)
    ax1.tick_params(colors="#e0e0e0")
    ax1.grid(True, linestyle=":", alpha=0.35, color="#808080")
    ax1.legend(loc="upper left", facecolor="#16213e", edgecolor="#00ffcc", labelcolor="#ffffff")

    # -------------------------------------------------------------
    # Gráfico 2: Evolución del Tiempo de Supervivencia
    # -------------------------------------------------------------
    ax2.plot(numero_partidas, tiempos, marker="s", markersize=7, color="#ffb703",
             linewidth=2.2, label="Segundos sobrevividos")

    # Línea de tendencia para el tiempo de supervivencia
    if len(df) >= 2:
        coeficientes_tiempo = np.polyfit(numero_partidas, tiempos, deg=1)
        funcion_tendencia_tiempo = np.poly1d(coeficientes_tiempo)
        valores_tendencia_t = funcion_tendencia_tiempo(numero_partidas)
        pendiente_t = coeficientes_tiempo[0]
        ax2.plot(
            numero_partidas, valores_tendencia_t,
            linestyle="--", color="#00f5d4", linewidth=1.8,
            label=f"Tendencia ({pendiente_t:+.1f} s/partida)"
        )

    ax2.set_title("Tiempo de Supervivencia por Partida", color="#ffffff", fontsize=12, fontweight="bold", pad=10)
    ax2.set_xlabel("Número de Partida", color="#e0e0e0", fontsize=10)
    ax2.set_ylabel("Duración (segundos)", color="#e0e0e0", fontsize=10)
    ax2.set_xticks(numero_partidas)
    ax2.tick_params(colors="#e0e0e0")
    ax2.grid(True, linestyle=":", alpha=0.35, color="#808080")
    ax2.legend(loc="upper left", facecolor="#16213e", edgecolor="#ffb703", labelcolor="#ffffff")

    # Ajuste del borde y título general
    for ax in (ax1, ax2):
        for spine in ax.spines.values():
            spine.set_color("#4a4e69")

    fig.suptitle("RetroTrack - Rendimiento y Progreso del Jugador", color="#00e5ff", fontsize=14, fontweight="bold")

    # Nota explicativa al pie requerida por los lineamientos pedagógicos
    nota_pie = (
        "Nota pedagógica: Estos gráficos permiten observar la evolución y tendencia del desempeño del jugador,\n"
        "aunque no demuestran por sí solos una mejora de los reflejos en condiciones científicas controladas."
    )
    plt.figtext(0.5, 0.02, nota_pie, ha="center", fontsize=8.5, color="#b0b0b0", style="italic")

    plt.subplots_adjust(bottom=0.17, top=0.88, wspace=0.25)
    plt.show()


def mostrar_resumen_y_graficos():
    """
    Función combinada que primero imprime las métricas en consola
    y luego abre la ventana visual de Matplotlib.
    """
    mostrar_resumen_consola()
    mostrar_graficos()


# Bloque de prueba directa si se ejecuta este módulo de forma independiente
if __name__ == "__main__":
    print("[RetroTrack] Ejecución directa del módulo 'estadisticas.py'.")
    mostrar_resumen_y_graficos()
