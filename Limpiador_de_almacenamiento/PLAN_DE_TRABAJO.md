# PLAN DE TRABAJO: LIMPIADOR DE ESPACIO PARA WINDOWS CON PYTHON

**Nivel:** 3.º Año de Escuela Técnica - Especialidad en Programación  
**Proyecto:** Limpiador de Almacenamiento y Archivos Innecesarios para Windows  
**Tecnología:** Python 3 + Tkinter + PyInstaller  

---

## 📋 Introducción y Objetivos del Plan
Este plan describe paso a paso el proceso de diseño, estructuración modular, programación, pruebas y empaquetado del software de escritorio. Cada etapa tiene objetivos claros, archivos involucrados y criterios de comprobación para asegurar que el programa sea **100% funcional, seguro y comprensible** para ser expuesto ante un docente.

---

## 🛠️ Desglose de Etapas de Desarrollo

### Etapa 1: Análisis de Requisitos y Diseño de Arquitectura Modular
- **Objetivo:** Definir la responsabilidad de cada archivo `.py`, evitando código duplicado y asegurando que cada módulo cumpla una función específica.
- **Acciones:**
  1. Identificar las ubicaciones seguras de archivos temporales en Windows (`Temp` de Windows, `Temp` de usuario, caché de navegadores, papelera de reciclaje).
  2. Diseñar el flujo de datos: Almacenamiento -> Analizador -> Limpiador -> Historial -> Interfaz.
  3. Definir la regla de oro de seguridad: jamás tocar archivos personales (Documentos, Imágenes, Descargas, etc.).

### Etapa 2: Estructura de Carpetas y Configuración del Entorno
- **Objetivo:** Preparar el árbol de directorios del proyecto y el entorno virtual de Python.
- **Archivos a crear:**
  - `datos/historial.json` (almacenamiento persistente)
  - `recursos/` (íconos y elementos gráficos)
  - `requirements.txt` (lista de dependencias)

### Etapa 3: Módulo de Utilidades (`utilidades.py`)
- **Objetivo:** Centralizar funciones auxiliares para evitar repetición de código.
- **Funcionalidades:**
  - Conversión de bytes a unidades legibles (`B`, `KB`, `MB`, `GB`) con fórmulas matemáticas sencillas.
  - Resolución dinámica de rutas absolutas (compatible tanto en script como en el ejecutable `.exe` con `sys._MEIPASS`).
  - Validación de rutas seguras (comprobación de que una ruta pertenece a una carpeta temporal permitida antes de cualquier borrado).

### Etapa 4: Módulo de Almacenamiento (`almacenamiento.py`)
- **Objetivo:** Obtener información verídica del disco duro principal (C:) y de otras unidades disponibles.
- **Librerías a utilizar:** `shutil`, `os`, `ctypes` (Win32 API) y `psutil` (opcional/detectable).
- **Funcionalidades:**
  - Espacio total, espacio ocupado, espacio libre y porcentaje de uso.
  - Formato listo para mostrar en la interfaz gráfica.

### Etapa 5: Módulo de Historial (`historial.py`)
- **Objetivo:** Gestionar el registro histórico de las limpiezas realizadas.
- **Librerías a utilizar:** `json`, `os`, `datetime`.
- **Funcionalidades:**
  - Cargar el historial desde `datos/historial.json`.
  - Agregar un nuevo registro con fecha y hora exacta, cantidad de archivos borrados y megabytes recuperados.
  - Vaciar el historial si el usuario lo solicita.

### Etapa 6: Módulo Analizador (`analizador.py`)
- **Objetivo:** Escanear las carpetas temporales y calcular cuánto espacio se puede liberar sin borrar nada aún.
- **Categorías a analizar:**
  1. Temporales de Windows (`C:\Windows\Temp`).
  2. Temporales de Usuario (`%TEMP%`).
  3. Papelera de reciclaje (consulta mediante API Win32 `SHQueryRecycleBinW`).
  4. Caché de navegadores (Chrome, Edge, Firefox en AppData Local).
  5. Reportes de errores y registros de Windows (`CrashDumps`, logs temporales).
- **Seguridad:** Manejar errores de acceso (`PermissionError`) sin detener el análisis.

### Etapa 7: Módulo Limpiador Seguro (`limpiador.py`)
- **Objetivo:** Eliminar de forma controlada los archivos seleccionados por el usuario.
- **Protocolo de Seguridad:**
  1. Comprobación previa de autorización del usuario.
  2. Eliminación archivo por archivo mediante `os.remove()` protegido por `try-except`.
  3. No borrar carpetas raíz de Windows ni carpetas del sistema.
  4. Vaciado seguro de la papelera con `SHEmptyRecycleBinW` únicamente si el usuario la seleccionó.
  5. Registro exacto del espacio y número de archivos efectivamente borrados.

### Etapa 8: Módulo de Interfaz Gráfica (`interfaz.py`)
- **Objetivo:** Crear una interfaz gráfica moderna, con tema oscuro y estilo tecnológico utilizando `tkinter` y `ttk`.
- **Componentes:**
  - Barra de almacenamiento en disco con porcentaje.
  - Lista de categorías con casillas de verificación (checkboxes) y detalles de tamaño.
  - Botones destacados: "Analizar Sistema" y "Limpiar Archivos Seleccionados".
  - Barra de progreso interactiva con mensaje en tiempo real.
  - Pestañas organizadas: Limpiador, Historial de Limpiezas y Seguridad/Ayuda.
  - Uso de hilos (`threading.Thread`) para evitar que la ventana se congele durante el análisis o limpieza.

### Etapa 9: Módulo Principal (`main.py`)
- **Objetivo:** Servir como punto de entrada de la aplicación, inicializar carpetas necesarias e iniciar el bucle principal (`mainloop`).

### Etapa 10: Pruebas y Depuración
- **Objetivo:** Verificar que el flujo completo funcione sin errores.
- **Comprobaciones:**
  - Detección correcta de temporales.
  - Cálculo exacto de tamaños.
  - Manejo de archivos bloqueados sin caídas del programa.
  - Verificación del guardado en `historial.json`.

### Etapa 11: Documentación Didáctica
- **Objetivo:** Redactar el archivo `README.md` y una guía detallada explicando cada archivo, cada función y cada `import` como para exponerlo en el colegio técnico.

### Etapa 12: Generación del Ejecutable (`.exe`)
- **Objetivo:** Compilar el proyecto con PyInstaller para que funcione en cualquier Windows sin instalar Python.
- **Archivos a crear:**
  - `generar_exe.bat`: Script automático para compilar con un solo clic.
  - `instalar_dependencias.bat`: Script para instalar librerías necesarias.
  - Verificación de la versión portable resultante en `dist/LimpiadorPC/`.
