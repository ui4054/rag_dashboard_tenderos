@echo off
TITLE SERVIDOR BACKEND RAG - FASTAPI SEGURA (PUERTO 8000)
COLOR 0A
CLS

echo ============================================================
echo   INICIANDO BACKEND RAG SEGURO (FASTAPI)
echo ============================================================
echo [INFO] Asegurate de ejecutar este archivo como ADMINISTRADOR.
echo [INFO] Usando entorno Conda: rag_despliegue
echo [INFO] Escuchando solo en localhost (127.0.0.1:8000) - Inmune a escaneos externos
echo.

"%USERPROFILE%\.conda\envs\rag_despliegue\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
