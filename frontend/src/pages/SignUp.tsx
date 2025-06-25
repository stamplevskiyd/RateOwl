// src/pages/SignUp.tsx
import {FormEvent, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import api from '@/api';
import {useAuth} from '@/context/AuthContext';

export default function SignUp() {
    const nav = useNavigate();
    const {login} = useAuth();
    const [form, setForm] = useState({username: '', password: ''});

    const submit = async (e: FormEvent) => {
        e.preventDefault();
        // 1) создаём пользователя
        await api.post('api/v1/users/', form);
        // 2) сразу логинимся через AuthContext
        await login(form);
        nav('/');
    };

    return (
        <main className="flex min-h-screen items-center justify-center bg-canvas">
            <form
                onSubmit={submit}
                className="w-full max-w-sm rounded-xl border border-zinc-700
                   bg-surface p-8 shadow-xl">
                <h1 className="mb-6 text-2xl font-bold text-gray-100">Регистрация</h1>

                <label className="mb-4 block">
                    <span className="mb-1 block text-sm text-gray-300">Логин</span>
                    <input
                        className="w-full rounded-md bg-zinc-700 p-2 text-gray-100"
                        value={form.username}
                        onChange={e => setForm({...form, username: e.target.value})}
                    />
                </label>

                <label className="mb-6 block">
                    <span className="mb-1 block text-sm text-gray-300">Пароль</span>
                    <input
                        type="password"
                        className="w-full rounded-md bg-zinc-700 p-2 text-gray-100"
                        value={form.password}
                        onChange={e => setForm({...form, password: e.target.value})}
                    />
                </label>

                <button
                    disabled={!form.username || !form.password}
                    className="w-full rounded-md bg-spruce-600 px-4 py-2 text-sm
                     font-semibold text-gray-100 transition-colors hover:bg-spruce-700">
                    Создать
                </button>
            </form>
        </main>
    );
}