import {ReactNode, useEffect} from 'react';
import {createPortal} from 'react-dom';
import {X} from 'lucide-react';

interface Props {
    title?: string;
    onClose: () => void;
    children: ReactNode;
}

export default function Modal({title, onClose, children}: Props) {
    // блокируем скролл body пока открыт оверлей
    useEffect(() => {
        document.body.style.overflow = 'hidden';
        return () => void (document.body.style.overflow = '');
    }, []);

    return createPortal(
        <div
            className="fixed inset-0 z-50 flex items-center justify-center
                 bg-black/50 backdrop-blur-sm"
            onClick={onClose}>
            {/* ловим клик, чтобы не закрывать по внутренним нажатиям */}
            <div
                onClick={e => e.stopPropagation()}
                className="w-[90vw] max-w-md rounded-xl bg-zinc-800 p-6 shadow-xl">
                {/* Заголовок + крестик */}
                <header className="mb-4 flex items-center justify-between">
                    {title && (
                        <h3 className="text-lg font-semibold text-gray-100">{title}</h3>
                    )}
                    <button
                        onClick={onClose}
                        className="rounded p-1 text-zinc-400 hover:bg-zinc-700 hover:text-gray-100">
                        <X size={18}/>
                    </button>
                </header>

                {children}
            </div>
        </div>,
        document.body,
    );
}