@echo off
TITLE PLATAFORMA WEB - INVESTIGACION TENDEROS
COLOR 0E
CLS


echo ============================================================
echo   PLATAFORMA WEB DE INVESTIGACION (STREAMLIT + PLOTLY)
echo ============================================================
echo.
echo [INFO] Iniciando Servidor Web Local (Modo Rapido)...
echo [INFO] El navegador se abrira automaticamente.
echo.

"%USERPROFILE%\.conda\envs\rag_despliegue\python.exe" -m streamlit run "%~dp0app_web.py" --server.fileWatcherType none

pause
