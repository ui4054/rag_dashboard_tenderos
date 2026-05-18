import React, { useState } from 'react';
import { Grid, BarChart2, Info, X, TrendingUp, RefreshCw, AlertTriangle } from 'lucide-react';
import { apiService } from '../services/api';
import '../styles/Semaforo.css';

export const Semaforo = ({ promedios = {}, matrizCorrelacion = {}, filtrosActivos = {} }) => {
  const [vistaActiva, setVistaActiva] = useState('unidimensional'); // 'matriz' | 'unidimensional'
  const [hoveredCell, setHoveredCell] = useState(null);

  // Estado para el modal de estadígrafo bivariado
  const [modalData, setModalData] = useState(null);
  const [cargandoModal, setCargandoModal] = useState(false);
  const [errorModal, setErrorModal] = useState('');

  const entradas = Object.entries(promedios);
  if (entradas.length === 0) return <div className="glass-card semaforo-container">No hay datos para calcular el semáforo ni la matriz.</div>;

  const valores = entradas.map(e => e[1]);
  const mediaGlobal = valores.reduce((a, b) => a + b, 0) / (valores.length || 1);

  const clasificar = (val) => {
    if (val >= mediaGlobal + 0.1) return { color: '#22c55e', bg: 'var(--success-bg)', border: 'var(--success-border)', label: 'ALTO' };
    if (val >= mediaGlobal - 0.1) return { color: '#eab308', bg: 'var(--warning-bg)', border: 'var(--warning-border)', label: 'PROMEDIO' };
    return { color: '#ef4444', bg: 'var(--danger-bg)', border: 'var(--danger-border)', label: 'BAJO' };
  };

  const getCellColor = (val) => {
    if (val === 1) return { bg: 'var(--border-color)', color: 'var(--text-main)' };

    const red = [239, 68, 68];
    const yellow = [250, 204, 21];
    const green = [22, 163, 74];

    let r, g, b;
    if (val >= 0) {
      const f = Math.min(val, 1);
      r = Math.round(yellow[0] + f * (green[0] - yellow[0]));
      g = Math.round(yellow[1] + f * (green[1] - yellow[1]));
      b = Math.round(yellow[2] + f * (green[2] - yellow[2]));
    } else {
      const f = Math.min(Math.abs(val), 1);
      r = Math.round(yellow[0] + f * (red[0] - yellow[0]));
      g = Math.round(yellow[1] + f * (red[1] - yellow[1]));
      b = Math.round(yellow[2] + f * (red[2] - yellow[2]));
    }
    
    const textColor = val <= -0.7 ? '#ffffff' : '#0f172a';
    return { bg: `rgb(${r}, ${g}, ${b})`, color: textColor };
  };

  const getNivelCorrelacionLabel = (val) => {
    if (val === 1) return 'Identidad (Misma Variable)';
    if (val >= 0.8) return 'Correlación Fuerte Positiva';
    if (val >= 0.3) return 'Correlación Moderada Positiva';
    if (val > -0.3) return 'Correlación Neutra / Sin Asociación';
    if (val > -0.8) return 'Correlación Moderada Negativa';
    return 'Correlación Fuerte Negativa';
  };

  const dimensiones = Object.keys(promedios);

  // Mapeo para acortar nombres en los encabezados sin perder claridad
  const acortarNombre = (nombre) => {
    const mapa = {
      "Gestión del Riesgo": "Gest. Riesgo",
      "Gestión Financiera": "Gest. Finan.",
      "Gestión Comercial y Mercadeo": "Comer. Merc.",
      "Gestión de Inventarios y Logística": "Inv. Logíst.",
      "Gestión Administrativa": "Administrat.",
      "Nodo de Significancia": "Nodo",
      "Antigüedad del Negocio": "Antigüedad",
      "Perfil de Riesgo": "Perf. Riesgo"
    };
    return mapa[nombre] || (nombre.length > 12 ? nombre.substring(0, 10) + '.' : nombre);
  };

  // Manejador al hacer clic en una celda de la matriz
  const handleCellClick = async (dim1, dim2) => {
    if (dim1 === dim2) return; // No calculamos regresión de una variable consigo misma
    setCargandoModal(true);
    setErrorModal('');
    setModalData(null);
    try {
      const stats = await apiService.calcularBivariado(dim1, dim2, filtrosActivos);
      if (stats.error) {
        setErrorModal(stats.error);
      } else {
        setModalData(stats);
      }
    } catch (err) {
      setErrorModal('Error calculando la métrica de asociación en el backend.');
    } finally {
      setCargandoModal(false);
    }
  };

  return (
    <div className="glass-card semaforo-container">
      <div className="semaforo-header-bar">
        <h3 className="semaforo-title">
          <Grid size={24} style={{ color: 'var(--accent-light)' }} />
          <span>Matriz de Cruce y Semáforo Psicométrico</span>
        </h3>
        <span className="semaforo-summary">
          Media muestral: <strong>{mediaGlobal.toFixed(2)}</strong> / 5.0
        </span>
      </div>

      <div className="semaforo-tabs">

        <button
          onClick={() => setVistaActiva('unidimensional')}
          className={`semaforo-tab-btn ${vistaActiva === 'unidimensional' ? 'active' : ''}`}
        >
          <BarChart2 size={18} />
          <span>Promedios Unidimensionales (15 Nodos)</span>
        </button>
        <button
          onClick={() => setVistaActiva('matriz')}
          className={`semaforo-tab-btn ${vistaActiva === 'matriz' ? 'active' : ''}`}
        >
          <Grid size={18} />
          <span>Matriz de Correlación (Cruce de Variables)</span>
        </button>
      </div>

      {vistaActiva === 'matriz' ? (
        <div>
          {Object.keys(matrizCorrelacion).length === 0 ? (
            <div style={{ color: 'var(--text-muted)' }}>La matriz de correlación requiere al menos 2 tenderos filtrados para calcularse.</div>
          ) : (
            <div className="matriz-wrapper">
              <table className="matriz-table">
                <thead>
                  <tr>
                    <th className="matriz-th matriz-th-left">Dimensiones</th>
                    {dimensiones.map((dim) => (
                      <th key={dim} className="matriz-th" title={dim}>
                        {acortarNombre(dim)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {dimensiones.map((dimFila) => (
                    <tr key={dimFila}>
                      <th className="matriz-th matriz-th-left" title={dimFila}>{acortarNombre(dimFila)}</th>
                      {dimensiones.map((dimCol) => {
                        const val = matrizCorrelacion[dimCol]?.[dimFila] ?? 0;
                        const cellStyle = getCellColor(val);
                        return (
                          <td
                            key={`${dimFila}-${dimCol}`}
                            className="matriz-cell"
                            style={{ background: cellStyle.bg, color: cellStyle.color }}
                            onMouseEnter={() => setHoveredCell({ d1: dimFila, d2: dimCol, val })}
                            onMouseLeave={() => setHoveredCell(null)}
                            onClick={() => handleCellClick(dimFila, dimCol)}
                            title={`Clic para analizar asociación ordinal (Spearman) entre ${dimFila} y ${dimCol}`}
                          >
                            {val.toFixed(2)}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="matriz-tooltip-box">
                <Info size={20} style={{ color: 'var(--accent-light)', flexShrink: 0 }} />
                {hoveredCell ? (
                  <div>
                    Cruce: <strong>{hoveredCell.d1}</strong> ↔ <strong>{hoveredCell.d2}</strong> | ρ Spearman: <strong style={{ color: getCellColor(hoveredCell.val).color, background: 'rgba(0,0,0,0.5)', padding: '2px 6px', borderRadius: '4px' }}>{hoveredCell.val.toFixed(2)}</strong> ({getNivelCorrelacionLabel(hoveredCell.val)}) | <em>Clic en la celda para analizar estadígrafo bivariado.</em>
                  </div>
                ) : (
                  <div style={{ color: 'var(--text-muted)' }}>Pasa el cursor sobre cualquier celda de la matriz para ver la fuerza de asociación. Haz clic en una celda para analizar la métrica bivariada robusta.</div>
                )}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="semaforo-grid">
          {entradas.map(([dim, val]) => {
            const cat = clasificar(val);
            return (
              <div key={dim} className="semaforo-card" style={{ background: cat.bg, borderLeft: `4px solid ${cat.border}` }}>
                <div className="semaforo-card-left">
                  <span className="semaforo-dot" style={{ background: cat.color, boxShadow: `0 0 8px ${cat.color}` }} />
                  <span className="semaforo-dim-name">{dim}</span>
                </div>
                <div className="semaforo-card-right">
                  <span className="semaforo-badge" style={{ color: cat.color }}>{cat.label}</span>
                  <span className="semaforo-value">{val.toFixed(2)}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* MODAL ESTADÍGRAFO BIVARIADO */}
      {(cargandoModal || modalData || errorModal) && (
        <div className="bivariado-modal-overlay" onClick={() => { setModalData(null); setErrorModal(''); setCargandoModal(false); }}>
          <div className="bivariado-modal-card" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <div>
                <h2 className="modal-title">Relación Bivariada Robusta</h2>
                <p className="modal-subtitle">Análisis de Correlación Ordinal (ρ de Spearman) sobre submuestra activa</p>
              </div>
              <button onClick={() => { setModalData(null); setErrorModal(''); setCargandoModal(false); }} className="btn-close-modal">
                <X size={20} />
              </button>
            </div>
            <div className="modal-body">
              {cargandoModal && (
                <div style={{ padding: '40px', textAlign: 'center', color: 'var(--accent-light)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
                  <RefreshCw size={36} className="spin" />
                  <p>Calculando métrica ordinal en Python (scipy.stats.spearmanr)...</p>
                </div>
              )}

              {errorModal && (
                <div style={{ padding: '24px', background: 'var(--danger-bg)', border: '1px solid var(--danger-border)', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '16px', color: '#ef4444' }}>
                  <AlertTriangle size={32} style={{ flexShrink: 0 }} />
                  <div>
                    <h4 style={{ fontWeight: '700', marginBottom: '4px' }}>Aviso Estadístico</h4>
                    <p style={{ color: 'var(--text-main)', fontSize: '0.9rem' }}>{errorModal}</p>
                  </div>
                </div>
              )}

              {modalData && (
                <div className="modal-compact-view">
                  <div className="modal-compact-header">
                    <div className="dim-name">{modalData.dim1}</div>
                    <TrendingUp size={16} style={{ color: 'var(--success-border)', margin: '0 8px', flexShrink: 0 }} />
                    <div className="dim-name">{modalData.dim2}</div>
                  </div>

                  <div className="stats-mini-grid">
                    <div className="stat-mini">
                      <span>ρ (rho)</span>
                      <strong style={{ color: (modalData.rho_spearman ?? modalData.r_pearson) > 0 ? '#22c55e' : '#ef4444' }}>{modalData.rho_spearman ?? modalData.r_pearson}</strong>
                    </div>
                    <div className="stat-mini">
                      <span>R²</span>
                      <strong>{(modalData.r_squared * 100).toFixed(1)}%</strong>
                    </div>
                    <div className="stat-mini">
                      <span>P-Value</span>
                      <strong style={{ color: modalData.p_value < 0.05 ? '#22c55e' : 'var(--text-muted)' }}>{modalData.p_value}</strong>
                    </div>
                    <div className="stat-mini">
                      <span>N</span>
                      <strong>{modalData.n_muestral}</strong>
                    </div>
                  </div>

                  <div className="interpretacion-mini">
                    <strong>Fuerza de Asociación:</strong> {getNivelCorrelacionLabel(modalData.rho_spearman ?? modalData.r_pearson)}.
                    {modalData.p_value < 0.05 ? <span style={{ color: '#22c55e', display: 'block', marginTop: '4px' }}>Estadísticamente Significativo (p &lt; 0.05).</span> : <span style={{ color: '#eab308', display: 'block', marginTop: '4px' }}>Asociación no significativa.</span>}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
