// src/api/index.ts
import axios from 'axios';

const api = axios.create({baseURL: import.meta.env.VITE_API_URL || ''});

api.interceptors.request.use(cfg => {
    const token = localStorage.getItem('token');
    if (token) cfg.headers.Authorization = `Bearer ${token}`;
    return cfg;
});

api.interceptors.response.use(
    res => res,
    err => {
        const {status, data} = err.response || {};
        const msg = data?.detail || err.message || 'Неизвестная ошибка';
        pushError(msg, status);
        if (err.response?.status === 401) {
            /* Очищаем токен, но НЕ меняем location */
            localStorage.removeItem('token');
        }
        return Promise.reject(err);
    },
);

export default api;