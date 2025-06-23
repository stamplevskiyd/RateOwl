import {Link} from 'react-router-dom';
import logoPng from '@/assets/logo.png';   // положите файл сюда

const Navbar = () => (
    <header className="sticky top-0 z-10 flex items-center gap-1
                     bg-spruce-700 px-4 py-2 shadow-md">
        {/* всё обёрнуто в <Link> для перехода на “/” */}
        <Link to="/" className="flex items-center gap-3">
            <img
                src={logoPng}
                alt="RateOwl logo"
                className="h-13 w-12 shrink-0 rounded" /* rounded сгладит углы PNG */
            />
            <h1 className="text-2xl font-semibold tracking-wide text-gray-100">
                RateOwl
            </h1>
        </Link>

        <nav className="ml-auto flex items-center gap-3">
            <Link
                to="/"
                className="rounded-md px-3 py-1.5 text-sm font-medium text-gray-100
                   hover:bg-spruce-600/70 active:bg-spruce-800/60">
                Главная
            </Link>

            <Link
                to="/create"
                className="rounded-md bg-spruce-500 px-3 py-1.5 text-sm font-medium
                   text-gray-100 transition-colors
                   hover:bg-spruce-600 active:bg-spruce-700">
                + Обзор
            </Link>
        </nav>
    </header>
);

export default Navbar;