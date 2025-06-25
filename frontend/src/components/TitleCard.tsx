// src/components/TitleCard.tsx
import TagBadge from '@/components/TagBadge';
import {TitleRead} from '@/types';
import {Edit3, Trash2} from 'lucide-react';
import api from '@/api';
import {Link} from 'react-router-dom';

export default function TitleCard({
                                      item,
                                      onRemove,
                                      onEdit,
                                  }: {
    item: TitleRead;
    onRemove: (id: number) => void;
    onEdit: (t: TitleRead) => void;
}) {
    const del = async () => {
        if (!confirm('Удалить медиа?')) return;
        await api.delete(`/api/v1/titles/${item.id}`);
        onRemove(item.id);
    };

    return (
        <div
            className="rounded-xl border-2 border-zinc-700 bg-surface p-4 transition
                 hover:-translate-y-0.5 hover:border-spruce-500/70 hover:shadow-md">
            <div className="flex items-start justify-between">
                <Link
                    to={`/titles/${item.id}`}
                    className="text-lg font-semibold text-gray-100 hover:underline">
                    {item.name}
                </Link>

                <div className="flex gap-2">
                    <button onClick={() => onEdit(item)} className="btn-icon">
                        <Edit3 size={16}/>
                    </button>
                    <button onClick={del} className="btn-icon">
                        <Trash2 size={16}/>
                    </button>
                </div>
            </div>

            <div className="mt-3 flex flex-wrap gap-2">
                {item.tags.map(t => (
                    <TagBadge key={t.id} tag={t}/>
                ))}
            </div>
        </div>
    );
}