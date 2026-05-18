import React from 'react';
import { Link } from 'react-router-dom';
import { TolimaMap } from './TolimaMap';
import {
  ArrowRight, Users, MapPin, Brain, BarChart3,
  Database, MessageSquare, Grid, TrendingUp, BookOpen, GraduationCap
} from 'lucide-react';
import '../styles/Landing.css';

export const LandingPage = () => {
  return (
    <div className="landing-page">

      {/* ═══════════ HERO SECTION ═══════════ */}
      <section className="hero-section">
        <div className="hero-badge">
          <span className="hero-badge-dot" />
          Visualización Preliminar — Investigación en Curso
        </div>

        <h1 className="hero-title">
          Factores Sociodemográficos, Estructurales y Psicométricos de la Formalización
        </h1>

        <p className="hero-subtitle">
          Un <em>Análisis Multivariado</em> del Sector Tendero del Norte del Tolima.
          Plataforma interactiva con inteligencia artificial (RAG) para explorar los datos
          psicométricos y demográficos de 100 tenderos en 6 municipios.
        </p>

        {/* Mapa SVG interactivo */}
        <TolimaMap />

        <Link to="/login" className="cta-button">
          Ingresar al Dashboard Analítico
          <ArrowRight size={22} />
        </Link>
      </section>

      {/* ═══════════ FICHA TÉCNICA ═══════════ */}
      <section className="info-section">
        <div className="section-divider" />
        <h2 className="section-title">Ficha Técnica del Estudio</h2>

        <div className="ficha-grid">
          <div className="ficha-card">
            <div className="ficha-icon"><Users size={24} /></div>
            <div className="ficha-number">100</div>
            <div className="ficha-label">Tenderos Encuestados</div>
          </div>
          <div className="ficha-card">
            <div className="ficha-icon"><MapPin size={24} /></div>
            <div className="ficha-number">6</div>
            <div className="ficha-label">Municipios del Norte del Tolima</div>
          </div>
          <div className="ficha-card">
            <div className="ficha-icon"><Brain size={24} /></div>
            <div className="ficha-number">15</div>
            <div className="ficha-label">Dimensiones Psicométricas</div>
          </div>
          <div className="ficha-card">
            <div className="ficha-icon"><BarChart3 size={24} /></div>
            <div className="ficha-number">ρ</div>
            <div className="ficha-label">Rho Spearman y Regresión OLS</div>
          </div>
        </div>

        <div className="ficha-disclaimer">
          ⚠️ Esta es una visualización preliminar con fines académicos e investigativos. Los datos y conclusiones están sujetos a revisión.
        </div>
      </section>

      {/* ═══════════ QUÉ ENCONTRARÁS ═══════════ */}
      <section className="info-section">
        <div className="section-divider" />
        <h2 className="section-title">¿Qué Encontrarás en el Dashboard?</h2>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon" style={{ background: 'rgba(34,197,94,0.15)', color: '#22c55e' }}>
              <TrendingUp size={22} />
            </div>
            <div className="feature-name">KPIs en Tiempo Real</div>
            <div className="feature-desc">
              Indicadores de formalización, resiliencia media y perfil de riesgo que reaccionan instantáneamente a cada filtro aplicado.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ background: 'rgba(99,102,241,0.15)', color: '#818cf8' }}>
              <Grid size={22} />
            </div>
            <div className="feature-name">Matriz de Correlación 15×15</div>
            <div className="feature-desc">
              Mapa de calor interactivo con coeficientes ρ de Spearman entre las 15 dimensiones psicométricas (escala Likert ordinal). Haz clic en cualquier celda para obtener el estadígrafo de regresión bivariada (OLS).
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ background: 'rgba(234,179,8,0.15)', color: '#eab308' }}>
              <BarChart3 size={22} />
            </div>
            <div className="feature-name">Hipercubo Multidimensional</div>
            <div className="feature-desc">
              Diagnóstico automático de Picos de Riesgo y Valles de Resiliencia basado en el análisis combinatorio del espacio de filtros.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ background: 'rgba(236,72,153,0.15)', color: '#ec4899' }}>
              <MessageSquare size={22} />
            </div>
            <div className="feature-name">Terminal RAG con IA (Gemini)</div>
            <div className="feature-desc">
              Motor de Generación Aumentada por Recuperación con búsqueda BM25 sobre datos reales. Haz preguntas en lenguaje natural y obtén respuestas con fundamento estadístico.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ background: 'rgba(2,132,199,0.15)', color: '#0ea5e9' }}>
              <Database size={22} />
            </div>
            <div className="feature-name">Explorador de Microdatos</div>
            <div className="feature-desc">
              Visualiza la tabla completa de registros en crudo y exporta la submuestra filtrada como archivo CSV para análisis externo en SPSS, R o Excel.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ background: 'rgba(20,184,166,0.15)', color: '#14b8a6' }}>
              <BookOpen size={22} />
            </div>
            <div className="feature-name">Semáforo Psicométrico</div>
            <div className="feature-desc">
              Clasificación visual ALTO / PROMEDIO / BAJO de las 15 dimensiones según la media muestral, con distribución demográfica interactiva por edad, educación, estrato e ingresos.
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════ INVESTIGADORES ═══════════ */}
      <section className="info-section">
        <div className="section-divider" />
        <h2 className="section-title">Equipo Investigador</h2>

        <div className="researchers-grid">
          <div className="researcher-card">
            <div className="researcher-avatar">MM</div>
            <div className="researcher-name">Miguel Martínez</div>
            <div className="researcher-role">Investigador Principal</div>
            <div className="researcher-location">
              <MapPin size={14} /> Lérida, Tolima
            </div>
          </div>
          <div className="researcher-card">
            <div className="researcher-avatar">EC</div>
            <div className="researcher-name">Erika Conde</div>
            <div className="researcher-role">Co-Investigadora</div>
            <div className="researcher-location">
              <MapPin size={14} /> Ibagué, Tolima
            </div>
          </div>
          <div className="researcher-card">
            <div className="researcher-avatar">
              <GraduationCap size={32} />
            </div>
            <div className="researcher-name">Estudiantes Álgebra Lineal</div>
            <div className="researcher-role">Semillero 2026-1A</div>
            <div className="researcher-location">
              <MapPin size={14} /> Lérida, Tolima
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════ FOOTER UNIVERSIDAD ═══════════ */}
      <footer className="university-footer">
        <img src="/uniminuto_logo.png" alt="UNIMINUTO" className="uni-logo" />
        <div className="uni-name">Corporación Universitaria Minuto de Dios — UNIMINUTO</div>
        <div className="uni-program">Programa de Investigación · Norte del Tolima · 2026</div>
      </footer>
    </div>
  );
};
