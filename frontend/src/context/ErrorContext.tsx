import {
    createContext,
    useContext,
    useEffect,
    useRef,
    useState,
    ReactNode,
} from 'react';
import {setErrorCallback, installInterceptors} from '@/api';

interface ErrorMsg {
    id: number;
    text: string;
    code?: number;
}

const ErrorCtx = createContext<(m: string, c?: number) => void>(() => {
});
export const useError = () => useContext(ErrorCtx);

export function ErrorProvider({children}: { children: ReactNode }) {
    const [errors, setErrors] = useState<ErrorMsg[]>([]);

    /* ② — хранит последние «текст+код», чтобы убрать дубликаты,
           даже если setState ещё не успел примениться */
    const lastKey = useRef<string | null>(null);

    const push = (text: string, code?: number) => {
        const key = `${code}-${text}`;
        if (lastKey.current === key) return;      // дубль → пропускаем
        lastKey.current = key;

        setErrors(prev => [...prev, {id: Date.now(), text, code}]);
    };

    const close = (id: number) =>
        setErrors(prev => prev.filter(e => e.id !== id));

    useEffect(() => {
        setErrorCallback(push);   // передаём в api
        installInterceptors();    // ставим интерцепторы ровно один раз
    }, []);

    return (
        <ErrorCtx.Provider value={push}>
            {children}

            <div className="fixed right-4 top-4 z-[9999] flex flex-col gap-3">
                {errors.map(e => (
                    <div
                        key={e.id}
                        className="max-w-xs rounded-lg border border-red-600/60
                       bg-zinc-800 p-4 shadow-lg">
                        <div className="mb-1 text-sm font-semibold text-red-400">
                            {e.code ? `Ошибка ${e.code}` : 'Ошибка'}
                        </div>
                        <p className="text-sm text-gray-200">{e.text}</p>

                        <button
                            onClick={() => close(e.id)}
                            className="mt-2 rounded bg-red-600/70 px-2 py-0.5 text-xs">
                            Закрыть
                        </button>
                    </div>
                ))}
            </div>
        </ErrorCtx.Provider>
    );
}