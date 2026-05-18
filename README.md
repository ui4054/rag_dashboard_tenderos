# 🏪 Sistema RAG Psicométrico y Analítico - Tenderos del Norte del Tolima

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Security](https://img.shields.io/badge/Security-HttpOnly_Cookies-22c55e?style=for-the-badge)

> **Plataforma  analítica e interactiva para la investigación  psicométrica y socioeconómica de micronegocios tradicionales (tenderos), impulsada por Inteligencia Artificial Generativa (RAG)**

Proyecto de investigación desarrollado en la **Corporación Universitaria Minuto de Dios — UNIMINUTO Lérida** (Programa de Investigación, Norte del Tolima). Diseñado para brindar un soporte gráfico e interactivo de apoyo al análisis  del proyecto**.

---

## 📊 Ficha Técnica del Estudio

| Atributo | Especificación | Descripción |
| :--- | :--- | :--- |
| **👥 Muestra Empírica** | **100 Tenderos** | Censo muestral depurado de micronegocios tradicionales. |
| **📍 Cobertura Geográfica** | **6 Municipios** | Lérida, Venadillo, Ambalema, Mariquita, Honda y Fresno (Norte del Tolima). |
| **🧠 Alcance Psicométrico** | **15 Dimensiones** | Formalización, contabilidad, resiliencia, asociatividad, entre otras (escala Likert). |
| **📈 Rigor Estadístico** | **Spearman $\rho$ & OLS** | Estadística no paramétrica robusta y regresiones de mínimos cuadrados ordinarios. |

---

## 🚀 Arquitectura Visual y Módulos del Dashboard

La plataforma destaca por una interfaz de usuario de estética premium (**Glassmorphism**), alta reactividad en tiempo real y una arquitectura modular que combina ciencia de datos con experiencia de usuario avanzada:

### 1. 📈 KPIs y Métricas en Tiempo Real
* Indicadores clave (Tasa de Formalización, Resiliencia Media, Perfil de Riesgo) que reaccionan instantáneamente ante cualquier combinación de filtros sociodemográficos (municipio, género, estrato, nivel educativo, rango de ingresos).

### 2. 🗺️ Matriz de Correlación 15×15 & Regresión Bivariada
* Mapa de calor interactivo que expone las correlaciones no paramétricas ($\rho$ de Spearman) entre las 15 dimensiones de estudio.


### 3. 🎲 Hipercubo Multidimensional (Análisis Combinatorio)
* Motor de consultas analíticas que explora automáticamente todas las combinaciones posibles de filtros sociodemográficos.
* Identifica y aísla de forma proactiva los **Picos de Riesgo** (segmentos con mayor vulnerabilidad comercial) y los **Valles de Resiliencia**, reportando la sensibilidad muestral exacta ($N$).

### 4. 🧠 Terminal RAG IA (Google Gemini)
* Sistema de **Generación Aumentada por Recuperación (RAG)** con indexación de literatura científica e IMRyD mediante el algoritmo **BM25**.
* Permite a los investigadores realizar consultas en lenguaje natural, obteniendo respuestas analíticas que sintetizan el marco teórico con la evidencia empírica filtrada en tiempo real.

### 5. 🚦 Semáforo Psicométrico y Anillos Demográficos
* Clasificación visual instantánea (ALTO / PROMEDIO / BAJO) para cada dimensión psicométrica según la media muestral.
* Desglose interactivo con anillos de distribución demográfica en gradientes cónicos.

### 6. 🗄️ Explorador de Microdatos anonimizados Exportable
* Vista tabular paginada de los registros limpios.
* Exportación directa de submuestras a **CSV** para análisis externo en software científico como SPSS, R, Python o Stata.

---

## 🏗️ Estructura del Repositorio e Ingeniería de Software

El proyecto sigue un diseño limpio que separa el motor de datos, el cerebro analítico y las capas de servicio:

```text
rag_git_consulta/
├── 01_cerebro/          # Manuscritos teóricos e IMRyD indexados para Full Text Search BM25
├── 02_evidencia/        # Datos limpios de la muestra empírica (data_cleaned.csv)
├── 04_motor/            # Base de datos embebida DuckDB y consultas de alto rendimiento
├── rag_react/           # Código fuente de la aplicación web unificada:
│   ├── backend/         # API en FastAPI robusta, segura y asíncrona
│   └── frontend/        # SPA en React 18 / Vite / CSS Glassmorphism / Lucide Icons
├── agente_maestro.py    # Núcleo de razonamiento RAG, orquestación y protección de PI
└── preparar_motor.py    # Script de inicialización, ingesta y estructuración de datos.
```

---

## 🛡️ Estándar de Seguridad y Producción

Al ser un proyecto apto para entornos de producción y exhibición en portafolios, implementa múltiples capas de seguridad y buenas prácticas de ingeniería:

* **Autenticación Robusta por Cookies HttpOnly:** El inicio de sesión emite tokens de sesión protegidos en cookies `HttpOnly` y `SameSite=Lax`, haciéndolos completamente invisibles al JavaScript del cliente e inmunes a ataques XSS y CSRF.
* **Limitación de Tasa (Rate Limiting):** Integración nativa de **SlowAPI** en FastAPI para limitar las peticiones por IP en cada endpoint, mitigando ataques de denegación de servicio (DDoS) y abusos del endpoint de IA.
* **Cabeceras de Seguridad HTTP:** Middleware dedicado que inyecta políticas estrictas (`HSTS`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`).
* **Protección de Credenciales:** Estructura configurada con `.env` y `.gitignore` para evitar la exposición de claves de API (Gemini) y certificados.

---

## 🛠️ Guía Rápida de Instalación y Despliegue Local

### 1. Preparación del Entorno y Motor de Datos
Asegúrate de contar con Python 3.11+. Clona el repositorio y prepara las dependencias:

```bash
git clone https://github.com/tu-usuario/rag_git_consulta.git
cd rag_git_consulta
pip install -r requirements.txt
```

Configura tus credenciales y clave de API copiando el archivo de ejemplo:
```bash
cp .env.example .env
# Edita el archivo .env e ingresa tu GEMINI_API_KEY
```

Construye la base de datos local de DuckDB a partir de la evidencia CSV:
```bash
python preparar_motor.py
```

### 2. Despliegue Unificado (Frontend SPA + Backend FastAPI)
Para compilar el frontend de React y servir todo el sistema a través del backend seguro en FastAPI:

```bash
# 1. Compilar el paquete de producción en React
cd rag_react/frontend
npm install
npm run build

# 2. Iniciar el servidor backend en FastAPI
cd ../backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Abre tu navegador en: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---
*2026.*
