// src/components/TitleFormModal.tsx
import {useState} from 'react';
import Modal from '@/components/Modal';
import TagSelector from '@/components/TagSelector';
import api from '@/api';
import {TitleRead, TagRead} from '@/types';

export default function TitleFormModal({
                                           title,
                                           onClose,
                                           onSave,
                                       }: {
    title: TitleRead;
    onClose: () => void;
    onSave: (t: TitleRead) => void;
}) {
    const [name, setName] = useState(title.name);
    const [tags, setTags] = useState<TagRead[]>(title.tags);

    const save = async () => {
        const {data} = await api.put<TitleRead>(`/api/v1/titles/${title.id}`, {
            name,
            tags: tags.map(t => t.id),
        });
        onSave(data);
        onClose();
    };

    return (
        <Modal title="Редактировать медиа" onClose={onClose}>
            <label className="mb-4 block">
                <span className="mb-1 block text-sm">Название</span>
                <input
                    className="w-full rounded-md bg-zinc-700 p-2"
                    value={name}
                    onChange={e => setName(e.target.value)}
                />
            </label>

            <label className="mb-6 block">
                <span className="mb-1 block text-sm">Теги</span>
                <TagSelector selected={tags} onChange={setTags}/>
            </label>

            <div className="flex justify-end gap-3">
                <button onClick={onClose}>Отмена</button>
                <button onClick={save} className="btn-primary">
                    Сохранить
                </button>
            </div>
        </Modal>
    );
}