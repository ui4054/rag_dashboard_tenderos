@echo off
TITLE DESPLIEGUE RAG REACT - HTTPS PUERTO 443
COLOR 0A
CLS

echo ============================================================
echo   DESPLEGANDO RAG REACT + FASTAPI EN PUERTO 443 CON HTTPS
echo ============================================================
echo [INFO] Asegurate de ejecutar este archivo como ADMINISTRADOR.
echo [INFO] Usando entorno Conda: rag_despliegue
echo [INFO] Dominio: tenderos.ddns.net
echo [INFO] El frontend React se sirve desde FastAPI (dist/)
echo.

:: Primero compilar el frontend React (por si hay cambios)
echo [PASO 1/2] Compilando frontend React...
cd /d "%~dp0rag_react\frontend"
cmd /c "npm run build"
:: Copiar logo a dist
copy /Y public\uniminuto_logo.png dist\uniminuto_logo.png >NUL 2>&1

echo.
echo [PASO 2/2] Iniciando FastAPI con SSL en puerto 443...
echo.

:: Ejecutar Uvicorn con SSL apuntando a los certificados existentes
cd /d "%~dp0rag_react\backend"
"%USERPROFILE%\.conda\envs\rag_despliegue\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 443 --ssl-certfile "%~dp0certs\tenderos.ddns.net-chain.pem" --ssl-keyfile "%~dp0certs\tenderos.ddns.net-key-unencrypted.pem"

pause
