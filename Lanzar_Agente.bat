@echo off
TITLE CONSOLA AGENTICA - INVESTIGACION TENDEROS
COLOR 0B
CLS


echo ============================================================
echo   SISTEMA DE INVESTIGACION AGENTICA (ENTORNO RAG_CONSULTA)
echo ============================================================
echo.
echo [INFO] Iniciando Motor de Inteligencia (Llama3 + DuckDB)...
echo [INFO] Usando entorno: tenderos_rag_env (Python 3.11)
echo.

"%USERPROFILE%\.conda\envs\rag_despliegue\python.exe" "%~dp0agente_maestro.py"

echo.
echo [INFO] Sesion finalizada.
pause
