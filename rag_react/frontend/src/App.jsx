import React, { useState, useEffect, useCallback } from 'react';
import { apiService } from './services/api';
import { ExecutiveBanner } from './components/ExecutiveBanner';
import { Semaforo } from './components/Semaforo';
import { DemografiasBarras, DemografiasDonuts } from './components/Demografias';
import { HipercuboCards } from './components/HipercuboCards';
import { MicrodatosExplorer } from './components/MicrodatosExplorer';
import { RagTerminal } from './components/RagTerminal';
import { ThemeToggle } from './components/ThemeToggle';
import { Store, ShieldCheck, Activity, Users, AlertTriangle, Filter, RefreshCw } from 'lucide-react';
import './styles/App.css';

export default function App() {
  const [opcionesFiltros, setOpcionesFiltros] = useState({
    nodos: [], formalizacion: [], rango_edad: [], nivel_educativo: [], estrato: [], antiguedad_negocio: [], tipo_vivienda: []
  });

  const [filtrosSeleccionados, setFiltrosSeleccionados] = useState({
    nodos: [], formalizacion: [], rango_edad: [], nivel_educativo: [], estrato: [], antiguedad_negocio: [], tipo_vivienda: []
  });

  const [datosKpis, setDatosKpis] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const cargarOpciones = async () => {
      try {
        const opts = await apiService.obtenerOpcionesFiltros();
        setOpcionesFiltros(opts);
      } catch (err) {
        setError('No se pudo conectar al Backend Seguro local (127.0.0.1:8000). Asegúrate de haber iniciado Lanzar_API.bat');
        setCargando(false);
      }
    };
    cargarOpciones();
  }, []);

  const actualizarKpis = useCallback(async () => {
    setCargando(true);
    setError('');
    try {
      const kpis = await apiService.obtenerKpis(filtrosSeleccionados);
      setDatosKpis(kpis);
    } catch (err) {
      setError('Error al obtener datos de los tenderos. Comprueba que la API esté corriendo sin errores.');
    } finally {
      setCargando(false);
    }
  }, [filtrosSeleccionados]);

  useEffect(() => {
    actualizarKpis();
  }, [actualizarKpis]);

  const handleSelectChange = (campo, valor) => {
    setFiltrosSeleccionados(prev => {
      const actuales = prev[campo];
      const nuevos = actuales.includes(valor) ? actuales.filter(i => i !== valor) : [...actuales, valor];
      return { ...prev, [campo]: nuevos };
    });
  };

  const limpiarFiltros = () => {
    setFiltrosSeleccionados({ nodos: [], formalizacion: [], rango_edad: [], nivel_educativo: [], estrato: [], antiguedad_negocio: [], tipo_vivienda: [] });
  };

  return (
    <div className="app-container">
      {/* SIDEBAR DE FILTRADO */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <Store size={32} style={{ color: 'var(--accent-primary)' }} />
          <div>
            <h1 className="sidebar-title">Filtros</h1>
            <span className="sidebar-badge">
              <ShieldCheck size={14} /> Datos anonimizados
            </span>
          </div>
        </div>

        <div className="filter-control-bar">
          <span className="filter-active-label">
            <Filter size={16} /> Filtros Activos
          </span>
          <button onClick={limpiarFiltros} className="btn-clear-filters">
            Limpiar Todo
          </button>
        </div>

        <div className="filters-scroll-area">
          {Object.entries(opcionesFiltros).map(([campo, opciones]) => (
            <div key={campo} className="filter-group">
              <label className="filter-label">
                {campo.replace('_', ' ')} ({filtrosSeleccionados[campo].length})
              </label>
              <div className="filter-options-box">
                {opciones.map(opt => {
                  const seleccionado = filtrosSeleccionados[campo].includes(opt);
                  return (
                    <div
                      key={opt}
                      onClick={() => handleSelectChange(campo, opt)}
                      className={`filter-item ${seleccionado ? 'selected' : ''}`}
                    >
                      <span>{opt}</span>
                      {seleccionado && <span className="filter-dot" />}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </aside>

      {/* DASHBOARD PRINCIPAL */}
      <main className="main-dashboard">
        {error ? (
          <div className="alert-card">
            <AlertTriangle size={36} style={{ color: '#ef4444', flexShrink: 0 }} />
            <div>
              <h3 className="alert-title">Alerta de Conexión</h3>
              <p style={{ color: 'var(--text-main)', fontSize: '0.95rem' }}>{error}</p>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '8px' }}>Paso requerido: Abre una terminal de Windows y ejecuta el archivo <strong>Lanzar_API.bat</strong> en la carpeta rag_react\backend.</p>
            </div>
          </div>
        ) : (
          <>
            <header className="dashboard-header">
              <div>
                <h1 className="dashboard-title">Análisis Multivariado</h1>
                <p className="dashboard-subtitle">Tenderos del Norte del Tolima</p>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <ThemeToggle />
                <button
                  onClick={actualizarKpis}
                  disabled={cargando}
                  className="btn-sync"
                >
                  <RefreshCw size={18} className={cargando ? "spin" : ""} />
                  <span>{cargando ? 'Sincronizando...' : 'Actualizar'}</span>
                </button>
              </div>
            </header>

            {/* BANNER EJECUTIVO DE KPIS */}
            <ExecutiveBanner datosKpis={datosKpis} />

            {/* PANEL DUAL: HIPERCUBO (Izquierda) Y DEMOGRAFIA DE BARRAS (Derecha) */}
            <section className="executive-dual-panel" style={{ display: 'grid', gridTemplateColumns: '1fr 1.4fr', gap: '20px', marginBottom: '24px' }}>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <h3 style={{ fontSize: '0.85rem', fontWeight: '800', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '12px', letterSpacing: '0.08em' }}>
                  Núcleo de Análisis (Picos y Valles)
                </h3>
                <HipercuboCards hipercubo={datosKpis?.hipercubo} />
              </div>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <h3 style={{ fontSize: '0.85rem', fontWeight: '800', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '12px', letterSpacing: '0.08em' }}>
                  Distribución y Representatividad
                </h3>
                <DemografiasBarras distribucion={datosKpis?.distribucion_demografica || {}} />
              </div>
            </section>

            {/* SECCION DE DONUTS DEMOGRAFICOS */}
            <DemografiasDonuts distribucion={datosKpis?.distribucion_demografica || {}} />

            {/* SEMAFORO PSICOMETRICO Y MATRIZ DE CRUCE */}
            <Semaforo promedios={datosKpis?.promedios_psicometricos || {}} matrizCorrelacion={datosKpis?.matriz_correlacion || {}} filtrosActivos={filtrosSeleccionados} />

            {/* EXPLORADOR DE MICRODATOS Y EXPORTACION CSV */}
            <MicrodatosExplorer filtrosActivos={filtrosSeleccionados} />

            {/* TERMINAL RAG */}
            <RagTerminal filtrosActivos={filtrosSeleccionados} />
          </>
        )}
      </main>
    </div>
  );
}
