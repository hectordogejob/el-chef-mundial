import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const guardado = localStorage.getItem('chef_usuario');
  if (guardado) {
    const usuario = JSON.parse(guardado);
    config.headers.Authorization = `Bearer ${usuario.token}`;
  }
  return config;
});

export const registrarUsuario = async (nombre, email, password) => {
  const response = await api.post('/auth/registro', { nombre, email, password });
  return response.data;
};

export const loginUsuario = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

export const preguntarAlChef = async (texto, conversacionId = null) => {
  const response = await api.post('/chef/preguntar', { texto, conversacion_id: conversacionId });
  return response.data;
};

export const obtenerPreguntasRestantes = async () => {
  const response = await api.get('/chef/preguntas-restantes');
  return response.data;
};

export const listarConversaciones = async () => {
  const response = await api.get('/conversaciones/');
  return response.data;
};

export const nuevaConversacion = async () => {
  const response = await api.post('/conversaciones/nueva');
  return response.data;
};

export const obtenerHistorialConversacion = async (conversacionId) => {
  const response = await api.get(`/conversaciones/${conversacionId}/historial`);
  return response.data;
};

export const eliminarConversacion = async (conversacionId) => {
  const response = await api.delete(`/conversaciones/${conversacionId}`);
  return response.data;
};

export const listarPlatillos = async () => {
  const response = await api.get('/platillos/');
  return response.data;
};

export const obtenerPlatillo = async (id) => {
  const response = await api.get(`/platillos/${id}`);
  return response.data;
};

export const obtenerIngredientes = async (id) => {
  const response = await api.get(`/platillos/${id}/ingredientes`);
  return response.data;
};

export const obtenerFavoritos = async () => {
  const response = await api.get('/favoritos/');
  return response.data;
};

export const obtenerIdsFavoritos = async () => {
  const response = await api.get('/favoritos/ids');
  return response.data;
};

export const agregarFavorito = async (platilloId) => {
  const response = await api.post(`/favoritos/${platilloId}`);
  return response.data;
};

export const quitarFavorito = async (platilloId) => {
  const response = await api.delete(`/favoritos/${platilloId}`);
  return response.data;
};

export const obtenerPerfil = async () => {
  const response = await api.get('/perfil/');
  return response.data;
};
export default api;