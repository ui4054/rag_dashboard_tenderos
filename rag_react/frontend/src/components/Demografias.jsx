import React from 'react';
import '../styles/Demografias.css';

export const DemografiasBarras = ({ distribucion = {} }) => {
  const { edad = {}, nodo = {} } = distribucion;

  const renderBarSection = (title, dataMap, color = "#0284c7") => {
    const entries = Object.entries(dataMap).sort((a,b)=>b[1]-a[1]);
    if (entries.length === 0) return null;
    
    const maxVal = Math.max(...entries.map(e => e[1]), 1);

    return (
      <div className="glass-card demo-card">
        <h4 className="demo-title">{title}</h4>
        <div className="demo-list">
          {entries.map(([label, count]) => {
            const perc = Math.round((count / maxVal) * 100);
            return (
              <div key={label} className="demo-item">
                <div className="demo-item-header">
                  <span className="demo-item-label">{label}</span>
                  <span className="demo-item-count" style={{ color }}>{count}</span>
                </div>
                <div className="demo-bar-track">
                  <div className="demo-bar-fill" style={{ width: `${perc}%`, backgroundColor: color }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
      {renderBarSection("Distribución Geográfica (Nodos)", nodo, "#8b5cf6")}
      {renderBarSection("Distribución por Edades", edad, "#0ea5e9")}
    </div>
  );
};

export const DemografiasDonuts = ({ distribucion = {} }) => {
  const { educacion = {}, estrato = {}, ingresos = {} } = distribucion;

  const renderDonutSection = (title, dataMap, baseColors) => {
    const entries = Object.entries(dataMap).sort((a,b)=>b[1]-a[1]);
    if (entries.length === 0) return null;
    const total = entries.reduce((a,b)=>a+b[1], 0);
    
    let currentDegree = 0;
    const conicStops = entries.map(([label, count], i) => {
      const percentage = (count / total) * 100;
      const start = currentDegree;
      const end = currentDegree + percentage;
      currentDegree = end;
      return `${baseColors[i % baseColors.length]} ${start}% ${end}%`;
    }).join(', ');

    return (
      <div className="glass-card demo-card" style={{ padding: '16px' }}>
        <h4 className="demo-title" style={{ marginBottom: '12px' }}>{title}</h4>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ 
            width: '76px', height: '76px', borderRadius: '50%', 
            background: `conic-gradient(${conicStops})`,
            position: 'relative', flexShrink: 0
          }}>
            <div style={{
              position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
              width: '46px', height: '46px', backgroundColor: 'var(--bg-secondary)', borderRadius: '50%'
            }} />
          </div>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {entries.map(([label, count], i) => (
              <div key={label} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: baseColors[i % baseColors.length] }} />
                <span style={{ color: 'var(--text-main)', flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={label}>{label}</span>
                <strong style={{ color: 'var(--text-muted)' }}>{count}</strong>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px', marginBottom: '24px' }}>
      {renderDonutSection("Nivel Educativo", educacion, ["#38bdf8", "#0284c7", "#0369a1", "#0c4a6e", "#e0f2fe"])}
      {renderDonutSection("Estrato Socioeconómico", estrato, ["#22c55e", "#16a34a", "#15803d", "#14532d", "#dcfce7"])}
      {renderDonutSection("Ingresos Mensuales", ingresos, ["#eab308", "#ca8a04", "#a16207", "#713f12", "#fef08a"])}
    </div>
  );
};
