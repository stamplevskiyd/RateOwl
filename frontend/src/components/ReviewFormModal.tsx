// src/components/ReviewFormModal.tsx
import {useState} from 'react';
import Modal from '@/components/Modal';
import TagSelector from '@/components/TagSelector';
import StarRating from '@/components/StarRating';
import api from '@/api';
import {ReviewRead, TagRead} from '@/types';

export default function ReviewFormModal({
                                            review,
                                            onClose,
                                            onSave,
                                        }: {
    review: ReviewRead;
    onClose: () => void;
    onSave: (r: ReviewRead) => void;
}) {
    const [form, setForm] = useState({
        title_id: review.title.id,
        rating: review.rate,
        content: review.text,
        tags: review.tags as TagRead[],
    });

    const save = async () => {
        const {data} = await api.put<ReviewRead>(`/v1/reviews/${review.id}`, {
            ...form,
            tag_ids: form.tags.map(t => t.id),
        });
        onSave(data); // обновляем родителя
        onClose();
    };

    return (
        <Modal title="Редактировать обзор" onClose={onClose}>
            <label className="mb-4 block">
                <span className="mb-1 inline-block text-sm">Оценка</span>
                <StarRating
                    value={form.rating}
                    onChange={v => setForm({...form, rating: v})}
                />
            </label>

            <label className="mb-4 block">
                <span className="mb-1 inline-block text-sm">Текст</span>
                <textarea
                    rows={5}
                    className="w-full resize-y rounded-md bg-zinc-700 p-2 text-gray-100"
                    value={form.content}
                    onChange={e => setForm({...form, content: e.target.value})}
                />
            </label>

            <label className="mb-6 block">
                <span className="mb-1 inline-block text-sm">Теги</span>
                <TagSelector
                    selected={form.tags}
                    onChange={tags => setForm({...form, tags})}
                />
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