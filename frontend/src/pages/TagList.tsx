// src/pages/TagList.tsx
import {useEffect, useState} from 'react';
import api from '@/api';
import {TagRead} from '@/types';
import Modal from '@/components/Modal';
import TagCard from '@/components/TagCard';
import TagEditModal from '@/components/TagEditModal';

export default function TagList() {
    const [items, setItems] = useState<TagRead[]>([]);
    const [showCreate, setShowCreate] = useState(false);
    const [name, setName] = useState('');
    const [editing, setEditing] = useState<TagRead | null>(null);

    /* загрузка */
    useEffect(() => {
        api.get<TagRead[]>('/api/v1/tags').then(r => setItems(r.data));
    }, []);

    /* CRUD helpers */
    const add = (t: TagRead) => setItems(prev => [...prev, t]);
    const replace = (t: TagRead) =>
        setItems(prev => prev.map(x => (x.id === t.id ? t : x)));
    const remove = (id: number) =>
        setItems(prev => prev.filter(t => t.id !== id));

    /* создание */
    const create = async () => {
        const {data} = await api.post<TagRead>('/api/v1/tags/add', {name});
        add(data);
        setName('');
        setShowCreate(false);
    };

    return (
        <main className="mx-auto mt-6 w-full max-w-lg px-4 pb-24">
            <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-100">Теги</h2>
                <button
                    onClick={() => setShowCreate(true)}
                    className="rounded-md bg-spruce-500 px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600">
                    + Тег
                </button>
            </div>

            {/* список */}
            <div className="flex flex-wrap gap-3">
                {items.map(tag => (
                    <TagCard
                        key={tag.id}
                        tag={tag}
                        onRemove={remove}
                        onEdit={setEditing}
                    />
                ))}
            </div>

            {/* модалка создания */}
            {showCreate && (
                <Modal title="Новый тег" onClose={() => setShowCreate(false)}>
                    <input
                        className="mb-6 w-full rounded-md bg-zinc-700 p-2"
                        value={name}
                        onChange={e => setName(e.target.value)}
                        placeholder="Название"
                    />
                    <div className="flex justify-end gap-3">
                        <button onClick={() => setShowCreate(false)}>Отмена</button>
                        <button
                            onClick={create}
                            disabled={!name}
                            className="btn-primary">
                            Создать
                        </button>
                    </div>
                </Modal>
            )}

            {/* модалка редактирования */}
            {editing && (
                <TagEditModal
                    tag={editing}
                    onClose={() => setEditing(null)}
                    onSave={replace}
                />
            )}
        </main>
    );
}