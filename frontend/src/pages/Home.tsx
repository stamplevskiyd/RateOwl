// frontend/src/pages/Home.tsx
import {useEffect, useState} from 'react';
import api from '@/api';
import {ReviewRead} from '@/types';
import ReviewCard from '@/components/ReviewCard';
import ReviewFormModal from '@/components/ReviewFormModal';

export default function Home() {
    const [items, setItems] = useState<ReviewRead[]>([]);
    const [editing, setEditing] = useState<ReviewRead | null>(null);

    /* ─── загрузка списка при монтировании ─── */
    useEffect(() => {
        api.get<ReviewRead[]>('api/v1/reviews').then(r => setItems(r.data));
    }, []);

    /* ─── колбэки ─── */
    const remove = (id: number) =>
        setItems(prev => prev.filter(r => r.id !== id));

    const replace = (r: ReviewRead) =>
        setItems(prev => prev.map(p => (p.id === r.id ? r : p)));

    return (
        <main className="mx-auto mt-6 w-full max-w-3xl px-4 pb-24">
            <div className="space-y-6">
                {items.map(review => (
                    <ReviewCard
                        key={review.id}
                        review={review}
                        onRemove={remove}
                        onEdit={setEditing}
                    />
                ))}
            </div>

            {/* модальное редактирование */}
            {editing && (
                <ReviewFormModal
                    review={editing}
                    onClose={() => setEditing(null)}
                    onSave={replace}
                />
            )}
        </main>
    );
}