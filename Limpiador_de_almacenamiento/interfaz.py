"""
Módulo: interfaz.py
Descripción: Interfaz gráfica moderna, tecnológica y amigable con el usuario.
Nivel: 3.º Año - Escuela Técnica en Programación

Este módulo utiliza:
- 'tkinter' y 'ttk': Para crear las ventanas, botones, tablas y barras de progreso.
- 'threading': Para ejecutar las tareas pesadas (analizar y limpiar) en segundo plano
  sin que la ventana se congele ni aparezca el mensaje "(No responde)".
- 'messagebox': Para mostrar alertas y cuadros de confirmación de seguridad.
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Importamos los otros módulos de nuestro proyecto
import utilidades
import almacenamiento
import analizador
import limpiador
import historial


# Paleta de colores de estilo tecnológico moderno (Dark Theme)
COLOR_FONDO = "#0d1117"        # Fondo principal oscuro
COLOR_TARJETA = "#161b22"      # Fondo de tarjetas y paneles
COLOR_BORDE = "#30363d"        # Bordes sutiles
COLOR_TEXTO = "#f0f6fc"        # Texto blanco suave
COLOR_TEXTO_SEC = "#8b949e"    # Texto secundario gris
COLOR_AZUL = "#38bdf8"         # Azul cian de acento tecnológico
COLOR_AZUL_BOTON = "#0284c7"   # Azul para botones de acción
COLOR_VERDE = "#10b981"        # Verde esmeralda para limpieza y éxito
COLOR_ROJO = "#ef4444"         # Rojo para advertencias o vaciar historial
COLOR_PROGRESO_FONDO = "#21262d" # Fondo de la barra de progreso


class VentanaPrincipal:
    """
    Clase principal que gestiona la ventana y la lógica de la interfaz gráfica.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Limpiador de Espacio para Windows - Versión Técnica")
        self.root.geometry("900x720")
        self.root.minsize(800, 600)
        self.root.configure(bg=COLOR_FONDO)
        
        # Establecer icono si existe
        ruta_icono = utilidades.obtener_ruta_recurso(os.path.join("recursos", "icono.ico"))
        if os.path.exists(ruta_icono):
            try:
                self.root.iconbitmap(ruta_icono)
            except Exception:
                pass
                
        # Variables de estado
        self.resultados_analisis = None
        self.esta_trabajando = False
        self.variables_checkbox = {}
        self.labels_info_categoria = {}
        
        # Configurar estilos visuales de ttk
        self._configurar_estilos()
        
        # Construir la interfaz
        self._crear_encabezado()
        self._crear_tarjeta_almacenamiento()
        self._crear_pestanas()
        
        # Centrar la ventana en la pantalla del usuario
        self._centrar_ventana()
        
        # Cargar los datos del almacenamiento al iniciar
        self.actualizar_info_almacenamiento()

    def _configurar_estilos(self):
        """Configura los estilos oscuros para los componentes de ttk."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configuración general de pestañas (Notebook)
        self.style.configure('TNotebook', background=COLOR_FONDO, borderwidth=0)
        self.style.configure(
            'TNotebook.Tab',
            background=COLOR_TARJETA,
            foreground=COLOR_TEXTO_SEC,
            padding=[16, 8],
            font=('Segoe UI', 10, 'bold')
        )
        self.style.map(
            'TNotebook.Tab',
            background=[('selected', COLOR_FONDO)],
            foreground=[('selected', COLOR_AZUL)]
        )
        
        # Configuración de la barra de progreso
        self.style.configure(
            'Tecno.Horizontal.TProgressbar',
            background=COLOR_AZUL,
            troughcolor=COLOR_PROGRESO_FONDO,
            borderwidth=0,
            thickness=14
        )
        
        # Configuración de la tabla de historial (Treeview)
        self.style.configure(
            'Treeview',
            background=COLOR_TARJETA,
            foreground=COLOR_TEXTO,
            fieldbackground=COLOR_TARJETA,
            borderwidth=0,
            font=('Segoe UI', 9),
            rowheight=26
        )
        self.style.configure(
            'Treeview.Heading',
            background=COLOR_FONDO,
            foreground=COLOR_AZUL,
            font=('Segoe UI', 9, 'bold'),
            relief='flat'
        )
        self.style.map('Treeview', background=[('selected', COLOR_AZUL_BOTON)])

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla física."""
        self.root.update_idletasks()
        ancho = 900
        alto = 720
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ==========================================
    # COMPONENTES VISUALES
    # ==========================================

    def _crear_encabezado(self):
        """Crea la barra superior con el título y subtítulo del programa."""
        frame_header = tk.Frame(self.root, bg=COLOR_FONDO, padx=20, pady=12)
        frame_header.pack(fill=tk.X)
        
        titulo = tk.Label(
            frame_header,
            text="🛡️ LIMPIADOR DE ESPACIO PARA WINDOWS",
            font=('Segoe UI', 15, 'bold'),
            fg=COLOR_AZUL,
            bg=COLOR_FONDO
        )
        titulo.pack(anchor='w')
        
        subtitulo = tk.Label(
            frame_header,
            text="Mantenimiento Seguro del Almacenamiento - Proyecto de 3.º Año de Programación",
            font=('Segoe UI', 9),
            fg=COLOR_TEXTO_SEC,
            bg=COLOR_FONDO
        )
        subtitulo.pack(anchor='w')

    def _crear_tarjeta_almacenamiento(self):
        """Crea el panel que muestra el estado de uso del disco duro."""
        frame_borde = tk.Frame(self.root, bg=COLOR_BORDE, padx=1, pady=1)
        frame_borde.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        frame_disco = tk.Frame(frame_borde, bg=COLOR_TARJETA, padx=16, pady=12)
        frame_disco.pack(fill=tk.X)
        
        # Fila superior de la tarjeta: Título de unidad y selector
        fila_titulo = tk.Frame(frame_disco, bg=COLOR_TARJETA)
        fila_titulo.pack(fill=tk.X, pady=(0, 8))
        
        lbl_disco = tk.Label(
            fila_titulo,
            text="💾 Estado del Disco Duro Principal",
            font=('Segoe UI', 11, 'bold'),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA
        )
        lbl_disco.pack(side=tk.LEFT)
        
        # Selector de unidad
        unidades = almacenamiento.obtener_unidades_disponibles()
        self.var_unidad = tk.StringVar(value=unidades[0] if unidades else "C:\\")
        
        combo_unidades = ttk.Combobox(
            fila_titulo,
            textvariable=self.var_unidad,
            values=unidades,
            state="readonly",
            width=6,
            font=('Segoe UI', 9)
        )
        combo_unidades.pack(side=tk.RIGHT)
        combo_unidades.bind("<<ComboboxSelected>>", lambda e: self.actualizar_info_almacenamiento())
        
        lbl_sel = tk.Label(
            fila_titulo,
            text="Unidad:",
            font=('Segoe UI', 9),
            fg=COLOR_TEXTO_SEC,
            bg=COLOR_TARJETA
        )
        lbl_sel.pack(side=tk.RIGHT, padx=6)
        
        # Barra gráfica visual (Canvas personalizado)
        self.canvas_barra = tk.Canvas(
            frame_disco,
            height=20,
            bg=COLOR_PROGRESO_FONDO,
            highlightthickness=0
        )
        self.canvas_barra.pack(fill=tk.X, pady=6)
        
        # Fila de estadísticas: Espacio Total, Usado y Libre
        fila_stats = tk.Frame(frame_disco, bg=COLOR_TARJETA)
        fila_stats.pack(fill=tk.X, pady=(4, 0))
        
        self.lbl_espacio_total = tk.Label(
            fila_stats,
            text="Total: Calculando...",
            font=('Segoe UI', 9),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA
        )
        self.lbl_espacio_total.pack(side=tk.LEFT, expand=True)
        
        self.lbl_espacio_usado = tk.Label(
            fila_stats,
            text="Ocupado: Calculando...",
            font=('Segoe UI', 9),
            fg=COLOR_AZUL,
            bg=COLOR_TARJETA
        )
        self.lbl_espacio_usado.pack(side=tk.LEFT, expand=True)
        
        self.lbl_espacio_libre = tk.Label(
            fila_stats,
            text="Disponible: Calculando...",
            font=('Segoe UI', 9),
            fg=COLOR_VERDE,
            bg=COLOR_TARJETA
        )
        self.lbl_espacio_libre.pack(side=tk.LEFT, expand=True)

    def _crear_pestanas(self):
        """Crea el panel de pestañas: Limpiador, Historial y Seguridad."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # 1. Pestaña Limpiador
        self.tab_limpiador = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.notebook.add(self.tab_limpiador, text="  🧹 Limpieza y Análisis  ")
        self._construir_pestana_limpiador()
        
        # 2. Pestaña Historial
        self.tab_historial = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.notebook.add(self.tab_historial, text="  📋 Historial de Limpiezas  ")
        self._construir_pestana_historial()
        
        # 3. Pestaña Seguridad y Ayuda
        self.tab_seguridad = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.notebook.add(self.tab_seguridad, text="  ℹ️ Seguridad y Acerca de  ")
        self._construir_pestana_seguridad()

    def _construir_pestana_limpiador(self):
        """Construye el contenido de la pestaña principal de análisis y limpieza."""
        # Panel superior de categorías
        lbl_instruccion = tk.Label(
            self.tab_limpiador,
            text="Seleccioná las categorías que querés analizar y limpiar:",
            font=('Segoe UI', 10, 'bold'),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        )
        lbl_instruccion.pack(anchor='w', pady=(8, 6))
        
        # Tarjeta contenedora de las opciones
        frame_borde_cat = tk.Frame(self.tab_limpiador, bg=COLOR_BORDE, padx=1, pady=1)
        frame_borde_cat.pack(fill=tk.X, pady=(0, 10))
        
        frame_cat = tk.Frame(frame_borde_cat, bg=COLOR_TARJETA, padx=12, pady=10)
        frame_cat.pack(fill=tk.X)
        
        # Lista de categorías disponibles
        categorias_definidas = [
            ("temp_usuario", "Archivos Temporales de Usuario", "Archivos temporales en AppData Local"),
            ("temp_windows", "Archivos Temporales de Windows", "Temporales del sistema y descargas de update"),
            ("papelera", "Papelera de Reciclaje", "Archivos eliminados pendientes de vaciar"),
            ("cache_navegadores", "Caché de Navegadores Web", "Caché de Chrome, Edge, Firefox y Brave"),
            ("reportes_logs", "Reportes de Error y Logs", "Archivos CrashDumps y volcados de error")
        ]
        
        for id_cat, nombre_cat, desc_cat in categorias_definidas:
            fila = tk.Frame(frame_cat, bg=COLOR_TARJETA)
            fila.pack(fill=tk.X, pady=3)
            
            var = tk.BooleanVar(value=True)
            self.variables_checkbox[id_cat] = var
            
            chk = tk.Checkbutton(
                fila,
                text=nombre_cat,
                variable=var,
                font=('Segoe UI', 9, 'bold'),
                fg=COLOR_TEXTO,
                bg=COLOR_TARJETA,
                activebackground=COLOR_TARJETA,
                activeforeground=COLOR_AZUL,
                selectcolor="#0f172a"
            )
            chk.pack(side=tk.LEFT)
            
            lbl_desc = tk.Label(
                fila,
                text=f"({desc_cat})",
                font=('Segoe UI', 8),
                fg=COLOR_TEXTO_SEC,
                bg=COLOR_TARJETA
            )
            lbl_desc.pack(side=tk.LEFT, padx=6)
            
            lbl_info = tk.Label(
                fila,
                text="Pendiente de análisis",
                font=('Segoe UI', 9),
                fg=COLOR_AZUL,
                bg=COLOR_TARJETA
            )
            lbl_info.pack(side=tk.RIGHT)
            self.labels_info_categoria[id_cat] = lbl_info
            
        # Botones pequeños para seleccionar / deseleccionar todos
        frame_sel_botones = tk.Frame(self.tab_limpiador, bg=COLOR_FONDO)
        frame_sel_botones.pack(fill=tk.X, pady=(0, 10))
        
        btn_sel_todo = tk.Button(
            frame_sel_botones,
            text="Marcar Todos",
            command=self._marcar_todos,
            font=('Segoe UI', 8),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA,
            relief='flat',
            padx=8,
            pady=2,
            cursor='hand2'
        )
        btn_sel_todo.pack(side=tk.LEFT, padx=(0, 6))
        
        btn_desel_todo = tk.Button(
            frame_sel_botones,
            text="Desmarcar Todos",
            command=self._desmarcar_todos,
            font=('Segoe UI', 8),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA,
            relief='flat',
            padx=8,
            pady=2,
            cursor='hand2'
        )
        btn_desel_todo.pack(side=tk.LEFT)
        
        # Botones Principales de Acción (Analizar y Limpiar)
        frame_acciones = tk.Frame(self.tab_limpiador, bg=COLOR_FONDO)
        frame_acciones.pack(fill=tk.X, pady=6)
        
        self.btn_analizar = tk.Button(
            frame_acciones,
            text="🔍  1. ANALIZAR SISTEMA",
            command=self.iniciar_analisis_en_hilo,
            font=('Segoe UI', 10, 'bold'),
            fg="#ffffff",
            bg=COLOR_AZUL_BOTON,
            activebackground="#0369a1",
            activeforeground="#ffffff",
            relief='flat',
            padx=18,
            pady=8,
            cursor='hand2'
        )
        self.btn_analizar.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.btn_limpiar = tk.Button(
            frame_acciones,
            text="🧹  2. LIMPIAR ARCHIVOS SELECCIONADOS",
            command=self.iniciar_limpieza_en_hilo,
            font=('Segoe UI', 10, 'bold'),
            fg="#ffffff",
            bg=COLOR_VERDE,
            activebackground="#059669",
            activeforeground="#ffffff",
            relief='flat',
            padx=18,
            pady=8,
            state=tk.DISABLED,
            cursor='hand2'
        )
        self.btn_limpiar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Barra de progreso y texto de estado
        self.progreso_barra = ttk.Progressbar(
            self.tab_limpiador,
            style='Tecno.Horizontal.TProgressbar',
            mode='determinate'
        )
        self.progreso_barra.pack(fill=tk.X, pady=(10, 4))
        
        self.lbl_estado = tk.Label(
            self.tab_limpiador,
            text="Listo para analizar. Hacé clic en 'Analizar Sistema' para comenzar.",
            font=('Segoe UI', 9),
            fg=COLOR_TEXTO_SEC,
            bg=COLOR_FONDO
        )
        self.lbl_estado.pack(anchor='w')
        
        # Consola / Resumen de resultados
        frame_consola_borde = tk.Frame(self.tab_limpiador, bg=COLOR_BORDE, padx=1, pady=1)
        frame_consola_borde.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        
        self.txt_consola = tk.Text(
            frame_consola_borde,
            bg="#090d13",
            fg=COLOR_TEXTO,
            insertbackground=COLOR_AZUL,
            font=('Consolas', 9),
            relief='flat',
            padx=10,
            pady=8
        )
        self.txt_consola.pack(fill=tk.BOTH, expand=True)
        self._escribir_consola("Sistema listo. Los análisis no modifican ningún archivo.")

    def _construir_pestana_historial(self):
        """Construye la vista de historial de limpiezas anteriores."""
        frame_top_hist = tk.Frame(self.tab_historial, bg=COLOR_FONDO)
        frame_top_hist.pack(fill=tk.X, pady=(10, 6))
        
        lbl_tit_hist = tk.Label(
            frame_top_hist,
            text="Registro de limpiezas ejecutadas en la computadora:",
            font=('Segoe UI', 10, 'bold'),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        )
        lbl_tit_hist.pack(side=tk.LEFT)
        
        btn_vaciar_hist = tk.Button(
            frame_top_hist,
            text="🗑️ Vaciar Historial",
            command=self._vaciar_historial,
            font=('Segoe UI', 8),
            fg="#ffffff",
            bg=COLOR_ROJO,
            relief='flat',
            padx=10,
            pady=3,
            cursor='hand2'
        )
        btn_vaciar_hist.pack(side=tk.RIGHT)
        
        btn_recargar_hist = tk.Button(
            frame_top_hist,
            text="🔄 Actualizar",
            command=self.cargar_datos_historial,
            font=('Segoe UI', 8),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA,
            relief='flat',
            padx=10,
            pady=3,
            cursor='hand2'
        )
        btn_recargar_hist.pack(side=tk.RIGHT, padx=6)
        
        # Tabla Treeview para mostrar el historial ordenado
        columnas = ("fecha", "archivos", "espacio", "categorias")
        self.tabla_historial = ttk.Treeview(
            self.tab_historial,
            columns=columnas,
            show='headings',
            selectmode='browse'
        )
        
        self.tabla_historial.heading("fecha", text="Fecha y Hora")
        self.tabla_historial.heading("archivos", text="Archivos Borrados")
        self.tabla_historial.heading("espacio", text="Espacio Recuperado")
        self.tabla_historial.heading("categorias", text="Categorías Limpiadas")
        
        self.tabla_historial.column("fecha", width=150, anchor='center')
        self.tabla_historial.column("archivos", width=120, anchor='center')
        self.tabla_historial.column("espacio", width=140, anchor='center')
        self.tabla_historial.column("categorias", width=380, anchor='w')
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.tab_historial, orient="vertical", command=self.tabla_historial.yview)
        self.tabla_historial.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(6, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(6, 10))
        
        # Cargar los datos actuales
        self.cargar_datos_historial()

    def _construir_pestana_seguridad(self):
        """Construye la pestaña educativa con las reglas de seguridad y explicación del proyecto."""
        frame_scroll = tk.Frame(self.tab_seguridad, bg=COLOR_FONDO)
        frame_scroll.pack(fill=tk.BOTH, expand=True, pady=10)
        
        txt_info = tk.Text(
            frame_scroll,
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO,
            font=('Segoe UI', 9),
            relief='flat',
            padx=16,
            pady=14,
            wrap=tk.WORD
        )
        txt_info.pack(fill=tk.BOTH, expand=True)
        
        texto_explicativo = (
            "🛡️ NORMAS DE SEGURIDAD ESTRICTAS DEL LIMPIADOR\n"
            "====================================================\n\n"
            "1. PROTECCIÓN DE ARCHIVOS PERSONALES:\n"
            "   - Este software NUNCA tocará tus documentos, fotos, videos, descargas o escritorio.\n"
            "   - Cada ruta es validada previamente mediante la función 'es_ruta_segura()'.\n\n"
            "2. EXCLUSIVIDAD DE CARPETAS TEMPORALES:\n"
            "   - Únicamente se examinan las carpetas destinadas por el sistema operativo para residuos\n"
            "     (Temp de Usuario, Temp de Windows, Caché de Navegadores y volcados CrashDumps).\n\n"
            "3. NO FORZAR ARCHIVOS EN USO:\n"
            "   - Si un archivo temporal está siendo utilizado en ese instante por un programa abierto,\n"
            "     Windows denegará el acceso. Nuestro código captura esa excepción de forma segura\n"
            "     (PermissionError) y continúa con el siguiente archivo sin congelarse ni cerrarse.\n\n"
            "4. CONFIRMACIÓN PREVIA:\n"
            "   - Jamás se borra nada de forma automática. El usuario siempre debe hacer clic en 'Limpiar'\n"
            "     y confirmar la acción en el cuadro de diálogo emergente.\n\n"
            "5. CONTROL DE LA PAPELERA:\n"
            "   - La papelera solo se consulta en el análisis. Solo se vacía si el usuario marca su casilla\n"
            "     y lo autoriza expresamente.\n\n"
            "----------------------------------------------------\n"
            "PROYECTO TÉCNICO: 3.º Año - Orientación en Programación\n"
            "Arquitectura modular: main.py, interfaz.py, analizador.py, limpiador.py,\n"
            "almacenamiento.py, historial.py, utilidades.py.\n"
        )
        txt_info.insert(tk.END, texto_explicativo)
        txt_info.configure(state=tk.DISABLED)

    # ==========================================
    # LÓGICA Y COMUNICACIÓN CON HILOS (THREADING)
    # ==========================================

    def _marcar_todos(self):
        """Marca todas las casillas de categorías."""
        for var in self.variables_checkbox.values():
            var.set(True)

    def _desmarcar_todos(self):
        """Desmarca todas las casillas de categorías."""
        for var in self.variables_checkbox.values():
            var.set(False)

    def _escribir_consola(self, mensaje):
        """Escribe un mensaje en la consola de texto de la interfaz."""
        self.txt_consola.insert(tk.END, f"{mensaje}\n")
        self.txt_consola.see(tk.END)

    def actualizar_info_almacenamiento(self):
        """Actualiza la barra y los textos de almacenamiento del disco seleccionado."""
        unidad = self.var_unidad.get()
        datos = almacenamiento.obtener_informacion_disco(unidad)
        
        self.lbl_espacio_total.configure(text=f"Total: {datos['total_formateado']}")
        self.lbl_espacio_usado.configure(text=f"Ocupado: {datos['usado_formateado']} ({datos['porcentaje_usado']}%)")
        self.lbl_espacio_libre.configure(text=f"Disponible: {datos['libre_formateado']} ({datos['porcentaje_libre']}%)")
        
        # Redibujar la barra Canvas
        self.root.update_idletasks()
        ancho = self.canvas_barra.winfo_width()
        alto = self.canvas_barra.winfo_height()
        
        self.canvas_barra.delete("all")
        if ancho > 1 and datos["total_bytes"] > 0:
            ancho_ocupado = int((datos["usado_bytes"] / datos["total_bytes"]) * ancho)
            # Dibujar rectángulo ocupado (azul tecnológico)
            self.canvas_barra.create_rectangle(0, 0, ancho_ocupado, alto, fill=COLOR_AZUL, width=0)
            # Dibujar texto de porcentaje en el centro
            self.canvas_barra.create_text(
                ancho // 2, alto // 2,
                text=f"{datos['porcentaje_usado']}% Ocupado",
                fill="#ffffff",
                font=('Segoe UI', 9, 'bold')
            )

    def cargar_datos_historial(self):
        """Carga y muestra los registros guardados en 'datos/historial.json'."""
        # Limpiar filas existentes
        for fila in self.tabla_historial.get_children():
            self.tabla_historial.delete(fila)
            
        registros = historial.cargar_historial()
        for reg in registros:
            categorias_str = ", ".join(reg.get("categorias", []))
            self.tabla_historial.insert(
                "",
                tk.END,
                values=(
                    reg.get("fecha", ""),
                    reg.get("archivos_eliminados", 0),
                    reg.get("espacio_formateado", "0 B"),
                    categorias_str
                )
            )

    def _vaciar_historial(self):
        """Pide confirmación y vacía el historial."""
        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de que querés vaciar todo el historial de limpiezas?",
            icon='warning'
        )
        if confirmar:
            historial.vaciar_historial()
            self.cargar_datos_historial()
            messagebox.showinfo("Historial", "El historial ha sido vaciado correctamente.")

    # -----------------
    # HILO DE ANÁLISIS
    # -----------------
    def iniciar_analisis_en_hilo(self):
        """Inicia el análisis en un hilo secundario para no congelar la pantalla."""
        if self.esta_trabajando:
            return
            
        self.esta_trabajando = True
        self.btn_analizar.configure(state=tk.DISABLED)
        self.btn_limpiar.configure(state=tk.DISABLED)
        self.progreso_barra["value"] = 0
        self._escribir_consola("--- Iniciando Análisis del Sistema ---")
        
        # Creamos y lanzamos el hilo secundario
        hilo = threading.Thread(target=self._tarea_analisis, daemon=True)
        hilo.start()

    def _tarea_analisis(self):
        """Función que corre dentro del hilo secundario."""
        def callback_progreso(porcentaje, mensaje):
            # Usamos root.after para actualizar la interfaz de forma segura entre hilos
            self.root.after(0, self._actualizar_progreso_ui, porcentaje, mensaje)
            
        # Ejecutamos el análisis real
        self.resultados_analisis = analizador.analizar_sistema(callback_progreso)
        
        # Una vez completado, notificamos a la interfaz en el hilo principal
        self.root.after(0, self._finalizar_analisis_ui)

    def _actualizar_progreso_ui(self, porcentaje, mensaje):
        """Actualiza la barra de progreso y el texto de estado en la UI."""
        self.progreso_barra["value"] = porcentaje
        self.lbl_estado.configure(text=mensaje)

    def _finalizar_analisis_ui(self):
        """Actualiza los componentes de la interfaz cuando termina el análisis."""
        self.esta_trabajando = False
        self.btn_analizar.configure(state=tk.NORMAL)
        
        if self.resultados_analisis:
            total_archivos = self.resultados_analisis["total_archivos"]
            total_espacio = self.resultados_analisis["total_formateado"]
            
            # Actualizamos las etiquetas de cada categoría
            for id_cat, datos_cat in self.resultados_analisis["categorias"].items():
                if id_cat in self.labels_info_categoria:
                    self.labels_info_categoria[id_cat].configure(
                        text=f"{datos_cat['archivos']} archivos ({datos_cat['tamano_formateado']})",
                        fg=COLOR_TEXTO
                    )
                    
            self._escribir_consola(f"Análisis completado:")
            self._escribir_consola(f"-> Total archivos detectados: {total_archivos}")
            self._escribir_consola(f"-> Espacio recuperable: {total_espacio}")
            
            if total_archivos > 0:
                self.btn_limpiar.configure(state=tk.NORMAL)
                self.lbl_estado.configure(
                    text=f"Análisis completo: Se pueden recuperar {total_espacio} ({total_archivos} archivos)."
                )
            else:
                self.btn_limpiar.configure(state=tk.DISABLED)
                self.lbl_estado.configure(text="¡Tu sistema ya está limpio! No se encontraron archivos innecesarios.")

    # ------------------
    # HILO DE LIMPIEZA
    # ------------------
    def iniciar_limpieza_en_hilo(self):
        """Inicia el proceso de limpieza segura tras confirmar con el usuario."""
        if self.esta_trabajando or not self.resultados_analisis:
            return
            
        # Obtenemos las categorías marcadas con el checkbox
        categorias_a_limpiar = [
            id_cat for id_cat, var in self.variables_checkbox.items() if var.get()
        ]
        
        if not categorias_a_limpiar:
            messagebox.showwarning("Atención", "Por favor, seleccioná al menos una categoría para limpiar.")
            return
            
        # Calculamos cuánto espacio se liberará según las categorías seleccionadas
        bytes_estimados = 0
        archivos_estimados = 0
        nombres_seleccionados = []
        
        for id_cat in categorias_a_limpiar:
            if id_cat in self.resultados_analisis["categorias"]:
                cat = self.resultados_analisis["categorias"][id_cat]
                bytes_estimados += cat["bytes"]
                archivos_estimados += cat["archivos"]
                nombres_seleccionados.append(f"• {cat['nombre']} ({cat['tamano_formateado']})")
                
        mensaje_confirmacion = (
            f"¿Estás seguro de que deseás eliminar los archivos innecesarios?\n\n"
            f"Categorías seleccionadas:\n" + "\n".join(nombres_seleccionados) + "\n\n"
            f"Total aproximado a recuperar: {utilidades.formatear_tamano(bytes_estimados)}\n"
            f"Archivos a procesar: {archivos_estimados}\n\n"
            f"Nota: Los archivos en uso por el sistema o aplicaciones se omitirán de forma segura."
        )
        
        # Diálogo de confirmación de seguridad
        confirmar = messagebox.askyesno(
            "Confirmación de Limpieza Segura",
            mensaje_confirmacion,
            icon='question'
        )
        
        if not confirmar:
            return
            
        self.esta_trabajando = True
        self.btn_analizar.configure(state=tk.DISABLED)
        self.btn_limpiar.configure(state=tk.DISABLED)
        self.progreso_barra["value"] = 0
        self._escribir_consola("--- Iniciando Limpieza Segura ---")
        
        # Lanzamos el hilo de limpieza
        hilo = threading.Thread(
            target=self._tarea_limpieza,
            args=(categorias_a_limpiar,),
            daemon=True
        )
        hilo.start()

    def _tarea_limpieza(self, categorias_a_limpiar):
        """Función que ejecuta la limpieza dentro del hilo secundario."""
        def callback_progreso(porcentaje, mensaje):
            self.root.after(0, self._actualizar_progreso_ui, porcentaje, mensaje)
            
        resultado = limpiador.ejecutar_limpieza(
            self.resultados_analisis,
            categorias_a_limpiar,
            callback_progreso
        )
        
        self.root.after(0, self._finalizar_limpieza_ui, resultado)

    def _finalizar_limpieza_ui(self, resultado):
        """Actualiza la pantalla tras completar la limpieza."""
        self.esta_trabajando = False
        self.btn_analizar.configure(state=tk.NORMAL)
        self.btn_limpiar.configure(state=tk.DISABLED)
        
        archivos = resultado["archivos_eliminados"]
        espacio = resultado["espacio_formateado"]
        omitidos = resultado["archivos_omitidos"]
        
        self._escribir_consola(f"Limpieza finalizada con éxito:")
        self._escribir_consola(f"-> Archivos eliminados: {archivos}")
        self._escribir_consola(f"-> Espacio recuperado: {espacio}")
        if omitidos > 0:
            self._escribir_consola(f"-> Archivos omitidos (en uso o protegidos): {omitidos}")
            
        # Actualizamos la barra de almacenamiento y el historial
        self.actualizar_info_almacenamiento()
        self.cargar_datos_historial()
        
        # Reseteamos etiquetas de categorías
        for lbl in self.labels_info_categoria.values():
            lbl.configure(text="Pendiente de análisis", fg=COLOR_AZUL)
            
        self.resultados_analisis = None
        
        messagebox.showinfo(
            "Limpieza Completada",
            f"¡Operación exitosa!\n\n"
            f"• Archivos eliminados: {archivos}\n"
            f"• Espacio recuperado: {espacio}\n"
            f"• Archivos omitidos por estar en uso: {omitidos}\n\n"
            f"Los datos quedaron registrados en el Historial."
        )
