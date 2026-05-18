import React from 'react';

export const KpiCard = ({ title, value, subvalue, icon: Icon, color = "#0284c7", isGauge = false, maxGauge = 100 }) => {
  const percentage = isGauge ? Math.min(100, Math.round((Number(value) / maxGauge) * 100)) : 0;

  return (
    <div className="glass-card" style={{ padding: '20px', position: 'relative', overflow: 'hidden' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
        <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)' }}>
          {title}
        </h4>
        {Icon && <Icon size={22} style={{ color: color }} />}
      </div>
      
      <div style={{ fontSize: '2.2rem', fontWeight: '800', color: 'var(--text-main)', marginBottom: '4px' }}>
        {value}
      </div>

      {subvalue && (
        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          {subvalue}
        </div>
      )}

      {isGauge && (
        <div style={{ marginTop: '16px', width: '100%', background: 'var(--border-color)', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
          <div 
            style={{ 
              width: `${percentage}%`, 
              height: '100%', 
              background: color, 
              transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)',
              boxShadow: `0 0 10px ${color}`
            }} 
          />
        </div>
      )}
    </div>
  );
};
