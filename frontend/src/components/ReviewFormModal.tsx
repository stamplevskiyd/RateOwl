// src/components/ReviewFormModal.tsx
import {useState} from 'react';
import Modal from '@/components/Modal';
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
        rate: review.rate,
        text: review.text,
    });

    const save = async () => {
        const { data } = await api.put(`/api/v1/reviews/${review.id}`, form);
        onSave(data); // обновляем родителя
        onClose();
    };

    return (
        <Modal title="Редактировать обзор" onClose={onClose}>
            <label className="mb-4 block">
                <span className="mb-1 inline-block text-sm">Оценка</span>
                <StarRating
                    value={form.rate}
                    onChange={v => setForm({...form, rate: v})}
                />
            </label>

            <label className="mb-4 block">
                <span className="mb-1 inline-block text-sm">Текст</span>
                <textarea
                    rows={5}
                    className="w-full resize-y rounded-md bg-zinc-700 p-2 text-gray-100"
                    value={form.text}
                    onChange={e => setForm({...form, text: e.target.value})}
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