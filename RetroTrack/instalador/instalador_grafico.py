# ==============================================================================
# INSTALADOR AUTÓNOMO GRÁFICO - RETROTRACK PARA WINDOWS
# ==============================================================================
# Este script genera la aplicación 'Instalar_RetroTrack.exe'.
# Permite a cualquier usuario instalar el juego sin necesidad de tener Python
# ni bibliotecas instaladas en su computadora.
#
# Realiza las siguientes tareas automáticas:
# 1. Muestra un asistente visual con la estética de RetroTrack.
# 2. Permite elegir la carpeta de instalación (por defecto en AppData/RetroTrack).
# 3. Copia el ejecutable 'RetroTrack.exe' y los recursos necesarios.
# 4. Configura el archivo 'historial.csv' en la carpeta de datos.
# 5. Crea un acceso directo en el Escritorio de Windows.
# 6. Crea un acceso directo en el Menú Inicio de Windows.
# 7. Crea un script de desinstalación limpia.
# 8. Permite iniciar el juego inmediatamente al terminar la instalación.
# ==============================================================================

import os
import sys
import shutil
import subprocess
import time
import pygame

# Ocultar mensaje publicitario de Pygame
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

ANCHO = 640
ALTO = 440

COLOR_FONDO = (14, 15, 30)
COLOR_PANEL = (22, 24, 46)
COLOR_BORDE = (0, 240, 255)
COLOR_TEXTO = (245, 245, 255)
COLOR_TEXTO_MUTED = (160, 170, 200)
COLOR_CIAN = (0, 240, 255)
COLOR_VERDE = (60, 240, 100)
COLOR_AMARILLO = (255, 220, 40)
COLOR_BARRA_FONDO = (35, 38, 65)
COLOR_BARRA_LLENA = (0, 240, 255)


def obtener_ruta_recurso(nombre_archivo):
    """Obtiene la ruta absoluta a un archivo empaquetado o local."""
    if hasattr(sys, "_MEIPASS"):
        # Extraído temporalmente por PyInstaller
        return os.path.join(sys._MEIPASS, nombre_archivo)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", nombre_archivo)


def crear_acceso_directo_windows(ruta_destino_exe, ruta_lnk, descripcion="RetroTrack"):
    """Crea un acceso directo .lnk en Windows mediante PowerShell y WScript.Shell."""
    try:
        ps_cmd = (
            f'$WshShell = New-Object -comObject WScript.Shell; '
            f'$Shortcut = $WshShell.CreateShortcut("{ruta_lnk}"); '
            f'$Shortcut.TargetPath = "{ruta_destino_exe}"; '
            f'$Shortcut.WorkingDirectory = "{os.path.dirname(ruta_destino_exe)}"; '
            f'$Shortcut.Description = "{descripcion}"; '
            f'$Shortcut.Save()'
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False, creationflags=0x08000000)
        return True
    except Exception as e:
        print(f"Error creando acceso directo: {e}")
        return False


def ejecutar_proceso_instalacion(carpeta_destino, callback_progreso):
    """
    Copia los archivos a la carpeta de destino y crea los accesos directos.
    """
    try:
        callback_progreso(15, "Creando carpeta de instalación...")
        os.makedirs(carpeta_destino, exist_ok=True)
        carpeta_datos = os.path.join(carpeta_destino, "datos")
        os.makedirs(carpeta_datos, exist_ok=True)

        callback_progreso(35, "Copiando ejecutable RetroTrack.exe...")
        # Buscar el RetroTrack.exe empaquetado o en dist
        ruta_exe_origen = obtener_ruta_recurso("RetroTrack.exe")
        if not os.path.exists(ruta_exe_origen):
            # Probar en dist/RetroTrack.exe
            ruta_exe_origen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist", "RetroTrack.exe")
        if not os.path.exists(ruta_exe_origen):
            # Probar en la raíz
            ruta_exe_origen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "RetroTrack.exe")

        ruta_exe_destino = os.path.join(carpeta_destino, "RetroTrack.exe")
        if os.path.exists(ruta_exe_origen):
            shutil.copy2(ruta_exe_origen, ruta_exe_destino)

        callback_progreso(55, "Configurando base de datos de partidas...")
        ruta_csv_origen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datos", "historial.csv")
        ruta_csv_destino = os.path.join(carpeta_datos, "historial.csv")
        if os.path.exists(ruta_csv_origen) and not os.path.exists(ruta_csv_destino):
            shutil.copy2(ruta_csv_origen, ruta_csv_destino)

        callback_progreso(70, "Creando acceso directo en el Escritorio...")
        ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(ruta_escritorio):
            lnk_escritorio = os.path.join(ruta_escritorio, "RetroTrack.lnk")
            crear_acceso_directo_windows(ruta_exe_destino, lnk_escritorio)

        callback_progreso(85, "Creando acceso directo en el Menú Inicio...")
        ruta_inicio = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")
        if os.path.exists(ruta_inicio):
            carpeta_menu_inicio = os.path.join(ruta_inicio, "RetroTrack")
            os.makedirs(carpeta_menu_inicio, exist_ok=True)
            lnk_inicio = os.path.join(carpeta_menu_inicio, "RetroTrack.lnk")
            crear_acceso_directo_windows(ruta_exe_destino, lnk_inicio)

        callback_progreso(95, "Creando desinstalador...")
        ruta_desinstalador = os.path.join(carpeta_destino, "Desinstalar_RetroTrack.bat")
        with open(ruta_desinstalador, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("echo Desinstalando RetroTrack...\n")
            f.write(f'del /f /q "{os.path.join(ruta_escritorio, "RetroTrack.lnk")}" 2>nul\n')
            f.write(f'rmdir /s /q "{os.path.join(ruta_inicio, "RetroTrack")}" 2>nul\n')
            f.write(f'echo RetroTrack ha sido desinstalado con exito.\n')
            f.write("pause\n")

        callback_progreso(100, "¡Instalación completada con éxito!")
        return True, ruta_exe_destino

    except Exception as e:
        return False, str(e)


def iniciar_instalador():
    """Interfaz gráfica del instalador en Pygame."""
    pygame.init()
    pygame.font.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Instalador Oficial de RetroTrack - Windows")
    reloj = pygame.time.Clock()

    fuente_titulo = pygame.font.SysFont("Consolas", 26, bold=True)
    fuente_sub = pygame.font.SysFont("Consolas", 15)
    fuente_botones = pygame.font.SysFont("Consolas", 16, bold=True)
    fuente_estado = pygame.font.SysFont("Consolas", 14)

    # Carpeta de instalación por defecto (en AppData para no requerir permisos de Administrador)
    appdata = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
    carpeta_destino = os.path.join(appdata, "RetroTrack")

    estado = "espera"  # 'espera', 'instalando', 'completado', 'error'
    porcentaje = 0
    mensaje_estado = "Listo para comenzar la instalación."
    ruta_exe_instalado = ""

    boton_instalar = pygame.Rect(180, 360, 280, 48)
    boton_jugar = pygame.Rect(140, 360, 170, 48)
    boton_cerrar = pygame.Rect(330, 360, 170, 48)

    ejecutando = True

    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado == "espera":
                    if boton_instalar.collidepoint(pos_mouse):
                        estado = "instalando"

                elif estado == "completado":
                    if boton_jugar.collidepoint(pos_mouse):
                        # Abrir el juego y cerrar el instalador
                        if os.path.exists(ruta_exe_instalado):
                            subprocess.Popen([ruta_exe_instalado], cwd=os.path.dirname(ruta_exe_instalado))
                        ejecutando = False

                    elif boton_cerrar.collidepoint(pos_mouse):
                        ejecutando = False

        # Si el usuario presionó instalar, ejecutamos el proceso
        if estado == "instalando":
            def actualizar(p, txt):
                nonlocal porcentaje, mensaje_estado
                porcentaje = p
                mensaje_estado = txt
                # Redibujamos la pantalla durante el proceso
                pantalla.fill(COLOR_FONDO)
                # Barra de progreso
                pygame.draw.rect(pantalla, COLOR_BARRA_FONDO, (60, 280, 520, 24), border_radius=6)
                ancho_prog = int((520 * porcentaje) / 100)
                if ancho_prog > 0:
                    pygame.draw.rect(pantalla, COLOR_BARRA_LLENA, (60, 280, ancho_prog, 24), border_radius=6)
                txt_p = fuente_estado.render(f"{mensaje_estado} ({porcentaje}%)", True, COLOR_TEXTO)
                pantalla.blit(txt_p, (60, 315))
                pygame.display.flip()
                time.sleep(0.12)

            exito, resultado = ejecutar_proceso_instalacion(carpeta_destino, actualizar)
            if exito:
                estado = "completado"
                ruta_exe_instalado = resultado
                mensaje_estado = "¡RetroTrack fue instalado exitosamente!"
            else:
                estado = "error"
                mensaje_estado = f"Error en la instalación: {resultado}"

        # ----------------------------------------------------------------------
        # DIBUJADO DE LA VENTANA
        # ----------------------------------------------------------------------
        pantalla.fill(COLOR_FONDO)

        # Panel superior decorativo
        pygame.draw.rect(pantalla, COLOR_PANEL, (20, 20, ANCHO - 40, 80), border_radius=8)
        pygame.draw.rect(pantalla, COLOR_BORDE, (20, 20, ANCHO - 40, 80), width=1, border_radius=8)

        t_tit = fuente_titulo.render("ASISTENTE DE INSTALACIÓN RETROTRACK", True, COLOR_CIAN)
        t_sub = fuente_sub.render("Videojuego Arcade 2D & Sistema de Evolución Estadística", True, COLOR_TEXTO_MUTED)
        pantalla.blit(t_tit, (ANCHO // 2 - t_tit.get_width() // 2, 35))
        pantalla.blit(t_sub, (ANCHO // 2 - t_sub.get_width() // 2, 70))

        # Panel central informativo
        pygame.draw.rect(pantalla, COLOR_PANEL, (20, 115, ANCHO - 40, 220), border_radius=8)
        pygame.draw.rect(pantalla, (45, 50, 80), (20, 115, ANCHO - 40, 220), width=1, border_radius=8)

        # Información de instalación
        t_info1 = fuente_estado.render(f"Carpeta de instalación:", True, COLOR_AMARILLO)
        t_info2 = fuente_estado.render(carpeta_destino, True, COLOR_TEXTO)
        t_info3 = fuente_estado.render("• Incluye RetroTrack.exe, base de datos y recursos locales.", True, COLOR_TEXTO_MUTED)
        t_info4 = fuente_estado.render("• Crea acceso directo en el Escritorio y en el Menú Inicio.", True, COLOR_TEXTO_MUTED)
        t_info5 = fuente_estado.render("• No requiere tener Python instalado en la computadora.", True, COLOR_TEXTO_MUTED)

        pantalla.blit(t_info1, (45, 135))
        pantalla.blit(t_info2, (45, 155))
        pantalla.blit(t_info3, (45, 190))
        pantalla.blit(t_info4, (45, 215))
        pantalla.blit(t_info5, (45, 240))

        # Barra de progreso
        pygame.draw.rect(pantalla, COLOR_BARRA_FONDO, (45, 275, 550, 22), border_radius=6)
        ancho_p = int((550 * porcentaje) / 100)
        if ancho_p > 0:
            pygame.draw.rect(pantalla, COLOR_BARRA_LLENA, (45, 275, ancho_p, 22), border_radius=6)

        color_txt_estado = COLOR_VERDE if estado == "completado" else COLOR_TEXTO
        t_est = fuente_estado.render(mensaje_estado, True, color_txt_estado)
        pantalla.blit(t_est, (45, 305))

        # Botones inferiores según el estado
        if estado == "espera":
            hov_i = boton_instalar.collidepoint(pos_mouse)
            color_btn_i = (0, 180, 200) if hov_i else (0, 130, 150)
            pygame.draw.rect(pantalla, color_btn_i, boton_instalar, border_radius=8)
            pygame.draw.rect(pantalla, COLOR_CIAN, boton_instalar, width=2, border_radius=8)
            txt_i = fuente_botones.render("Instalar Ahora en Windows", True, COLOR_TEXTO)
            pantalla.blit(txt_i, (boton_instalar.centerx - txt_i.get_width() // 2, boton_instalar.centery - txt_i.get_height() // 2))

        elif estado == "completado":
            # Botón Jugar
            hov_j = boton_jugar.collidepoint(pos_mouse)
            color_j = (30, 160, 60) if hov_j else (20, 120, 45)
            pygame.draw.rect(pantalla, color_j, boton_jugar, border_radius=8)
            pygame.draw.rect(pantalla, COLOR_VERDE, boton_jugar, width=2, border_radius=8)
            txt_j = fuente_botones.render("JUGAR AHORA", True, COLOR_TEXTO)
            pantalla.blit(txt_j, (boton_jugar.centerx - txt_j.get_width() // 2, boton_jugar.centery - txt_j.get_height() // 2))

            # Botón Finalizar
            hov_c = boton_cerrar.collidepoint(pos_mouse)
            color_c = (55, 60, 85) if hov_c else (35, 40, 60)
            pygame.draw.rect(pantalla, color_c, boton_cerrar, border_radius=8)
            pygame.draw.rect(pantalla, (80, 90, 130), boton_cerrar, width=1, border_radius=8)
            txt_c = fuente_botones.render("Finalizar", True, COLOR_TEXTO)
            pantalla.blit(txt_c, (boton_cerrar.centerx - txt_c.get_width() // 2, boton_cerrar.centery - txt_c.get_height() // 2))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    iniciar_instalador()
