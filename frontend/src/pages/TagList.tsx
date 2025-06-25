// src/pages/TagList.tsx
import {useEffect, useState} from 'react';
import api from '@/api';
import {TagRead} from '@/types';
import Modal from '@/components/Modal';

export default function TagList() {
    const [items, setItems] = useState<TagRead[]>([]);
    const [show, setShow] = useState(false);
    const [name, setName] = useState('');
    const [slug, setSlug] = useState('');

    useEffect(() => {
        let cancelled = false;

        (async () => {
            try {
                const {data} = await api.get('/api/v1/tags/'); // ← слэш в конце необязателен
                if (!cancelled) setItems(data);
            } catch (e) {
                console.error(e);
            }
        })();

        return () => {
            cancelled = true;          // безопасно отменяем setState
        };
    }, []);

    const create = async () => {
        await api.post('api/v1/tags/add', {name, ...(slug && {slug})});
        setName('');
        setShow(false);
        load();
    };

    return (
        <main className="mx-auto mt-6 w-full max-w-lg px-4 pb-16">
            <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-100">Теги</h2>
                <button
                    className="rounded-md bg-spruce-500 px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600"
                    onClick={() => setShow(true)}>
                     + Тег
                </button>
            </div>

            <div className="flex flex-wrap gap-2">
                {items.map(t => (
                    <span key={t.id} className="rounded-full bg-spruce-600/30 px-2 py-1 text-sm text-spruce-300">
            {t.name}
          </span>
                ))}
            </div>

            {show && (
                <Modal title="Новый тег" onClose={() => setShow(false)}>
                    <input
                        className="mb-4 w-full rounded-md bg-zinc-700 p-2"
                        value={name}
                        onChange={e => setName(e.target.value)}
                        placeholder="Название тега"
                    />
                    <input
                        className="mb-4 w-full rounded-md bg-zinc-700 p-2"
                        value={slug}
                        onChange={e => setSlug(e.target.value)}
                        placeholder="slug-тега (опционально)"
                    />
                    <div className="flex justify-end gap-2">
                        <button onClick={() => setShow(false)}>Отмена</button>
                        <button
                            disabled={!name}
                            onClick={create}
                            className="rounded bg-spruce-600 px-3 py-1 text-gray-100 disabled:opacity-50">
                            Создать
                        </button>
                    </div>
                </Modal>
            )}
        </main>
    );
}