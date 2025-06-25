// src/components/TagCard.tsx
import {TagRead} from '@/types';
import {Edit3, Trash2} from 'lucide-react';
import api from '@/api';

export default function TagCard({
                                    tag,
                                    onRemove,
                                    onEdit,
                                }: {
    tag: TagRead;
    onRemove: (id: number) => void;
    onEdit: (t: TagRead) => void;
}) {
    const del = async () => {
        if (!confirm('Удалить тег?')) return;
        await api.delete(`/api/v1/tags/${tag.id}`);
        onRemove(tag.id);
    };

    return (
        <div className="flex items-center gap-2 rounded-full bg-spruce-600/30 px-2 py-1">
            <span className="text-sm text-spruce-200">{tag.name}</span>

            <button onClick={() => onEdit(tag)} className="btn-icon" title="Переименовать">
                <Edit3 size={14}/>
            </button>
            <button onClick={del} className="btn-icon" title="Удалить">
                <Trash2 size={14}/>
            </button>
        </div>
    );
}