@echo off
REM Script de build y despliegue para Windows
REM Ejecutar desde la carpeta backend

echo.
echo ================================================
echo   SIGNANCE SYSTEM - BUILD Y DESPLIEGUE FRONTEND
echo ================================================
echo.

REM Verificar que Python esté disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instale Python primero.
    pause
    exit /b 1
)

REM Ejecutar el script de Python
echo Ejecutando script de build...
python build_and_deploy_frontend.py

REM Verificar resultado
if errorlevel 1 (
    echo.
    echo ERROR: El build falló. Revise los errores anteriores.
    pause
    exit /b 1
) else (
    echo.
    echo EXITO: Build completado correctamente.
    echo Presione cualquier tecla para continuar...
    pause >nul
)
