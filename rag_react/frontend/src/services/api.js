import axios from 'axios';

// En producción el frontend y la API viven en el mismo servidor (FastAPI sirve ambos)
// En desarrollo (Vite en :5173), usamos el proxy configurado en vite.config.js
const API_BASE_URL = '/api/v1';

// Ya NO se envía API Key hardcodeada — la autenticación es por cookie HttpOnly
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Envía la cookie de sesión automáticamente
});

// Cliente separado para autenticación (no usa /api/v1 como prefijo)
const authClient = axios.create({
  baseURL: '',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

export const authService = {
  login: async (password) => {
    const response = await authClient.post('/auth/login', { password });
    return response.data;
  },

  logout: async () => {
    const response = await authClient.post('/auth/logout');
    return response.data;
  },

  checkSession: async () => {
    try {
      const response = await authClient.get('/auth/check');
      return response.data.authenticated === true;
    } catch {
      return false;
    }
  }
};

export const apiService = {
  obtenerOpcionesFiltros: async () => {
    try {
      const response = await apiClient.get('/filtros/opciones');
      return response.data;
    } catch (error) {
      console.error('Error obteniendo opciones de filtros:', error);
      throw error;
    }
  },

  obtenerKpis: async (filtros) => {
    try {
      const response = await apiClient.post('/filtros/kpis', filtros);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo KPIs:', error);
      throw error;
    }
  },

  consultarRag: async (consigna, filtros) => {
    try {
      const response = await apiClient.post('/rag/consulta', { consigna, filtros });
      return response.data;
    } catch (error) {
      console.error('Error en consulta RAG:', error);
      throw error;
    }
  },

  calcularBivariado: async (dim1, dim2, filtros) => {
    try {
      const response = await apiClient.post('/filtros/bivariado', { dim1, dim2, filtros });
      return response.data;
    } catch (error) {
      console.error('Error en cálculo bivariado:', error);
      throw error;
    }
  },

  exportarMicrodatos: async (filtros) => {
    try {
      const response = await apiClient.post('/filtros/exportar', filtros);
      return response.data;
    } catch (error) {
      console.error('Error exportando microdatos:', error);
      throw error;
    }
  }
};
