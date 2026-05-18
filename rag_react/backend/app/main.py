import sys
import os
from fastapi import FastAPI, Depends, Request, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.schemas import FiltrosRequest, ConsultaRagRequest, BivariadoRequest
from app.auth import (
    get_authenticated_user, verify_password, create_session_token,
    invalidate_session_token, SESSION_COOKIE_NAME
)
from app.services import RagService

# ─── RATE LIMITER ──────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="RAG Tenderos Tolima API",
    description="API Segura de alto rendimiento para el RAG Psicométrico y Demográfico",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ─── SECURITY HEADERS MIDDLEWARE ───────────────────────────
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# ─── CORS ──────────────────────────────────────────────────
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://tenderos.ddns.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

service = RagService()

# ─── AUTENTICACIÓN ─────────────────────────────────────────
class LoginRequest(BaseModel):
    password: str

@app.post("/auth/login", tags=["Autenticación"])
@limiter.limit("10/minute")
def login(request: Request, body: LoginRequest, response: Response):
    if not verify_password(body.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta.")
    
    token = create_session_token()
    is_https = request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,       # JavaScript NO puede leer esta cookie
        secure=is_https,     # True en producción HTTPS, False en desarrollo HTTP
        samesite="lax",      # Protección CSRF
        max_age=86400,       # 24 horas
        path="/"
    )
    return {"status": "ok", "message": "Sesión iniciada correctamente."}

@app.post("/auth/logout", tags=["Autenticación"])
def logout(request: Request, response: Response):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        invalidate_session_token(token)
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return {"status": "ok", "message": "Sesión cerrada."}

@app.get("/auth/check", tags=["Autenticación"])
def check_session(request: Request):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        from app.auth import validate_session_token
        if validate_session_token(token):
            return {"authenticated": True}
    return {"authenticated": False}

# ─── ENDPOINTS DE LA API (protegidos por cookie o API key) ─
@app.get("/api/v1/health", tags=["Health"])
@limiter.limit("30/minute")
def health_check(request: Request):
    return {"status": "online", "message": "API RAG Segura en operación", "db_connected": service.total_n > 0}

@app.get("/api/v1/filtros/opciones", tags=["Filtros"], dependencies=[Depends(get_authenticated_user)])
@limiter.limit("60/minute")
def obtener_opciones(request: Request):
    return service.obtener_opciones_filtros()

@app.post("/api/v1/filtros/kpis", tags=["Métricas"], dependencies=[Depends(get_authenticated_user)])
@limiter.limit("60/minute")
def obtener_kpis(request: Request, req: FiltrosRequest):
    return service.obtener_kpis(req)

@app.post("/api/v1/filtros/bivariado", tags=["Estadística Bivariada"], dependencies=[Depends(get_authenticated_user)])
@limiter.limit("30/minute")
def calcular_bivariado(request: Request, req: BivariadoRequest):
    return service.calcular_bivariado(req)

@app.post("/api/v1/filtros/exportar", tags=["Exportación"], dependencies=[Depends(get_authenticated_user)])
@limiter.limit("10/minute")
def exportar_datos(request: Request, req: FiltrosRequest):
    return service.exportar_microdatos(req)

@app.post("/api/v1/rag/consulta", tags=["RAG IA"], dependencies=[Depends(get_authenticated_user)])
@limiter.limit("5/minute")
def consulta_rag(request: Request, req: ConsultaRagRequest):
    return service.ejecutar_consulta_rag(req.consigna, req.filtros)

# ─── SERVIR FRONTEND ESTÁTICO (React build) ────────────────
dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

if os.path.isdir(dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_dir, "assets")), name="static-assets")
    
    @app.get("/uniminuto_logo.png")
    def serve_logo():
        logo_path = os.path.join(dist_dir, "uniminuto_logo.png")
        if os.path.isfile(logo_path):
            return FileResponse(logo_path)
        return {"error": "Logo not found"}

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = os.path.join(dist_dir, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(dist_dir, "index.html"))
