import React from 'react';
import { TrendingDown, TrendingUp } from 'lucide-react';

export const HipercuboCards = ({ hipercubo }) => {
  if (!hipercubo || !hipercubo.valle_resiliencia || !hipercubo.pico_riesgo) return null;

  const v = hipercubo.valle_resiliencia;
  const p = hipercubo.pico_riesgo;
  const dims = hipercubo.dimensiones || ["Nodo de Significancia"];

  const formatSegment = (item) => {
    return dims.map(d => `${d}: ${item[d] || 'N/A'}`).join(' | ');
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginTop: '24px' }}>
      {/* VALLE DE RESILIENCIA */}
      <div 
        className="glass-card" 
        style={{ 
          background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05))',
          borderLeft: '4px solid #ef4444',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: '800', color: '#f87171', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
            Valle Crítico de Resiliencia
          </span>
          <TrendingDown size={22} style={{ color: '#ef4444' }} />
        </div>
        <div style={{ margin: '16px 0' }}>
          <div style={{ fontSize: '2.5rem', fontWeight: '800', color: '#ef4444' }}>
            {Number(v["Resiliencia_mean"] || 0).toFixed(2)}
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Muestra del segmento: <strong>{v["Resiliencia_count"] || 0}</strong> tenderos
          </p>
        </div>
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px 14px', borderRadius: '6px', fontSize: '0.85rem', color: 'var(--text-main)', fontWeight: '600' }}>
          {formatSegment(v)}
        </div>
      </div>

      {/* PICO DE RIESGO */}
      <div 
        className="glass-card" 
        style={{ 
          background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.05))',
          borderLeft: '4px solid #22c55e',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: '800', color: '#4ade80', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
            Pico de Disposición al Riesgo
          </span>
          <TrendingUp size={22} style={{ color: '#22c55e' }} />
        </div>
        <div style={{ margin: '16px 0' }}>
          <div style={{ fontSize: '2.5rem', fontWeight: '800', color: '#22c55e' }}>
            {Number(p["Perfil de Riesgo_mean"] || 0).toFixed(2)}
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Muestra del segmento: <strong>{p["Perfil de Riesgo_count"] || 0}</strong> tenderos
          </p>
        </div>
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px 14px', borderRadius: '6px', fontSize: '0.85rem', color: 'var(--text-main)', fontWeight: '600' }}>
          {formatSegment(p)}
        </div>
      </div>
    </div>
  );
};
