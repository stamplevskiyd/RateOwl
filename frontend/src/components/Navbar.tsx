import {NavLink, Link, useNavigate} from 'react-router-dom';
import logoPng from '@/assets/logo.png';
import {useAuth} from '@/context/AuthContext';

export default function Navbar() {
    const {user, logout} = useAuth();
    const nav = useNavigate();

    return (
        <header className="sticky top-0 z-10 flex items-center gap-1 bg-spruce-700 px-4 py-2 shadow-md">
            <Link to="/" className="flex items-center gap-2">
                <img src={logoPng} alt="logo" className="h-24 w-18 rounded"/>
                <span className="text-xl font-semibold tracking-wide text-gray-100">RateOwl</span>
            </Link>

            <nav className="ml-8 flex items-center gap-4">
                <NavLink to="/" end className="nav-link">Обзоры</NavLink>
                <NavLink to="/titles" className="nav-link">Медиа</NavLink>
                <NavLink to="/tags" className="nav-link">Теги</NavLink>
            </nav>

            <div className="ml-auto flex items-center gap-3">
                <NavLink to="/create" className="btn-primary">+ Обзор</NavLink>

                {user ? (
                    <>
                        <button
                            onClick={() => nav('/profile')}
                            className="rounded px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600/50">
                            {user.username}
                        </button>

                        <button
                            onClick={logout}
                            className="rounded-md bg-zinc-700/60 px-3 py-1.5 text-sm text-gray-100 hover:bg-zinc-700">
                            Выйти
                        </button>
                    </>
                ) : (
                    <NavLink to="/login" className="btn-ghost">Войти</NavLink>
                )}

                {/*{user ? (*/}
                {/*    <button onClick={() => nav('/profile')} className="btn-ghost">{user.username}</button>*/}
                {/*) : (*/}
                {/*    <NavLink to="/login" className="btn-ghost">Войти</NavLink>*/}
                {/*)}*/}

                {/*{user && (*/}
                {/*    <button onClick={logout} className="btn-ghost text-sm opacity-70 hover:opacity-100">⟲</button>*/}
                {/*)}*/}
            </div>
        </header>
    );
}

/* tailwind helpers (где-нибудь global.css)
.nav-link { @apply rounded-md px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600/70 [&.active]:bg-spruce-600; }
.btn-primary { @apply rounded-md bg-spruce-500 px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600; }
.btn-ghost   { @apply rounded-md px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600/50; }
*/