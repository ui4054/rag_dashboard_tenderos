# 🏪 Sistema RAG Psicométrico y Analítico - Tenderos del Norte del Tolima

Plataforma científica, analítica e interactiva para la investigación psicométrica y socioeconómica de micronegocios tradicionales (tenderos), impulsada por Inteligencia Artificial Generativa (RAG) y motores analíticos de alto rendimiento.

## 🚀 Características y Arquitectura Visual
- **Estadística No Paramétrica Robusta:** Transición metodológica completa al coeficiente $\rho$ (rho) de Spearman, adaptado con precisión matemática para escalas ordinales de Likert.
- **Núcleo de Análisis Combinatorio (Hipercubo):** Algoritmo de agrupamiento multidimensional en DuckDB que identifica de forma automática los picos y valles de resiliencia y riesgo comercial, evaluando la sensibilidad muestral exacta ($N$).
- **Dashboard Modular de React:** Interfaz de usuario compacta y de estética premium (Glassmorphism), con gráficas de dispersión nativas en SVG, anillos demográficos en gradientes cónicos y exploración dinámica de microdatos.

## 🏗️ Estructura del Repositorio
```
rag_git_consulta/
├── 01_cerebro/          # Manuscritos teóricos e IMRyD indexados para Full Text Search
├── 02_evidencia/        # Datos limpios de la muestra (data_cleaned.csv)
├── 04_motor/            # Scripts del motor de DuckDB y Vista de Oro
├── rag_react/           # Código fuente completo:
│   ├── backend/         # API en FastAPI (Protegida por cookies HttpOnly y SlowAPI)
│   └── frontend/        # SPA en React / Vite / Tailwind / Lucide Icons
├── agente_maestro.py    # Lógica de razonamiento RAG y protección de propiedad intelectual
└── preparar_motor.py    # Script de inicialización e ingesta de DuckDB
```

## 🛠️ Guía Rápida de Instalación (Local / Desarrollo)

### 1. Ingesta de Datos y Motor
Asegúrate de tener Python 3.11+ instalado. Clona el repositorio e instala las dependencias:
```bash
pip install -r requirements.txt
```
Configura tu clave de API copiando el archivo de ejemplo:
```bash
cp .env.example .env
# Ingresa tu GEMINI_API_KEY en el archivo .env
```
Ejecuta la ingesta para que DuckDB construya la base de datos local a partir del CSV:
```bash
python preparar_motor.py
```

### 2. Despliegue del Servidor Web (FastAPI + React SPA)
Para desarrollo del frontend en React:
```bash
cd rag_react/frontend
npm install
npm run dev
```

Para compilar y correr el servidor de producción unificado en FastAPI:
```bash
cd rag_react/frontend
npm run build
cd ../backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Abre tu navegador en [http://localhost:8000](http://localhost:8000).

## 🛡️ Estándar de Seguridad y Privacidad
El repositorio está configurado con un estricto archivo `.gitignore` para prevenir la fuga de certificados SSL y llaves de API. La autenticación en producción emplea cookies seguras de sesión `HttpOnly` inyectadas por middleware, y cada endpoint cuenta con limitadores de tasa por IP.
