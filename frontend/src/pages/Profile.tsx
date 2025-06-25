import {useState} from 'react';
import {useAuth} from '@/context/AuthContext';
import api from '@/api';
import {UserRead} from '@/types';

export default function Profile() {
    const {user, logout} = useAuth();
    const [form, setForm] = useState<UserRead | null>(user);
    const [password, setPassword] = useState('');

    if (!form) return <p className="p-6">Вы не авторизованы.</p>;

    const save = async () => {
        const {data} = await api.put<UserRead>('/v1/users/me', form);
        setForm(data);
        alert('Профиль обновлён ✔︎');
    };

    return (
        <main className="mx-auto mt-6 w-full max-w-lg px-4 pb-16">
            <h2 className="mb-6 text-xl font-semibold text-gray-100">Профиль</h2>

            <label className="block pb-4">
                <span className="mb-1 block text-sm">Имя пользователя</span>
                <input
                    className="w-full rounded-md bg-zinc-700 p-2"
                    value={form.username}
                    onChange={e => setForm({...form, username: e.target.value})}
                />
            </label>

            <label className="block pb-4">
                <span className="mb-1 block text-sm text-gray-300">E-mail</span>
                <input
                    className="w-full rounded-md bg-zinc-700 p-2 text-gray-100"
                    value={form.email ?? ''}
                    onChange={e => setForm({...form, email: e.target.value})}
                />
            </label>


            <div className="mb-4 grid grid-cols-2 gap-4">
                <label className="block">
                    <span className="mb-1 block text-sm text-gray-300">Имя</span>
                    <input
                        className="w-full rounded-md bg-zinc-700 p-2 text-gray-100"
                        value={form.first_name ?? ''}
                        onChange={e => setForm({...form, first_name: e.target.value})}
                    />
                </label>
                <label className="block">
                    <span className="mb-1 block text-sm text-gray-300">Фамилия</span>
                    <input
                        className="w-full rounded-md bg-zinc-700 p-2 text-gray-100"
                        value={form.last_name ?? ''}
                        onChange={e => setForm({...form, last_name: e.target.value})}
                    />
                </label>

            </div>

            <label className="block pb-6">
             <span className="mb-1 block text-sm text-gray-300">
    Новый пароль&nbsp;
                 <span className="text-xs text-zinc-400">(опционально)</span>
  </span>
                <input
                    type="password"
                    placeholder="Оставьте пустым — пароль не изменится"
                    className="w-full rounded-md bg-zinc-700 p-2 text-gray-100"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
            </label>

            <div className="mt-6 flex gap-3">
                <button
                    onClick={save}
                    className="rounded bg-spruce-600 px-4 py-1.5 text-gray-100 hover:bg-spruce-700">
                    Сохранить
                </button>
                <button
                    onClick={logout}
                    className="rounded px-4 py-1.5 text-sm hover:bg-zinc-700/60">
                    Выйти
                </button>
            </div>
        </main>
    );
}