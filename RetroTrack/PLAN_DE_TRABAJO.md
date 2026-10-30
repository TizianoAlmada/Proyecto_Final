# 📋 PLAN DE TRABAJO DEFINITIVO Y BITÁCORA — RETROTRACK: ODISEA ESPACIAL

Este documento contiene el plan de trabajo organizado por etapas para el desarrollo de **RetroTrack (Edición Espacial)**, con el seguimiento y la verificación del estado de cada tarea.

---

## 📊 Tabla de Estado de las Etapas

| Etapa | Tareas principales | Resultado esperado | Estado |
|---|---|---|:---:|
| **1. Diagnóstico y Corrección de Gráficos** | Identificar por qué la opción 3 de Estadísticas no abría los gráficos (conflicto de GUI Tkinter en PyInstaller y falta de pantalla integrada). Rediseñar con `Agg` y visualizador nativo en Pygame. | Estadísticas visibles 100% integradas dentro del juego. | **Completado** |
| **2. Tematización Espacial** | Transformar el escenario urbano en el espacio exterior: campo de estrellas móviles con sensación de profundidad y velocidad cósmica. | Fondo dinámico espacial a 60 FPS. | **Completado** |
| **3. Cazas Estelares (Naves)** | Diseñar las naves jugables Astra (Interceptor Cían) y Nova (Caza Asalto Magenta) con dibujo vectorial, cabinas y propulsores animados. | Dos naves con hitboxes idénticas y aspecto único. | **Completado** |
| **4. Amenazas Espaciales** | Crear 4 tipos de asteroides (Rocoso, Meteorito ígneo, Cristal/Hielo y Chatarra espacial) que caen con velocidades variables. | Obstáculos espaciales con colisiones precisas. | **Completado** |
| **5. Menú Principal Espacial** | Adaptar el menú arcade con título estelar, indicador de nave seleccionada y navegación por teclado y ratón. | Menú temático completamente funcional. | **Completado** |
| **6. Guardado y Persistencia CSV** | Registrar automáticamente cada misión en `datos/historial.csv` (`fecha_hora,tiempo_segundos,puntuacion,personaje`) sin sobrescribir partidas previas. | Persistencia compatible con Excel. | **Completado** |
| **7. Pantalla de Estadísticas en Pygame** | Crear `mostrar_pantalla_estadisticas` para proyectar el gráfico `datos/estadisticas.png` y tarjetas resumen (partidas, récord, tiempo total, promedio) con opción de retorno `[ESC]`. | Gráficos y métricas visibles sin salir del juego. | **Completado** |
| **8. Batería de Pruebas Automatizada** | Validar la integridad de los 6 módulos, carga de naves, física de asteroides y renderizado gráfico mediante `test_retrotrack.py`. | 5 de 5 pruebas técnicas superadas (100%). | **Completado** |
| **9. Compilación de RetroTrack.exe** | Empaquetar el juego espacial con PyInstaller en un único archivo ejecutable autónomo para Windows. | `RetroTrack.exe` generado y funcional. | **Completado** |
| **10. Instalador para Windows** | Empaquetar `Instalar_RetroTrack.exe` que instala el juego y crea accesos directos en Escritorio y Menú Inicio. | Instalador autónomo listo para distribución. | **Completado** |
| **11. Documentación Pedagógica de 3.° Año** | Explicación detallada de cómo funcionan los `import` en Python, el flujo entre módulos y guía para la exposición oral. | Documentación didáctica completa. | **Completado** |

---

## 🛠️ Detalle de las Modificaciones Realizadas

### 1. Solución Definitiva al Problema de los Gráficos
- **Diagnóstico original**: El código previo intentaba usar `plt.show()` de Matplotlib. En aplicaciones empaquetadas con PyInstaller bajo Windows en modo `--windowed`, el backend de Tkinter suele ser excluido o genera bloqueos en el bucle de eventos si no hay una consola activa. Además, si el archivo CSV no tenía partidas, la función retornaba silenciosamente sin mostrar ninguna ventana informativa.
- **Solución implementada**:
  1. Se configuró Matplotlib en modo headless con `matplotlib.use('Agg')`, lo que genera y guarda la imagen `datos/estadisticas.png` de manera segura y sin depender de Tkinter ni bloquear hilos.
  2. Se programó la función `mostrar_pantalla_estadisticas(pantalla, reloj)` en `estadisticas.py`, que carga directamente el gráfico generado dentro de la misma ventana de Pygame, acompañado de 4 tarjetas de resumen informativo (Partidas Jugadas, Puntuación Récord, Tiempo Total en Misión y Promedio de Puntos).
  3. Si aún no hay partidas registradas, se renderiza una pantalla con mensaje informativo indicando al piloto que debe completar su primera misión para calcular estadísticas.

### 2. Ambientación Espacial y Naves
- **Fondo de Estrellas**: Se generó un campo estelar dinámico con estrellas de diferentes tamaños y velocidades, generando efecto de paralaje espacial a 60 FPS.
- **Naves**:
  - **Astra**: Caza interceptor azul/cian con alas delta, cabina cristalina y propulsor de plasma parpadeante.
  - **Nova**: Caza de asalto magenta/dorado con alas en flecha invertida y motores gemelos de plasma.
- **Obstáculos**:
  - **Asteroide Rocoso**: Con cráteres y relieve circular.
  - **Meteorito Ígneo**: Con núcleo ardiente rojo y estela de partículas de fuego.
  - **Asteroide de Cristal**: Bloque helado reflectivo en tonos cian y blanco.
  - **Chatarra Espacial**: Núcleo metálico con paneles solares laterales.

### 3. Distribución para Windows
- **`RetroTrack.exe`**: Compilado en modo `--onefile --windowed`.
- **`Instalar_RetroTrack.exe`**: Instalador autónomo que configura el juego en el sistema del usuario con accesos directos.

---
*Plan de trabajo actualizado y verificado en C:\RetroTrack.*
