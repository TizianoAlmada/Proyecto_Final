# 🛡️ LimpiadorPC: Limpiador de Almacenamiento para Windows — Edición Técnica

**LimpiadorPC** es un programa de escritorio para Windows desarrollado en Python con **Tkinter**, diseñado para analizar el almacenamiento y encontrar archivos temporales e innecesarios. Al finalizar cada limpieza, guarda automáticamente en un archivo JSON la fecha/hora, la cantidad de archivos eliminados, el espacio recuperado (en MB o GB) y las categorías procesadas. Representa el uso del disco en una barra gráfica interactiva, muestra el avance en tiempo real mediante **multithreading** y permite consultar el historial de limpiezas anteriores de forma segura.

Incluye el código fuente modular, la suite de pruebas automatizadas, el ejecutable directo para Windows (**`dist/LimpiadorPC/LimpiadorPC.exe`**) y scripts de ejecución y compilación con un solo clic.

---

## 📂 Estructura del Proyecto

```text
Limpiador_de_almacenamiento/
│
├── main.py                     # Punto de entrada y arranque del bucle principal
├── interfaz.py                 # Ventana en modo oscuro tecnológico y control de hilos
├── analizador.py               # Escaneo seguro de temporales y consulta de la papelera
├── limpiador.py                # Motor de eliminación con try/except y vaciado seguro
├── almacenamiento.py           # Cálculo de espacio total, ocupado y disponible del disco
├── historial.py                # Persistencia automática en datos/historial.json
├── utilidades.py               # Conversión matemática de bytes y filtro de rutas seguras
├── test_limpiador.py           # Batería de 6 pruebas unitarias automatizadas
├── requirements.txt            # Dependencias externas necesarias (PyInstaller, psutil)
├── PLAN_DE_TRABAJO.md          # Plan de trabajo por etapas y bitácora técnica
├── README.md                   # Documentación general del proyecto
│
├── ejecutar_programa.bat       # Lanzador rápido del programa en modo Python
├── generar_exe.bat             # Script para compilar el .exe con PyInstaller
├── instalar_dependencias.bat   # Instalador automático de paquetes de Python
│
├── dist/
│   └── LimpiadorPC/
│       ├── LimpiadorPC.exe     # Ejecutable directo para Windows (doble clic)
│       ├── _internal/          # Dependencias y librerías empaquetadas
│       ├── datos/              # Carpeta de historial de la versión portable
│       └── recursos/           # Iconos y recursos portables
│
├── datos/
│   └── historial.json          # Base de datos local en JSON con las limpiezas realizadas
│
└── recursos/
    └── icono.ico               # Icono de la aplicación
```

---

## 🧹 Categorías de Limpieza Analizadas

1. **Archivos Temporales de Usuario (`%TEMP%`)**:
   - Archivos temporales creados por programas en la carpeta `AppData\Local\Temp`.
   - Incluye instaladores descargados temporalmente, cachés de edición y datos transitorios.
2. **Archivos Temporales de Windows (`C:\Windows\Temp`)**:
   - Registros residuales generados por actualizaciones del sistema operativo y tareas de mantenimiento de Windows.
3. **Papelera de Reciclaje (API Win32 `shell32.dll`)**:
   - Consulta precisa del peso y cantidad de elementos mediante `SHQueryRecycleBinW` **sin vaciarla automáticamente**.
   - Solo se vacía (`SHEmptyRecycleBinW`) si el usuario marca su casilla y lo confirma expresamente.
4. **Caché de Navegadores Web**:
   - Archivos temporales de páginas web visitadas para Google Chrome, Microsoft Edge, Mozilla Firefox y Brave.
5. **Reportes de Error y Logs Temporales**:
   - Volcados de memoria de aplicaciones caídas (`CrashDumps`) e informes de fallos del sistema (`WER`).

---

## 📊 Sistema de Almacenamiento y Métricas

En el panel superior de la aplicación:
- **Detección de Unidades:** Permite alternar entre las letras de disco presentes en el equipo (`C:\`, `D:\`, etc.).
- **Barra de Ocupación Gráfica:** Dibuja sobre un `Canvas` el porcentaje exacto de ocupación del disco en azul cian neón.
- **Tarjetas de Estadísticas:** Muestra en tiempo real:
  - Espacio Total del Disco (ej: `475.82 GB`).
  - Espacio Ocupado con porcentaje (ej: `346.18 GB - 72.8%`).
  - Espacio Disponible con porcentaje (ej: `129.64 GB - 27.2%`).

---

## 📋 Sistema de Historial Persistente

Al presionar la pestaña **📋 Historial de Limpiezas**:
- Carga y muestra los registros guardados en [datos/historial.json](file:///c:/Limpiador_de_almacenamiento/datos/historial.json) en una tabla moderna (`ttk.Treeview`).
- Columnas detalladas: **Fecha y Hora**, **Archivos Borrados**, **Espacio Recuperado** y **Categorías Limpiadas**.
- Botón **"🔄 Actualizar"** para recargar los datos tras una nueva limpieza.
- Botón **"🗑️ Vaciar Historial"** con confirmación previa para reiniciar los registros a cero cuando el usuario lo desee.

---

## 🛡️ Medidas de Seguridad Estrictas

1. **Protección Absoluta de Archivos Personales:**
   - La función `es_ruta_segura()` rechaza y bloquea automáticamente cualquier intento de borrado en `Documentos`, `Imágenes`, `Escritorio`, `Descargas`, `Música`, `Videos`, `System32` o `Program Files`.
2. **Manejo Seguro de Archivos en Uso (`try...except`):**
   - Si un archivo temporal está bloqueado o abierto por otra aplicación activa, Windows genera un `PermissionError`. El programa lo captura, lo suma a la cuenta de "archivos omitidos" y continúa con el siguiente sin cerrarse ni congelarse.
3. **Preservación de Carpetas Raíz:**
   - Carpetas clave como `C:\Windows\Temp` o `%TEMP%` nunca se eliminan; solo se depuran los archivos y subcarpetas vacías dentro de ellas.
4. **Confirmación Previa Obligatoria:**
   - La limpieza nunca es automática. Siempre requiere que el usuario presione el botón "Limpiar" y acepte el diálogo emergente (`messagebox.askyesno`) que resume la cantidad de archivos y los megabytes a liberar.

---

## 🚀 Cómo Usar el Limpiador

### Opción 1: Ejecutable Directo (Sin necesidad de Python instalado)
Hacé doble clic en:
👉 **`dist\LimpiadorPC\LimpiadorPC.exe`**  
*(Podés copiar la carpeta `dist\LimpiadorPC` completa a un pendrive y llevarla a cualquier computadora con Windows).*

### Opción 2: Desde Script Batch (Modo Rápido)
Hacé doble clic en el archivo:
👉 **`ejecutar_programa.bat`**

### Opción 3: Modo Desarrollo (Desde la Terminal)
```powershell
cd C:\Limpiador_de_almacenamiento
.\.venv\Scripts\activate
python main.py
```

### Para Ejecutar las Pruebas Unitarias
```powershell
python test_limpiador.py
```

---

## 🛠️ Controles y Funcionamiento de la Interfaz

| Elemento | Acción que Realiza |
| :--- | :--- |
| **Selector de Unidad** | Cambia la letra de disco a inspeccionar (`C:\`, `D:\`) y actualiza la barra gráfica. |
| **Casillas de Categorías** | Permite marcar o desmarcar individualmente qué áreas temporales analizar o limpiar. |
| **Marcar / Desmarcar Todos** | Selecciona o deselecciona todas las casillas con un solo clic. |
| **🔍 1. ANALIZAR SISTEMA** | Inicia el escaneo en un hilo secundario sin congelar la ventana y calcula los GB recuperables. |
| **🧹 2. LIMPIAR ARCHIVOS** | Solicita confirmación y ejecuta el borrado seguro de los archivos seleccionados. |
| **Pestaña Historial** | Consulta la lista cronológica de limpiezas anteriores con su fecha y espacio liberado. |
| **Pestaña Seguridad** | Despliega las reglas de protección y la explicación técnica para el usuario o docente. |
