import React, { useState } from 'react';
import { apiService } from '../services/api';
import { Send, Bot, Loader2, Sparkles } from 'lucide-react';

export const RagTerminal = ({ filtrosActivos }) => {
  const [consigna, setConsigna] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  const sugerencias = [
    "¿Por qué los tenderos formalizados presentan mayor resiliencia en el Norte del Tolima?",
    "Identifica el impacto de la carga familiar sobre la gestión del riesgo financiero.",
    "Compara el perfil de autonomía entre tenderos jóvenes y mayores de 50 años."
  ];

  const enviarConsulta = async (textoAEnviar = consigna) => {
    if (!textoAEnviar.trim()) return;
    setCargando(true);
    setError('');
    setRespuesta('');

    try {
      const res = await apiService.consultarRag(textoAEnviar, filtrosActivos);
      setRespuesta(res.respuesta || "Sin respuesta generada.");
    } catch (err) {
      setError("No se pudo conectar con la API de IA. Verifica tu conexión al backend.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="glass-card" style={{ padding: '28px', marginTop: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
        <Bot size={28} style={{ color: 'var(--accent-light)' }} />
        <div>
          <h3 style={{ fontSize: '1.3rem', fontWeight: '800' }}>Ia de Interpetación según filtro aplicados</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Gemini 2.5 Flash Lite
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
        <textarea
          value={consigna}
          onChange={(e) => setConsigna(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); enviarConsulta(); } }}
          placeholder="Escribe tu consigna o pregunta sobre la muestra de tenderos actual..."
          rows={3}
          style={{ flex: 1, resize: 'vertical', fontSize: '0.95rem' }}
        />
        <button
          onClick={() => enviarConsulta()}
          disabled={cargando || !consigna.trim()}
          style={{
            padding: '0 24px',
            background: 'var(--accent-primary)',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            opacity: (!consigna.trim() || cargando) ? 0.6 : 1
          }}
        >
          {cargando ? <Loader2 size={20} className="spin" /> : <Send size={20} />}
          <span>{cargando ? 'Procesando...' : 'Analizar'}</span>
        </button>
      </div>

      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '24px', alignItems: 'center' }}>
        <Sparkles size={16} style={{ color: '#eab308' }} />
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '600' }}>Sugerencias IA:</span>
        {sugerencias.map((sug, i) => (
          <button
            key={i}
            onClick={() => { setConsigna(sug); enviarConsulta(sug); }}
            style={{
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-light)',
              padding: '4px 12px',
              fontSize: '0.8rem',
              borderRadius: '20px',
              fontWeight: '400',
            }}
          >
            {sug}
          </button>
        ))}
      </div>

      {error && (
        <div style={{ background: 'var(--danger-bg)', border: '1px solid var(--danger-border)', padding: '16px', borderRadius: '8px', color: '#ef4444', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      {respuesta && (
        <div style={{ background: 'rgba(11, 15, 25, 0.8)', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '24px', position: 'relative' }}>
          <div style={{ position: 'absolute', top: '12px', right: '16px', fontSize: '0.75rem', fontWeight: '700', color: 'var(--accent-light)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
            Interpretación Q1
          </div>
          <p style={{ whiteSpace: 'pre-line', lineHeight: '1.7', fontSize: '0.95rem', color: 'var(--text-main)' }}>
            {respuesta}
          </p>
        </div>
      )}
    </div>
  );
};
