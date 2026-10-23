# 🏃 RetroTrack — Videojuego Arcade 2D & Sistema de Rendimiento del Jugador

**RetroTrack** es un proyecto integral de programación en Python diseñado con fines educativos y de demostración técnica. Combina un videojuego arcade retro en 2D donde un chico debe esquivar objetos que caen desde los edificios, con un sistema de persistencia en CSV, procesamiento de datos con **Pandas** y visualización gráfica del aprendizaje con **Matplotlib**.

---

## 📋 Tabla de Contenidos
1. [Descripción General](#-descripción-general)
2. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
3. [Estructura del Proyecto](#-estructura-del-proyecto)
4. [Instalación y Requisitos (Windows)](#-instalación-y-requisitos-windows)
5. [Ejecución del Juego](#-ejecución-del-juego)
6. [Controles y Mecánicas](#-controles-y-mecánicas)
7. [Persistencia y Archivo CSV](#-persistencia-y-archivo-csv)
8. [Análisis con Pandas y Gráficos con Matplotlib](#-análisis-con-pandas-y-gráficos-con-matplotlib)
9. [Pruebas Automatizadas](#-pruebas-automatizadas)
10. [Plan de Trabajo y Bitácora](#-plan-de-trabajo-y-bitácora)

---

## 🎯 Descripción General

En **RetroTrack**, el protagonista es un chico que camina por la vereda de la ciudad y debe esquivar diferentes objetos cotidianos que caen desde los balcones de los edificios:
- 🪴 **Macetas con plantas**
- 🏀 **Pelotas de básquetbol**
- ⚙️ **Yunques pesados**
- 🧱 **Ladrillos de obra**
- 📦 **Cajas de cartón**

A medida que avanza la partida, la dificultad aumenta de forma progresiva: los objetos caen más rápido y aparecen con mayor frecuencia.

Cada vez que el chico colisiona con un objeto, la partida finaliza y **sus resultados se registran automáticamente** en `historial_partidas.csv` sin borrar las partidas anteriores. Desde el menú principal, el usuario puede consultar en cualquier momento el **análisis estadístico** que procesa el historial y genera gráficos interactivos con líneas de tendencia que ilustran la evolución del rendimiento a lo largo del tiempo.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje de programación principal.
- **Pygame (>= 2.5.0)**: Ventana gráfica, renderizado retro vectorial a 60 FPS, animación de caminata, detección de eventos de teclado/ratón y colisiones rectangulares (`colliderect`).
- **Pandas (>= 2.0.0)**: Lectura del CSV en DataFrames, cálculo de métricas descriptivas (medias, máximos, totales y comparativas temporales).
- **Matplotlib (>= 3.7.0)**: Trazado de gráficos comparativos (evolución de puntaje y tiempo de supervivencia) con subplots y líneas de tendencia mediante regresión lineal (`numpy.polyfit`).
- **Módulos Estándar**: `time`, `datetime`, `random`, `pathlib`, `os` y `sys`.

---

## 📂 Estructura del Proyecto

```text
RetroTrack/
├── main.py                     # Menú interactivo con soporte de teclado y ratón
├── juego.py                    # Bucle a 60 FPS, el chico, objetos urbanos y colisiones
├── estadisticas.py             # Persistencia en CSV, análisis con Pandas y gráficos Matplotlib
├── historial_partidas.csv      # Archivo generado automáticamente con el registro histórico
├── requirements.txt            # Dependencias del proyecto (pygame, pandas, matplotlib, numpy)
├── test_retrotrack.py          # Batería de pruebas automatizadas (5 tests rigurosos)
├── generar_datos_ejemplo.py    # Script auxiliar para generar partidas de muestra al instante
├── limpiar_historial.py        # Script auxiliar para reiniciar el historial a cero
├── PLAN_DE_TRABAJO.md          # Bitácora cronológica y fases de ingeniería realizadas
└── README.md                   # Documentación técnica completa
```

---

## 💻 Instalación y Requisitos (Windows)

### 1. Requisitos Previos
Asegurate de tener instalado Python 3.10 o superior en Windows. Podés verificarlo abriendo PowerShell o el Símbolo del sistema:
```powershell
python --version
```

### 2. Posicionarse en la Carpeta del Proyecto
```powershell
cd C:\RetroTrack
```

### 3. Crear y Activar un Entorno Virtual (Recomendado)
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 4. Instalar las Dependencias
```powershell
pip install -r requirements.txt
```

---

## 🎮 Ejecución del Juego

Con el entorno virtual activado, iniciá RetroTrack con:
```powershell
python main.py
```

### Navegación del Menú
- Presioná **`[ 1 ]`** o hacé clic en **COMENZAR A JUGAR** para iniciar una partida.
- Presioná **`[ 2 ]`** o **`[ E ]`** o hacé clic en **CONSULTAR ESTADÍSTICAS** para ver los análisis y gráficos.
- Presioná **`[ 3 ]`** o **`[ ESC ]`** o hacé clic en **SALIR** para cerrar la aplicación de forma limpia.

---

## 🕹️ Controles y Mecánicas

| Acción | Teclas |
| :--- | :--- |
| **Correr a la Izquierda** | Flecha Izquierda `[ ← ]` o tecla `[ A ]` |
| **Correr a la Derecha** | Flecha Derecha `[ → ]` o tecla `[ D ]` |
| **Pausar / Volver al Menú** | Tecla `[ ESC ]` |
| **Reiniciar Partida (en Game Over)** | Tecla `[ R ]` |
| **Volver al Menú (en Game Over)** | Tecla `[ M ]` o `[ ENTER ]` |

### Sistema de Puntuación y Dificultad
- **Puntaje por Tiempo:** 10 puntos por cada segundo de supervivencia.
- **Bonificación por Evasión:** +25 puntos por cada objeto que cae y toca la vereda sin golpear al chico.
- **Dificultad Progresiva:** Cada 7 segundos transcurridos, el nivel aumenta en 1. La velocidad de caída de los objetos sube `0.75 px/frame` y el tiempo de espera entre apariciones se reduce gradualmente.

---

## 💾 Persistencia y Archivo CSV

Cada partida completada invoca a:
```python
estadisticas.guardar_partida(duracion_segundos, puntaje)
```

El archivo `historial_partidas.csv` se estructura de la siguiente manera:
```csv
fecha,duracion_segundos,puntaje
2026-10-22 20:30:15,14.25,280
2026-10-22 20:32:40,22.80,510
2026-10-22 20:35:10,31.40,790
```

1. **Modo Append (`"a"`):** Se utiliza `open(RUTA_CSV, mode="a", ...)` para anexar registros al final sin sobrescribir partidas previas.
2. **Creación Automática:** Si el archivo no existe, escribe automáticamente la fila de encabezados `fecha,duracion_segundos,puntaje`.
3. **Tolerancia a Estado Vacío:** Si el archivo aún no existe, el juego y las estadísticas funcionan con normalidad, mostrando mensajes de bienvenida sin arrojar excepciones.

---

## 📊 Análisis con Pandas y Gráficos con Matplotlib

Al seleccionar la opción de estadísticas:

### 1. Resumen en Consola con Pandas
Se imprime una tabla con formato claro calculada a partir de los datos reales:
```text
============================================================
             RETROTRACK - ESTADÍSTICAS DEL JUGADOR          
============================================================
 * Total de partidas jugadas:        6
 * Mejor puntaje histórico:          1180 pts
 * Mayor tiempo de supervivencia:    42.6 segundos
 * Puntaje promedio:                 660.0 pts
 * Tiempo promedio sobrevivido:      25.44 segundos
------------------------------------------------------------
 * Puntaje en la primera partida:    230 pts
 * Puntaje en la última partida:     1180 pts
 * Evolución global (última - 1ra):  +950 pts
============================================================
```

### 2. Ventana Gráfica con Matplotlib
Se despliega una ventana interactiva con dos subplots y estética arcade oscura:
- **Subplot Izquierdo:** *Evolución del Puntaje por Partida* (Puntos vs. Partida) con marcadores cian y una **línea de tendencia** discontinua fucsia ($pts/partida$).
- **Subplot Derecho:** *Tiempo de Supervivencia por Partida* (Segundos vs. Partida) con marcadores dorados y línea de tendencia verde neón.
- **Nota pedagógica:** Se incluye la aclaración requerida indicando que estos gráficos ilustran la evolución del desempeño en el juego pero no constituyen por sí solos una prueba de laboratorio neurocientífica controlada.

---

## 🧪 Pruebas Automatizadas

El proyecto incluye una suite de pruebas técnicas independientes en `test_retrotrack.py`. Podés ejecutarla con:

```powershell
python test_retrotrack.py
```

### Resultados de la Batería de Pruebas:
```text
============================================================
 INICIANDO BATERÍA DE PRUEBAS TÉCNICAS PARA RETROTRACK
============================================================

[TEST 1] Verificación con CSV ausente...
  -> PASADO: Manejo de historial vacío correcto y amigable.

[TEST 2] Verificación de guardado en CSV (modo append)...
  -> PASADO: Archivo CSV creado y registros agregados sin sobreescritura.

[TEST 3] Verificación de métricas estadísticas con Pandas...
  -> PASADO: Métricas de Pandas exactas (Total: 4, Promedio Pts: 575.0, Max: 950).

[TEST 4] Verificación de mecánicas de juego (Jugador, Obstáculos, Colisión)...
  -> PASADO: Lógica de jugador, límites, movimiento y colisiones verificada.

[TEST 5] Verificación de generación de gráficos con Matplotlib...
  -> PASADO: Generación de figuras, subplots y cálculo de tendencia exitoso.

============================================================
 ¡TODAS LAS PRUEBAS TÉCNICAS (5/5) FUERON SUPERADAS CON ÉXITO!
============================================================
```

---

## 📚 Scripts Auxiliares de Demostración

- **Generar datos de prueba inmediatos:**
  ```powershell
  python generar_datos_ejemplo.py
  ```
  Genera 6 partidas simuladas con una curva de aprendizaje realista para evaluar los gráficos de inmediato.

- **Reiniciar el historial a cero:**
  ```powershell
  python limpiar_historial.py
  ```
  Elimina el CSV para probar el comportamiento inicial del sistema cuando no hay datos.

---

## 📋 Plan de Trabajo y Bitácora

En el archivo [`PLAN_DE_TRABAJO.md`](file:///C:/RetroTrack/PLAN_DE_TRABAJO.md) tenés acceso a la bitácora completa de ingeniería que explica fase por fase **qué fuimos haciendo**, las decisiones de diseño y los problemas resueltos paso a paso.
