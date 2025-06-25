// src/components/TitleForm.tsx
import {useState} from 'react';
import Modal from '@/components/Modal';   // простой self-closing modal (создайте, если нет)
import TagSelector from '@/components/TagSelector';
import api from '@/api';
import {TagRead} from '@/types';

export default function TitleForm({onClose}: { onClose: () => void }) {
    const [name, setName] = useState('');
    const [tags, setTags] = useState<TagRead[]>([]);
    const save = async () => {
        await api.post('api/v1/titles/add', {
            name,
            tags: tags.map(t => t.id),
        });
        onClose();
    };

    return (
        <Modal onClose={onClose} title="Новое медиа">
            <label className="block pb-4">
                <span className="mb-1 inline-block">Название</span>
                <input
                    className="w-full rounded-md bg-zinc-700 p-2"
                    value={name}
                    onChange={e => setName(e.target.value)}
                />
            </label>

            <label className="block pb-4">
                <span className="mb-1 inline-block">Теги</span>
                <TagSelector selected={tags} onChange={setTags}/>
            </label>

            <div className="flex justify-end gap-2">
                <button onClick={onClose} className="rounded px-3 py-1 hover:bg-zinc-700">
                    Отмена
                </button>
                <button
                    disabled={!name}
                    onClick={save}
                    className="rounded bg-spruce-600 px-3 py-1 text-gray-100 disabled:opacity-50">
                    Сохранить
                </button>
            </div>
        </Modal>
    );
}