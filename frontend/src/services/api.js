import axios from 'axios';
import { auth } from '../firebase/config';
import toast from 'react-hot-toast';

const API_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(async (config) => {
  const user = auth.currentUser;
  if (user) {
    const token = await user.getIdToken();
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      toast.error('Session expired. Please login again.');
      localStorage.removeItem('medexplain_user');
      window.location.href = '/login';
    } else if (error.response?.status === 500) {
      toast.error('Server error. Please try again later.');
    } else if (!error.response) {
      toast.error('Network error. Check your connection.');
    }
    return Promise.reject(error);
  }
);

export const analyzeMedicalText = async (text, language = 'English') => {
  try {
    const response = await api.post('/api/analyze', {
      text: text.substring(0, 3000), // Limit for free tier
      language
    });
    return response.data;
  } catch (error) {
    console.error('Analysis error:', error);
    throw error;
  }
};

export const translateText = async (text, targetLang) => {
  try {
    const response = await api.post('/api/translate', {
      text,
      target_lang: targetLang
    });
    return response.data;
  } catch (error) {
    console.error('Translation error:', error);
    throw error;
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Health check error:', error);
    return { status: 'unhealthy', error: error.message };
  }
};

export default api;

