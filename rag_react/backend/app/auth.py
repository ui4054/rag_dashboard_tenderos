import os
import secrets
import hashlib
from fastapi import Security, HTTPException, status, Request, Response
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# Cargamos el .env desde el directorio raíz (subiendo 3 niveles desde backend/app/auth.py hasta el directorio raíz del repo)
root_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
load_dotenv(root_env_path)

# ─── CONFIGURACIÓN ─────────────────────────────────────────
# Contraseña de acceso al dashboard (hasheada en memoria, nunca en texto plano en el código fuente)
DASHBOARD_PASSWORD_HASH = hashlib.sha256("tolima2026".encode()).hexdigest()

# Nombre de la cookie de sesión
SESSION_COOKIE_NAME = "rag_session"

# Secreto para firmar tokens (generado al arrancar, cambia en cada reinicio = sesiones expiran)
SERVER_SECRET = os.getenv("SESSION_SECRET", secrets.token_urlsafe(32))

# Almacén de sesiones activas en memoria
active_sessions: set = set()

# API Key legacy para desarrollo/testing (fallback)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
LEGACY_API_KEY = os.getenv("RAG_API_KEY", "rag_secure_key_2026_x9182")

# ─── FUNCIONES DE SESIÓN ───────────────────────────────────
def create_session_token() -> str:
    """Genera un token de sesión criptográficamente seguro."""
    token = secrets.token_urlsafe(48)
    active_sessions.add(token)
    return token

def validate_session_token(token: str) -> bool:
    """Valida si un token de sesión existe en el almacén."""
    return token in active_sessions

def invalidate_session_token(token: str):
    """Elimina un token del almacén (logout)."""
    active_sessions.discard(token)

def verify_password(password: str) -> bool:
    """Verifica la contraseña contra el hash almacenado."""
    return hashlib.sha256(password.encode()).hexdigest() == DASHBOARD_PASSWORD_HASH

# ─── DEPENDENCIA DE AUTENTICACIÓN ─────────────────────────
def get_authenticated_user(request: Request, api_key: str = Security(api_key_header)) -> str:
    """
    Verifica la identidad del usuario mediante (en orden de prioridad):
    1. Cookie HttpOnly de sesión (navegador web)
    2. Header X-API-Key legacy (desarrollo/testing con curl)
    """
    # Prioridad 1: Cookie de sesión
    session_token = request.cookies.get(SESSION_COOKIE_NAME)
    if session_token and validate_session_token(session_token):
        return "authenticated_via_cookie"
    
    # Prioridad 2: API Key legacy (para desarrollo y testing)
    if api_key and api_key == LEGACY_API_KEY:
        return "authenticated_via_apikey"
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesión no válida. Inicia sesión en /login para acceder al dashboard.",
    )
