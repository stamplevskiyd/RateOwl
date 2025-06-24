// src/components/Navbar.tsx
import {NavLink, Link} from 'react-router-dom';
import logoPng from '@/assets/logo.png';

const linkCls =
    'rounded-md px-3 py-1.5 text-sm font-medium transition-colors ' +
    'hover:bg-spruce-600/70 active:bg-spruce-700';
const active =
    'bg-spruce-600 text-gray-100 ' +
    '!shadow-inner shadow-spruce-900/40 pointer-events-none';

export default function Navbar() {
    return (
        <header className="sticky top-0 z-10 flex items-center gap-1 bg-spruce-700 px-4 py-2 shadow-md">
            <Link to="/" className="flex items-center gap-2">
                <img src={logoPng} alt="logo" className="h-7 w-7 rounded"/>
                <span className="text-xl font-semibold tracking-wide text-gray-100">
          RateOwl
        </span>
            </Link>

            {/* вкладки */}
            <nav className="ml-6 flex items-center gap-1">
                <NavLink to="/" end className={({isActive}) => linkCls + (isActive ? ' ' + active : '')}>
                    Обзоры
                </NavLink>
                <NavLink to="/titles" className={({isActive}) => linkCls + (isActive ? ' ' + active : '')}>
                    Медиа
                </NavLink>
                <NavLink to="/tags" className={({isActive}) => linkCls + (isActive ? ' ' + active : '')}>
                    Теги
                </NavLink>
            </nav>

            {/* кнопка «+ обзор» справа */}
            <Link
                to="/create"
                className="ml-auto rounded-md bg-spruce-500 px-3 py-1.5 text-sm font-medium text-gray-100 hover:bg-spruce-600 active:bg-spruce-700">
                + Обзор
            </Link>
        </header>
    );
}