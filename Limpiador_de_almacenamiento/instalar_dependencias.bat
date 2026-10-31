@echo off
chcp 65001 > nul
title Instalador de Dependencias - Limpiador de Espacio para Windows

echo ==============================================================
echo    INSTALADOR DE DEPENDENCIAS - LIMPIADOR DE ESPACIO
echo       Proyecto de 3.º Año - Orientación Programación
echo ==============================================================
echo.
echo Comprobando la instalación de Python en el equipo...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] No se encontró Python instalado en el sistema.
        echo Por favor, instalá Python desde https://www.python.org/
        echo y asegurate de marcar la casilla "Add Python to PATH".
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo [OK] Python detectado: 
%PYTHON_CMD% --version
echo.
echo Instalando dependencias desde 'requirements.txt'...
echo.

%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install -r requirements.txt

echo.
echo ==============================================================
echo    ¡Instalación completada exitosamente!
echo    Ya podés ejecutar el programa con: %PYTHON_CMD% main.py
echo ==============================================================
echo.
pause
