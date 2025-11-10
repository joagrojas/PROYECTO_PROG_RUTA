/**
 * Servicio de API para comunicación con el backend
 * Usa Axios con configuración global e interceptores
 */

import api from './axiosConfig';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

// ========================================
// AUTH
// ========================================
export const authService = {
  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
};

// ========================================
// USUARIOS
// ========================================
export const usuariosService = {
  getAll: async (skip = 0, limit = 100) => {
    const response = await api.get(`/usuarios?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/usuarios/${id}`);
    return response.data;
  },

  create: async (usuario) => {
    const response = await api.post('/usuarios', usuario);
    return response.data;
  },

  update: async (id, usuario) => {
    const response = await api.put(`/usuarios/${id}`, usuario);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/usuarios/${id}`);
    return response.data;
  },
};

// ========================================
// AVENIDAS
// ========================================
export const avenidasService = {
  getAll: async () => {
    const response = await api.get('/avenidas');
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/avenidas/${id}`);
    return response.data;
  },

  create: async (avenida) => {
    const response = await api.post('/avenidas', avenida);
    return response.data;
  },

  update: async (id, avenida) => {
    const response = await api.put(`/avenidas/${id}`, avenida);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/avenidas/${id}`);
    return response.data;
  },
};

// ========================================
// TIPOS DE SINIESTRO
// ========================================
export const tiposSiniestroService = {
  getAll: async () => {
    const response = await api.get('/tipos-siniestro');
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/tipos-siniestro/${id}`);
    return response.data;
  },

  create: async (tipo) => {
    const response = await api.post('/tipos-siniestro', tipo);
    return response.data;
  },

  update: async (id, tipo) => {
    const response = await api.put(`/tipos-siniestro/${id}`, tipo);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/tipos-siniestro/${id}`);
    return response.data;
  },
};

// ========================================
// SINIESTROS
// ========================================
export const siniestrosService = {
  getAll: async (params = {}) => {
    const { skip = 0, limit = 100, avenida_id, tipo_id, nivel_gravedad } = params;
    let url = `/siniestros?skip=${skip}&limit=${limit}`;

    if (avenida_id) url += `&avenida_id=${avenida_id}`;
    if (tipo_id) url += `&tipo_id=${tipo_id}`;
    if (nivel_gravedad) url += `&nivel_gravedad=${nivel_gravedad}`;

    const response = await api.get(url);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/siniestros/${id}`);
    return response.data;
  },

  create: async (siniestro) => {
    const response = await api.post('/siniestros', siniestro);
    return response.data;
  },

  update: async (id, siniestro) => {
    const response = await api.put(`/siniestros/${id}`, siniestro);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/siniestros/${id}`);
    return response.data;
  },

  count: async (params = {}) => {
    const { avenida_id, tipo_id, nivel_gravedad } = params;
    let url = '/siniestros/count';
    const queryParams = [];

    if (avenida_id) queryParams.push(`avenida_id=${avenida_id}`);
    if (tipo_id) queryParams.push(`tipo_id=${tipo_id}`);
    if (nivel_gravedad) queryParams.push(`nivel_gravedad=${nivel_gravedad}`);

    if (queryParams.length > 0) url += `?${queryParams.join('&')}`;

    const response = await api.get(url);
    return response.data;
  },
};

// ========================================
// VEHÍCULOS
// ========================================
export const vehiculosService = {
  getBySiniestro: async (siniestroId) => {
    const response = await api.get(`/vehiculos/siniestro/${siniestroId}`);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/vehiculos/${id}`);
    return response.data;
  },

  create: async (vehiculo) => {
    const response = await api.post('/vehiculos', vehiculo);
    return response.data;
  },

  update: async (id, vehiculo) => {
    const response = await api.put(`/vehiculos/${id}`, vehiculo);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/vehiculos/${id}`);
    return response.data;
  },
};

// ========================================
// REPORTES
// ========================================
export const reportesService = {
  // Dashboard unificado
  getEstadisticas: async (params = {}) => {
    try {
      const response = await api.get('/reportes/estadisticas', { params });
      return response.data;
    } catch (error) {
      console.error('Error en getEstadisticas:', error);
      throw error;
    }
  },

  // Endpoints individuales
  getResumenGeneral: async () => {
    try {
      const response = await api.get('/reportes/resumen-general');
      return response.data;
    } catch (error) {
      console.error('Error en getResumenGeneral:', error);
      throw error;
    }
  },

  getSiniestrosPorZona: async () => {
    try {
      const response = await api.get('/reportes/siniestros-por-zona');
      return response.data;
    } catch (error) {
      console.error('Error en getSiniestrosPorZona:', error);
      throw error;
    }
  },

  getEstadisticasPorTipo: async () => {
    try {
      const response = await api.get('/reportes/estadisticas-por-tipo');
      return response.data;
    } catch (error) {
      console.error('Error en getEstadisticasPorTipo:', error);
      throw error;
    }
  },

  getSiniestrosPorDiaSemana: async () => {
    try {
      const response = await api.get('/reportes/siniestros-por-dia-semana');
      return response.data;
    } catch (error) {
      console.error('Error en getSiniestrosPorDiaSemana:', error);
      throw error;
    }
  },
};

// ========================================
// REPORTES DELICTIVOS
// ========================================
export const reportesDelitoService = {
  // Obtener todos los reportes con filtros
  getAll: async (params = {}) => {
    const { skip = 0, limit = 100, avenida_id, tipo_delito, nivel_peligrosidad } = params;
    let url = `/reportes-delito?skip=${skip}&limit=${limit}`;

    if (avenida_id) url += `&avenida_id=${avenida_id}`;
    if (tipo_delito) url += `&tipo_delito=${tipo_delito}`;
    if (nivel_peligrosidad) url += `&nivel_peligrosidad=${nivel_peligrosidad}`;

    const response = await api.get(url);
    return response.data;
  },

  // Obtener un reporte por ID
  getById: async (id) => {
    const response = await api.get(`/reportes-delito/${id}`);
    return response.data;
  },

  // Crear nuevo reporte
  create: async (reporte) => {
    const response = await api.post('/reportes-delito', reporte);
    return response.data;
  },

  // Actualizar reporte
  update: async (id, reporte) => {
    const response = await api.put(`/reportes-delito/${id}`, reporte);
    return response.data;
  },

  // Eliminar reporte
  delete: async (id) => {
    const response = await api.delete(`/reportes-delito/${id}`);
    return response.data;
  },

  // Contar reportes (para paginación)
  count: async (params = {}) => {
    const { avenida_id, tipo_delito, nivel_peligrosidad } = params;
    let url = '/reportes-delito/count';
    const queryParams = [];

    if (avenida_id) queryParams.push(`avenida_id=${avenida_id}`);
    if (tipo_delito) queryParams.push(`tipo_delito=${tipo_delito}`);
    if (nivel_peligrosidad) queryParams.push(`nivel_peligrosidad=${nivel_peligrosidad}`);

    if (queryParams.length > 0) url += `?${queryParams.join('&')}`;

    const response = await api.get(url);
    return response.data;
  },
};

export const getResumen = async () => {
  return axios.get(`${BASE_URL}/reportes/resumen-general`);
};

export const getSiniestrosPorZona = async () => {
  return axios.get(`${BASE_URL}/reportes/siniestros-por-zona`);
};

export const getEstadisticasPorTipo = async () => {
  return axios.get(`${BASE_URL}/reportes/estadisticas-por-tipo`);
};

export const getSiniestrosPorDia = async () => {
  return axios.get(`${BASE_URL}/reportes/siniestros-por-dia-semana`);
};

// Exportación por defecto (opcional)
export default {
  authService,
  usuariosService,
  avenidasService,
  tiposSiniestroService,
  siniestrosService,
  vehiculosService,
  reportesService,
  reportesDelitoService,
};