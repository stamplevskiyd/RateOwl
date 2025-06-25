// frontend/src/context/AuthContext.tsx
import {createContext, useContext, useEffect, useState} from 'react';
import api from '@/api';
import {UserRead} from '@/types';

interface AuthCtx {
    user: UserRead | null;
    token: string | null;          // ①
    loading: boolean;              // ② холостой период в начале
    login: (creds: { username: string; password: string }) => Promise<void>;
    logout: () => void;
}

const Ctx = createContext<AuthCtx>(null!);
export const useAuth = () => useContext(Ctx);

export function AuthProvider({children}: React.PropsWithChildren) {
    const [user, setUser] = useState<UserRead | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);

    /** ───── Проверяем токен при первом рендере ───── */
    useEffect(() => {
        if (!token) {
            setLoading(false);
            return;
        }
        api.get<UserRead>('api/v1/users/me')
            .then(r => setUser(r.data))
            .finally(() => setLoading(false));
    }, [token]);

    /** ───── Авторизация ───── */
    const login = async ({username, password}) => {
        const {data} = await api.post<{ access_token: string }>(
            'api/v1/users/token',
            new URLSearchParams({username, password}),
        );
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
        const me = await api.get<UserRead>('api/v1/users/me');
        setUser(me.data);                          // ←  сразу имя
    };

    /** ───── Выход ───── */
    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };


    return (
        <Ctx.Provider value={{user, token, loading, login, logout}}>
            {children}
        </Ctx.Provider>
    );
}