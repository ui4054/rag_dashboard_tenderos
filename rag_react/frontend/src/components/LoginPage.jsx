import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Shield, LogIn, ArrowLeft } from 'lucide-react';
import { authService } from '../services/api';
import '../styles/Login.css';

export const LoginPage = () => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await authService.login(password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Contraseña incorrecta. Intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-icon">
          <Shield size={32} />
        </div>
        <h1 className="login-title">Acceso al Dashboard</h1>
        <p className="login-subtitle">
          Ingresa la contraseña del equipo investigador para acceder a los datos analíticos.
        </p>

        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Contraseña del equipo"
            className="login-input"
            autoFocus
            required
          />

          {error && <div className="login-error">{error}</div>}

          <button type="submit" disabled={loading || !password} className="login-btn">
            <LogIn size={20} />
            {loading ? 'Verificando...' : 'Ingresar al Dashboard'}
          </button>
        </form>

        <div className="login-back">
          <Link to="/"><ArrowLeft size={14} style={{ verticalAlign: 'middle' }} /> Volver a la presentación</Link>
        </div>
      </div>
    </div>
  );
};
