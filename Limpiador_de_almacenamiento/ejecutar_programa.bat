@echo off
chcp 65001 > nul
title Limpiador de Espacio para Windows

echo Iniciando Limpiador de Espacio...
echo.

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
    exit /b
)

python main.py >nul 2>&1
if %errorlevel% neq 0 (
    py main.py
)
