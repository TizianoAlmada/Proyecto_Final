; ==============================================================================
; SCRIPT DE CONFIGURACIÓN DE INNO SETUP - RETROTRACK
; ==============================================================================
; Este archivo permite compilar el instalador profesional 'Instalar_RetroTrack.exe'
; utilizando la herramienta gratuita Inno Setup (versión 6 o superior).
;
; Funcionalidades del instalador:
; 1. Asistente visual paso a paso con selección de idioma y carpeta de destino.
; 2. Instalación de 'RetroTrack.exe', recursos y carpetas de datos.
; 3. Creación de accesos directos en el Escritorio y en el Menú Inicio.
; 4. Registro de desinstalador automático en el Panel de Control de Windows.
; 5. Opción de iniciar RetroTrack inmediatamente al terminar la instalación.
; ==============================================================================

[Setup]
; Información de la aplicación
AppId={{D374A1B2-841F-4682-A723-9A1F8C9D32E5}
AppName=RetroTrack
AppVersion=2.0
AppVerName=RetroTrack v2.0 (Odisea Espacial)
AppPublisher=Alumno de 3.º año de Programación
DefaultDirName={autopf}\RetroTrack
DefaultGroupName=RetroTrack
AllowNoIcons=yes
OutputDir=C:\RetroTrack\instalador
OutputBaseFilename=Instalar_RetroTrack_InnoSetup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Archivo ejecutable principal
Source: "C:\RetroTrack\dist\RetroTrack.exe"; DestDir: "{app}"; Flags: ignoreversion
; Carpeta de datos (historial y gráficos)
Source: "C:\RetroTrack\datos\*"; DestDir: "{userlocalappdata}\RetroTrack\datos"; Flags: ignoreversion recursesubdirs createallsubdirs
; Recursos del juego
Source: "C:\RetroTrack\recursos\*"; DestDir: "{app}\recursos"; Flags: ignoreversion recursesubdirs createallsubdirs
; Documentación técnica
Source: "C:\RetroTrack\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Acceso directo en el Menú Inicio
Name: "{group}\RetroTrack"; Filename: "{app}\RetroTrack.exe"
Name: "{group}\Desinstalar RetroTrack"; Filename: "{uninstallexe}"
; Acceso directo opcional en el Escritorio
Name: "{autodesktop}\RetroTrack"; Filename: "{app}\RetroTrack.exe"; Tasks: desktopicon

[Run]
; Opción para iniciar el juego al finalizar
Filename: "{app}\RetroTrack.exe"; Description: "{cm:LaunchProgram,RetroTrack}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpieza segura al desinstalar
Type: files; Name: "{app}\*.log"
