import {useEffect, useState} from 'react';
import StarRating from '@/components/StarRating';
import api from '@/api';
import {TitleRead, ReviewCreate} from '@/types';
import {useNavigate} from 'react-router-dom';

export default function CreateReview() {
    const nav = useNavigate();
    const [titles, setTitles] = useState<TitleRead[]>([]);
    const [payload, setPayload] = useState<ReviewCreate>({
        title_id: '',
        rate: 7,
        text: '',
        hidden: false
    });

    useEffect(() => {
        api.get('/api/v1/titles/').then(r => setTitles(r.data));
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await api.post('api/v1/reviews/add', payload);
        nav('/'); // к списку
    };

    return (
        <section className="mx-auto mt-6 w-full max-w-lg rounded-xl
                        bg-surface p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-semibold">Новый обзор</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                <label className="block">
                    <span className="mb-1 inline-block">Медиа</span>
                    <select
                        className="block w-full rounded-md bg-zinc-700 p-2"
                        value={payload.title_id}
                        onChange={e =>
                            setPayload({...payload, title_id: e.target.value})
                        }
                        required>
                        <option value="" disabled>
                            — выбрать —
                        </option>
                        {titles.map(t => (
                            <option key={t.id} value={t.id}>
                                {t.name}
                            </option>
                        ))}
                    </select>
                </label>

                <label className="block">
                    <span className="mb-1 inline-block">Оценка</span>
                    <StarRating
                        value={payload.rate}
                        onChange={v => setPayload({...payload, rate: v})}
                    />
                </label>

                <label className="block">
                    <span className="mb-1 inline-block">Текст</span>
                    <textarea
                        rows={4}
                        className="block w-full resize-y rounded-md bg-zinc-700 p-2"
                        value={payload.text}
                        onChange={e =>
                            setPayload({...payload, text: e.target.value})
                        }
                        required
                    />
                </label>

                <label className="mb-6 flex items-center gap-2">
                <input
                    type="checkbox"
                    checked={payload.hidden}
                    onChange={e => setPayload({...payload, hidden: e.target.checked})}
                />
                <span className="text-sm text-gray-200"> Обзор виден только&nbsp;мне</span>
            </label>

                <button
                    type="submit"
                    className="rounded-lg bg-spruce-600 px-4 py-2 font-medium
                     transition hover:bg-spruce-700">
                    Сохранить
                </button>
            </form>
        </section>
    );
}