import axios from 'axios';

/*  Колбэк, который ErrorProvider передаст сюда */
let pushError: (msg: string, code?: number) => void = () => {
};

/* Вызывается в ErrorProvider */
export const setErrorCallback = (fn: typeof pushError) => {
    pushError = fn;
};

/* Чтобы не ставить интерцепторы дважды */
let interceptorsInstalled = false;

export const installInterceptors = () => {
    if (interceptorsInstalled) return;
    interceptorsInstalled = true;

    api.interceptors.request.use(cfg => {
        const token = localStorage.getItem('token');
        if (token) cfg.headers.Authorization = `Bearer ${token}`;
        return cfg;
    });

    api.interceptors.response.use(
        res => res,
        err => {
            /* ① — игнорируем pre-flight OPTIONS */
            if (err.config?.method?.toLowerCase() === 'options') {
                return Promise.reject(err);
            }

            const {status, data} = err.response || {};
            const msg = data?.detail || err.message || 'Неизвестная ошибка';

            pushError(msg, status);

            if (status === 401 && localStorage.getItem('token')) {
                localStorage.removeItem('token');
            }
            return Promise.reject(err);
        },
    );
};

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '',
});
export default api;