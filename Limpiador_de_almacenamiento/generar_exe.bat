@echo off
chcp 65001 > nul
title Generador de Ejecutable - Limpiador de Espacio para Windows

echo ==============================================================
echo    COMPILADOR DE EJECUTABLE .EXE - LIMPIADOR DE ESPACIO
echo       Proyecto de 3.º Año - Orientación Programación
echo ==============================================================
echo.
echo Comprobando entorno de Python y PyInstaller...
echo.

set PYINSTALLER_CMD=pyinstaller

if exist ".venv\Scripts\pyinstaller.exe" (
    set PYINSTALLER_CMD=.venv\Scripts\pyinstaller.exe
) else (
    pyinstaller --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] No se encontró PyInstaller instalado.
        echo Ejecutá primero 'instalar_dependencias.bat'.
        echo.
        pause
        exit /b 1
    )
)

echo [OK] PyInstaller detectado.
echo.
echo Compilando 'main.py' a ejecutable para Windows...
echo Por favor, esperá unos momentos...
echo.

%PYINSTALLER_CMD% --noconfirm --onedir --windowed --icon "recursos/icono.ico" --add-data "recursos;recursos" --name "LimpiadorPC" main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ocurrió un fallo durante la compilación.
    echo.
    pause
    exit /b %errorlevel%
)

echo.
echo Copiando carpeta inicial de datos a la versión portable...
if not exist "dist\LimpiadorPC\datos" (
    mkdir "dist\LimpiadorPC\datos"
)
copy /y "datos\historial.json" "dist\LimpiadorPC\datos\historial.json" > nul

echo ==============================================================
echo    ¡Compilación completada exitosamente!
echo.
echo    El programa listo para Windows se encuentra en:
echo    dist\LimpiadorPC\LimpiadorPC.exe
echo.
echo    ¡Podés copiar la carpeta 'dist\LimpiadorPC' a cualquier
echo    computadora con Windows y funcionará de forma portable!
echo ==============================================================
echo.
pause
