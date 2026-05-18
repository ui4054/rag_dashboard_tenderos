import React, { useState } from 'react';
import { apiService } from '../services/api';
import { Send, Bot, Loader2, Sparkles } from 'lucide-react';
import '../styles/RagTerminal.css';

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
    <div className="glass-card terminal-box">
      <div className="terminal-header">
        <Bot size={28} style={{ color: 'var(--accent-light)' }} />
        <div>
          <h3 className="terminal-title">IA de Interpretación según filtros aplicados</h3>
          <p className="terminal-subtitle">
            Gemini 2.5 Flash Lite
          </p>
        </div>
      </div>

      <div className="terminal-input-row">
        <textarea
          value={consigna}
          onChange={(e) => setConsigna(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); enviarConsulta(); } }}
          placeholder="Escribe tu consigna o pregunta sobre la muestra de tenderos actual..."
          rows={3}
          className="terminal-textarea"
        />
        <button
          onClick={() => enviarConsulta()}
          disabled={cargando || !consigna.trim()}
          className="btn-send-rag"
        >
          {cargando ? <Loader2 size={20} className="spin" /> : <Send size={20} />}
          <span>{cargando ? 'Procesando...' : 'Analizar'}</span>
        </button>
      </div>

      <div className="sugerencias-bar">
        <Sparkles size={16} style={{ color: '#eab308' }} />
        <span className="sugerencias-label">Sugerencias IA:</span>
        {sugerencias.map((sug, i) => (
          <button
            key={i}
            onClick={() => { setConsigna(sug); enviarConsulta(sug); }}
            className="btn-sugerencia"
          >
            {sug}
          </button>
        ))}
      </div>

      {error && (
        <div className="terminal-error-box">
          {error}
        </div>
      )}

      {respuesta && (
        <div className="terminal-output-card">
          <div className="output-badge">
            Interpretación Q1
          </div>
          <p className="output-text">
            {respuesta}
          </p>
        </div>
      )}
    </div>
  );
};
