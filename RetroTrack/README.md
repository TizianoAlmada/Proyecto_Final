# 🚀 RetroTrack: Odisea Espacial — Edición Arcade Definitiva

**RetroTrack** es un videojuego arcade 2D en Python desarrollado con **Pygame**, ambientado en el espacio exterior. El jugador pilota cazas estelares (**Astra** y **Nova**) esquivando asteroides y meteoritos en un campo estelar dinámico, con registro persistente de misiones en CSV y visualización integrada de estadísticas y evolución con **Matplotlib**.

Incluye el código fuente modular, el ejecutable directo para Windows (**`RetroTrack.exe`**) y el instalador independiente (**`Instalar_RetroTrack.exe`**).

---

## 📂 Estructura del Proyecto

```text
RetroTrack/
│
├── main.py                     # Punto de entrada y coordinación de pantallas
├── menu.py                     # Menú principal interactivo y navegación espacial
├── juego.py                    # Bucle a 60 FPS, física de naves, estrellas y asteroides
├── personajes.py               # Definición y pantalla de selección de naves (Astra y Nova)
├── historial.py                # Persistencia automática en datos/historial.csv
├── estadisticas.py             # Generación de gráficos e interfaz visual en Pygame
├── requirements.txt            # Dependencias externas necesarias
├── test_retrotrack.py          # Batería de 5 pruebas unitarias automatizadas
├── PLAN_DE_TRABAJO.md          # Plan de trabajo por etapas y bitácora técnica
├── README.md                   # Documentación general
│
├── RetroTrack.exe              # Ejecutable directo del juego (doble clic)
├── Instalar_RetroTrack.exe     # Instalador independiente para Windows
│
├── datos/
│   ├── historial.csv           # Base de datos en texto plano (Excel compatible)
│   └── estadisticas.png        # Gráfico evolutivo con línea de tendencia
│
├── recursos/
│   ├── imagenes/               # Carpeta para recursos visuales locales
│   └── sonidos/                # Carpeta para recursos de audio locales
│
└── instalador/
    ├── configuracion_instalador.iss  # Script oficial para Inno Setup
    └── instalador_grafico.py         # Código fuente del instalador gráfico
```

---

## 🚀 Naves Jugables

1. **Astra (Interceptor Alfa)**:
   - Caza estelar de color cian neón con alas delta y cabina luminosa.
   - Propulsor de plasma cian animado.
2. **Nova (Caza de Asalto)**:
   - Nave de ataque magenta neón con alerones en flecha invertida y cabina dorada.
   - Motores gemelos de plasma magenta animados.

Ambas naves cuentan con una hitbox equilibrada de $44 \times 44$ píxeles para garantizar total justicia competitiva.

---

## 🪨 Amenazas Espaciales (Obstáculos)

1. **Asteroide Rocoso**: Masa rocosa con cráteres detallados.
2. **Meteorito Ígneo**: Fragmento incandescente con núcleo de fuego y estela abrasadora.
3. **Asteroide de Cristal / Hielo**: Formación cristalina brillante de alta velocidad.
4. **Chatarra Espacial**: Satélite residual a la deriva con paneles solares.

---

## 📊 Sistema de Estadísticas Integrado

Al presionar la opción **3. Estadísticas y Gráficos** en el menú principal:
- Genera automáticamente un gráfico de evolución estadística con **Matplotlib** (`datos/estadisticas.png`).
- Presenta el gráfico y tarjetas de métricas (partidas jugadas, récord de puntaje, tiempo total de vuelo y promedio) **directamente dentro de la ventana de Pygame**.
- No depende de ventanas externas de Tkinter ni causa bloqueos en el ejecutable `.exe`.
- Si aún no hay partidas registradas, muestra un aviso claro y orientativo para jugar la primera misión.

---

## 🎮 Cómo Jugar

### Opción 1: Ejecutable Directo (Sin necesidad de Python)
Hacé doble clic en **`RetroTrack.exe`** en la carpeta del juego.

### Opción 2: Instalador de Windows
Hacé doble clic en **`Instalar_RetroTrack.exe`** para instalar el juego en tu computadora. Creará automáticamente accesos directos en tu **Escritorio** y en el **Menú Inicio**.

### Opción 3: Modo Desarrollo (Desde Python)
```powershell
cd C:\RetroTrack
.\.venv\Scripts\activate
python main.py
```

---

## 🕹️ Controles del Juego

| Acción | Teclado |
| :--- | :--- |
| **Mover a la Izquierda** | Flecha Izquierda `[ ← ]` o tecla `[ A ]` |
| **Mover a la Derecha** | Flecha Derecha `[ → ]` o tecla `[ D ]` |
| **Volver al Menú / Pausa / Salir de Estadísticas** | Tecla `[ ESC ]` |
| **Reintentar Misión (en Game Over)** | Tecla `[ R ]` |
| **Cambiar Nave (en Game Over)** | Tecla `[ P ]` |
| **Menú Principal (en Game Over)** | Tecla `[ M ]` |

---

## 🧪 Pruebas Técnicas
Podés verificar la integridad de todos los módulos ejecutando:
```powershell
python test_retrotrack.py
```
*Todas las pruebas (5/5) superadas con éxito.*
