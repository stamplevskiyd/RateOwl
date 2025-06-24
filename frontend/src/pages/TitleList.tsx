// src/pages/TitleList.tsx
import {useEffect, useState} from 'react';
import api from '@/api';
import {TitleRead} from '@/types';
import TagBadge from '@/components/TagBadge';
import TitleForm from '@/components/TitleForm';

export default function TitleList() {
    const [items, setItems] = useState<TitleRead[]>([]);
    const [showForm, setShowForm] = useState(false);

    useEffect(() => {
        api.get('/api/v1/titles/').then(r => setItems(r.data));
    }, []);

    return (
        <main className="mx-auto mt-6 w-full max-w-4xl px-4 pb-16">
            <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-100">Медиа</h2>
                <button
                    onClick={() => setShowForm(true)}
                    className="rounded-md bg-spruce-500 px-3 py-1.5 text-sm text-gray-100 hover:bg-spruce-600">
                    + Медиа
                </button>
            </div>

            <div className="space-y-4">
                {items.map(t => (
                    <div key={t.id} className="rounded-lg border border-zinc-700 p-4">
                        <h3 className="font-medium text-gray-100">{t.name}</h3>
                        <div className="mt-1 flex flex-wrap gap-2">
                            {t.tags.map(tag => (
                                <TagBadge key={tag.id} tag={tag}/>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {showForm && (
                <TitleForm
                    onClose={() => {
                        setShowForm(false);
                        load();
                    }}
                />
            )}
        </main>
    );
}