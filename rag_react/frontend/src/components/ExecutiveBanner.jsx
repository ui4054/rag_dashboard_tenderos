import React from 'react';
import { Users, ShieldCheck, Activity, AlertTriangle } from 'lucide-react';
import '../styles/ExecutiveBanner.css';

export const ExecutiveBanner = ({ datosKpis }) => {
  const kpis = [
    {
      title: "Muestra Filtrada",
      val: datosKpis?.muestra_filtrada || 0,
      sub: `de ${datosKpis?.total_muestra || 0} total`,
      icon: Users,
      color: "#38bdf8",
      gauge: false
    },
    {
      title: "Formalización",
      val: `${datosKpis?.perc_formalizacion || 0}%`,
      num: datosKpis?.perc_formalizacion || 0,
      sub: "Registrados ante C.C.",
      icon: ShieldCheck,
      color: "#4ade80",
      gauge: true,
      max: 100
    },
    {
      title: "Resiliencia Media",
      val: (datosKpis?.resiliencia_media || 0).toFixed(2),
      num: datosKpis?.resiliencia_media || 0,
      sub: "/ 5.0 (Escala Likert)",
      icon: Activity,
      color: "#a855f7",
      gauge: true,
      max: 5
    },
    {
      title: "Riesgo Medio",
      val: (datosKpis?.riesgo_media || 0).toFixed(2),
      num: datosKpis?.riesgo_media || 0,
      sub: "/ 5.0 (Escala Likert)",
      icon: AlertTriangle,
      color: "#facc15",
      gauge: true,
      max: 5
    }
  ];

  return (
    <div className="glass-card executive-banner">
      {kpis.map((item, index) => {
        const IconComponent = item.icon;
        const percentage = item.gauge ? Math.min(100, Math.round((Number(item.num) / item.max) * 100)) : 0;

        return (
          <div key={index} className="banner-col">
            <div className="banner-top">
              <span className="banner-title">{item.title}</span>
              <IconComponent size={18} style={{ color: item.color }} />
            </div>

            <div className="banner-main">
              <span className="banner-value">{item.val}</span>
              <span className="banner-sub">{item.sub}</span>
            </div>

            {item.gauge && (
              <div className="banner-track">
                <div 
                  className="banner-fill" 
                  style={{ 
                    width: `${percentage}%`, 
                    backgroundColor: item.color,
                    boxShadow: `0 0 8px ${item.color}`
                  }} 
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
