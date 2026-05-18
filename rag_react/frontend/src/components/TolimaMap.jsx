import React, { useState } from 'react';

const municipios = [
  {
    id: 'lerida', nombre: 'Lérida', n: 29, cobertura: '72.5%',
    path: 'M 210,140 L 250,120 L 280,135 L 290,170 L 260,190 L 225,185 L 205,165 Z',
    labelX: 248, labelY: 158
  },
  {
    id: 'mariquita', nombre: 'Mariquita', n: 18, cobertura: '14.3%',
    path: 'M 140,175 L 175,155 L 210,165 L 225,185 L 215,215 L 180,225 L 150,210 Z',
    labelX: 183, labelY: 192
  },
  {
    id: 'armero', nombre: 'Armero\nGuayabal', n: 11, cobertura: '25.0%',
    path: 'M 250,120 L 290,105 L 320,125 L 325,155 L 290,170 L 280,135 Z',
    labelX: 290, labelY: 140
  },
  {
    id: 'honda', nombre: 'Honda', n: 4, cobertura: '4.0%',
    path: 'M 290,105 L 330,85 L 360,100 L 355,135 L 325,155 L 320,125 Z',
    labelX: 330, labelY: 118
  },
  {
    id: 'casabianca', nombre: 'Casabianca', n: 5, cobertura: '38.5%',
    path: 'M 130,115 L 170,95 L 210,105 L 210,140 L 175,155 L 140,145 Z',
    labelX: 172, labelY: 128
  },
  {
    id: 'ambalema', nombre: 'Ambalema', n: 1, cobertura: '4.5%',
    path: 'M 280,185 L 320,170 L 350,185 L 345,220 L 310,235 L 280,220 Z',
    labelX: 315, labelY: 202
  },
];

// Contorno simplificado del departamento del Tolima (norte)
const tolimaOutline = 'M 80,60 L 140,40 L 220,35 L 310,45 L 380,70 L 400,120 L 390,180 L 370,240 L 340,290 L 280,320 L 220,330 L 160,310 L 110,270 L 85,220 L 75,160 L 70,110 Z';

export const TolimaMap = () => {
  const [hovered, setHovered] = useState(null);

  return (
    <div className="map-container">
      <svg viewBox="40 20 400 330" className="tolima-map-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(2,132,199,0.12)" />
            <stop offset="100%" stopColor="transparent" />
          </radialGradient>
          <filter id="neon">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Ambient glow */}
        <ellipse cx="240" cy="180" rx="180" ry="160" fill="url(#glow)" />

        {/* Departamento outline */}
        <path d={tolimaOutline} className="municipio-path" style={{ fill: 'rgba(15,23,42,0.3)', stroke: '#1e293b', strokeWidth: 2 }} />

        {/* Título del mapa */}
        <text x="240" y="48" textAnchor="middle" style={{ fontSize: '11px', fill: '#475569', fontWeight: 700, letterSpacing: '2px' }}>
          NORTE DEL TOLIMA
        </text>

        {/* Municipios */}
        {municipios.map((m) => (
          <g key={m.id}
            onMouseEnter={() => setHovered(m.id)}
            onMouseLeave={() => setHovered(null)}
          >
            <path
              d={m.path}
              className={`municipio-path highlighted`}
              style={hovered === m.id ? { fill: 'rgba(2,132,199,0.55)', stroke: '#38bdf8', filter: 'url(#neon)' } : undefined}
            />
            <text x={m.labelX} y={m.labelY - 8} className="map-label active">
              {m.nombre.includes('\n')
                ? m.nombre.split('\n').map((line, i) => (
                    <tspan key={i} x={m.labelX} dy={i === 0 ? 0 : 12}>{line}</tspan>
                  ))
                : m.nombre
              }
            </text>
            <text x={m.labelX} y={m.labelY + (m.nombre.includes('\n') ? 14 : 6)} className="map-sample-label">
              n={m.n}
            </text>
          </g>
        ))}

        {/* Tooltip flotante */}
        {hovered && (() => {
          const m = municipios.find(x => x.id === hovered);
          return (
            <g>
              <rect x={m.labelX - 55} y={m.labelY + 18} width={110} height={32} rx={6}
                fill="rgba(2,6,23,0.9)" stroke="#0ea5e9" strokeWidth={1} />
              <text x={m.labelX} y={m.labelY + 32} textAnchor="middle" style={{ fontSize: '8px', fill: '#94a3b8', fontWeight: 600 }}>
                Muestra: {m.n} | Cob: {m.cobertura}
              </text>
              <text x={m.labelX} y={m.labelY + 43} textAnchor="middle" style={{ fontSize: '7px', fill: '#64748b' }}>
                Universo tendero del municipio
              </text>
            </g>
          );
        })()}
      </svg>

      <div className="map-legend">
        <div className="legend-item">
          <div className="legend-swatch" style={{ background: 'rgba(2,132,199,0.35)', border: '1px solid #0ea5e9' }} />
          <span>Municipio en estudio</span>
        </div>
        <div className="legend-item">
          <div className="legend-swatch" style={{ background: 'rgba(15,23,42,0.6)', border: '1px solid #334155' }} />
          <span>Resto del departamento</span>
        </div>
      </div>
    </div>
  );
};
