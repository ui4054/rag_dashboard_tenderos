import React, { useState, useEffect, useCallback } from 'react';
import { apiService } from './services/api';
import { KpiCard } from './components/KpiCard';
import { Semaforo } from './components/Semaforo';
import { Demografias } from './components/Demografias';
import { HipercuboCards } from './components/HipercuboCards';
import { MicrodatosExplorer } from './components/MicrodatosExplorer';
import { RagTerminal } from './components/RagTerminal';
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
                <h1 className="dashboard-title">Análisis Mutivariado</h1>
                <p className="dashboard-subtitle">Tenderos del Norte del Tolima</p>
              </div>
              <button
                onClick={actualizarKpis}
                disabled={cargando}
                className="btn-sync"
              >
                <RefreshCw size={18} className={cargando ? "spin" : ""} />
                <span>{cargando ? 'Sincronizando...' : 'Actualizar'}</span>
              </button>
            </header>

            {/* FILA DE KPIS */}
            <section className="kpi-grid">
              <KpiCard title="Muestra Filtrada" value={datosKpis?.muestra_filtrada || 0} subvalue={`de ${datosKpis?.total_muestra || 0} total`} icon={Users} color="#0284c7" />
              <KpiCard title="Formalización" value={`${datosKpis?.perc_formalizacion || 0}%`} icon={ShieldCheck} color="#22c55e" isGauge maxGauge={100} />
              <KpiCard title="Resiliencia Media" value={(datosKpis?.resiliencia_media || 0).toFixed(2)} subvalue="/ 5.0 (Likert)" icon={Activity} color="#38bdf8" isGauge maxGauge={5} />
              <KpiCard title="Riesgo Medio" value={(datosKpis?.riesgo_media || 0).toFixed(2)} subvalue="/ 5.0 (Likert)" icon={AlertTriangle} color="#eab308" isGauge maxGauge={5} />
            </section>

            {/* TARJETAS DE HIPERCUBO (Picos y Valles) */}
            <HipercuboCards hipercubo={datosKpis?.hipercubo} />

            {/* DISTRIBUCION GEOGRAFICA Y DEMOGRAFICA */}
            <Demografias distribucion={datosKpis?.distribucion_demografica || {}} />

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
