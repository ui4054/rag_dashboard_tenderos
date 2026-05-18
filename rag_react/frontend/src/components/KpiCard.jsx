import React from 'react';
import '../styles/KpiCard.css';

export const KpiCard = ({ title, value, subvalue, icon: Icon, color = "#0284c7", isGauge = false, maxGauge = 100 }) => {
  const numVal = parseFloat(value) || 0;
  const percentage = isGauge ? Math.min(100, Math.round((numVal / maxGauge) * 100)) : 0;

  return (
    <div className="glass-card kpi-card-box">
      <div className="kpi-card-header">
        <h4 className="kpi-card-title">
          {title}
        </h4>
        {Icon && <Icon size={22} style={{ color: color }} />}
      </div>
      
      <div className="kpi-card-value">
        {value}
      </div>

      {subvalue && (
        <div className="kpi-card-subvalue">
          {subvalue}
        </div>
      )}

      {isGauge && (
        <div className="kpi-gauge-track">
          <div 
            className="kpi-gauge-fill"
            style={{ 
              width: `${percentage}%`, 
              backgroundColor: color, 
              boxShadow: `0 0 10px ${color}`
            }} 
          />
        </div>
      )}
    </div>
  );
};
