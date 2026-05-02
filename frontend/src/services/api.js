import axios from 'axios';

const API_BASE_URL = 'https://penny-wise-latest.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add a request interceptor to add the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authApi = {
  login: (email, password) => api.post('/auth/login', { email, password }),
};

export const billsApi = {
  list: () => api.get('/bills/'),
  extract: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/bills/extract', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  create: (billData) => api.post('/bills/', billData),
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/bills/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export const analyticsApi = {
  getPriceHistory: (itemName) => api.get(`/analytics/price-history/${itemName}`),
};

export default api;
