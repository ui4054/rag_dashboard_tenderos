@echo off
TITLE DESPLIEGUE RAG - PUERTO 80
COLOR 0B
CLS


echo ============================================================
echo   DESPLEGANDO RAG EN PUERTO 80
echo ============================================================
echo [INFO] Asegurate de ejecutar este archivo como ADMINISTRADOR.
echo [INFO] Usando entorno Conda: rag_despliegue
echo.

:: Ejecutar streamlit en puerto 80 usando el entorno detectado
"%USERPROFILE%\.conda\envs\rag_despliegue\python.exe" -m streamlit run "%~dp0app_web.py" --server.port 80 --server.address 0.0.0.0

pause
