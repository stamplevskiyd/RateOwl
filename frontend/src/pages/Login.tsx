import {FormEvent, useState} from 'react';
import {useNavigate, Link} from 'react-router-dom';
import {useAuth} from '@/context/AuthContext';

export default function Login() {
    const {login} = useAuth();
    const nav = useNavigate();
    const [form, setForm] = useState({username: '', password: ''});

    const submit = async (e: FormEvent) => {
        e.preventDefault();
        await login(form);
        nav('/');                      // ← после успешного логина домой
    };

    return (
        <main className="flex min-h-screen items-center justify-center bg-canvas">
            <form
                onSubmit={submit}
                className="w-full max-w-sm rounded-xl border border-zinc-700
                   bg-surface p-8 shadow-xl">
                <h1 className="mb-6 text-2xl font-bold text-gray-100">Вход</h1>

                <label className="mb-4 block">
                    <span className="mb-1 block text-sm text-gray-300">Логин</span>
                    <input
                        className="w-full rounded-md bg-zinc-700 p-2 text-gray-100
                       placeholder:text-zinc-400 focus:outline-none"
                        value={form.username}
                        onChange={e => setForm({...form, username: e.target.value})}
                        placeholder="username"
                    />
                </label>

                <label className="mb-6 block">
                    <span className="mb-1 block text-sm text-gray-300">Пароль</span>
                    <input
                        type="password"
                        className="w-full rounded-md bg-zinc-700 p-2 text-gray-100
                       placeholder:text-zinc-400 focus:outline-none"
                        value={form.password}
                        onChange={e => setForm({...form, password: e.target.value})}
                        placeholder="•••••••"
                    />
                </label>

                <button
                    disabled={!form.username || !form.password}
                    className="mb-3 w-full rounded-md bg-spruce-600 px-4 py-2
                     text-sm font-semibold text-gray-100 transition-colors
                     hover:bg-spruce-700 disabled:opacity-50">
                    Войти
                </button>

                <p className="text-center text-xs text-zinc-400">
                    Нет учетной записи?{' '}
                    <Link className="text-spruce-400 hover:underline" to="/signup">
                        Регистрация
                    </Link>
                </p>
            </form>
        </main>
    );
}