// frontend/src/pages/TitleList.tsx
import {useEffect, useState} from 'react';
import api from '@/api';

import {TitleRead} from '@/types';
import TitleCard from '@/components/TitleCard';
import TitleForm from '@/components/TitleForm';
import TitleFormModal from '@/components/TitleFormModal';

export default function TitleList() {
    const [items, setItems] = useState<TitleRead[]>([]);
    const [showCreate, setShowCreate] = useState(false);
    const [editing, setEditing] = useState<TitleRead | null>(null);

    /** ─── безопасная загрузка списка ─── */
    useEffect(() => {
        let cancelled = false;

        (async () => {
            try {
                const {data} = await api.get<TitleRead[]>('/api/v1/titles');
                if (!cancelled) setItems(data);
            } catch (e) {
                console.error(e);
            }
        })();

        return () => {
            cancelled = true; // отменяем setState после размонтирования
        };
    }, []);

    /** ─── CRUD-колбэки ─── */
    const add = (t: TitleRead) => setItems(prev => [...prev, t]);
    const replace = (t: TitleRead) =>
        setItems(prev => prev.map(p => (p.id === t.id ? t : p)));
    const remove = (id: number) =>
        setItems(prev => prev.filter(t => t.id !== id));

    return (
        <main className="mx-auto mt-6 w-full max-w-4xl px-4 pb-24">
            <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-100">Медиа</h2>

                <button
                    onClick={() => setShowCreate(true)}
                    className="rounded-md bg-spruce-500 px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600">
                    + Медиа
                </button>
            </div>

            {/* карточки с увеличенным интервалом */}
            <div className="flex flex-col gap-4 px-2 sm:px-0">
                {items.map(t => (
                    <TitleCard
                        key={t.id}
                        item={t}
                        onRemove={remove}
                        onEdit={setEditing}
                    />
                ))}
            </div>

            {/* создание */}
            {showCreate && (
                <TitleForm onClose={() => setShowCreate(false)} onAdd={add}/>
            )}

            {/* редактирование */}
            {editing && (
                <TitleFormModal
                    title={editing}
                    onClose={() => setEditing(null)}
                    onSave={replace}
                />
            )}
        </main>
    );
}