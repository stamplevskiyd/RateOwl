// src/components/TagEditModal.tsx
import {useState} from 'react';
import Modal from '@/components/Modal';
import api from '@/api';
import {TagRead} from '@/types';

export default function TagEditModal({
                                         tag,
                                         onClose,
                                         onSave,
                                     }: {
    tag: TagRead;
    onClose: () => void;
    onSave: (t: TagRead) => void;
}) {
    const [name, setName] = useState(tag.name);

    const save = async () => {
        const {data} = await api.put<TagRead>(`/api/v1/tags/${tag.id}`, {name});
        onSave(data);
        onClose();
    };

    return (
        <Modal title="Переименовать тег" onClose={onClose}>
            <input
                className="mb-6 w-full rounded-md bg-zinc-700 p-2"
                value={name}
                onChange={e => setName(e.target.value)}
            />

            <div className="flex justify-end gap-3">
                <button onClick={onClose}>Отмена</button>
                <button onClick={save} className="btn-primary" disabled={!name}>
                    Сохранить
                </button>
            </div>
        </Modal>
    );
}