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

// Add a response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If the error is 401 and not a retry, try to refresh the token
    if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('/auth/refresh')) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await authApi.refresh(refreshToken);
        const { access_token, refresh_token } = response.data;

        localStorage.setItem('token', access_token);
        localStorage.setItem('refreshToken', refresh_token);

        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;

        return api(originalRequest);
      } catch (refreshError) {
        // Refresh token failed, log out user
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const authApi = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  refresh: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
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
  delete: (billId) => api.delete(`/bills/${billId}`),
  deleteItem: (itemId) => api.delete(`/bills/items/${itemId}`),
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

