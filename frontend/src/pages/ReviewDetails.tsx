// src/pages/ReviewDetails.tsx
import {useEffect, useState} from 'react';
import {useNavigate, useParams, Link} from 'react-router-dom';
import dayjs from 'dayjs';
import api from '@/api';
import {ReviewRead} from '@/types';
import StarsStatic from '@/components/StarsStatic';
import TagBadge from '@/components/TagBadge';
import {useAuth} from '@/context/AuthContext';
import {Edit3, Trash2} from 'lucide-react';
import ReviewFormModal from '@/components/ReviewFormModal';

export default function ReviewDetails() {
    const {id} = useParams();
    const nav = useNavigate();
    const {user} = useAuth();

    const [data, setData] = useState<ReviewRead | null>(null);
    const [err, setErr] = useState('');
    const [editing, setEditing] = useState(false);

    useEffect(() => {
        api
            .get<ReviewRead>(`/api/v1/reviews/${id}`)
            .then(r => setData(r.data))
            .catch(() => setErr('Не удалось загрузить обзор'));
    }, [id]);

    const isMine = user && data && user.id === data.created_by.id;

    const handleDelete = async () => {
        if (!confirm('Удалить этот обзор?')) return;
        await api.delete(`/api/v1/reviews/${id}`);
        nav('/'); // назад к списку
    };

    if (err) return <p className="p-6 text-center text-red-400">{err}</p>;
    if (!data) return <p className="p-6 text-center">Загрузка…</p>;

    return (
        <main className="mx-auto mt-6 w-full max-w-3xl px-4 pb-24">
            <Link to="/" className="mb-4 inline-block text-spruce-400 hover:underline">
                ← Назад
            </Link>

            <article className="rounded-xl border-2 border-zinc-700 bg-surface p-6 shadow">
                <header className="mb-4 flex items-start justify-between">
                    <div>
                        <h2 className="mb-1 text-2xl font-bold text-gray-100">
                            {data.title.name}
                        </h2>
                        <div className="flex flex-wrap items-center gap-2 text-sm text-zinc-400">
                            <span>by {data.created_by.username}</span>
                            <span>·</span>
                            <time dateTime={data.created_on}>
                                {dayjs(data.created_on).format('DD.MM.YYYY')}
                            </time>
                        </div>
                    </div>

                    {isMine && (
                        <div className="flex gap-2">
                            <button onClick={() => setEditing(true)} className="btn-icon" title="Редактировать">
                                <Edit3 size={18}/>
                            </button>
                            <button onClick={handleDelete} className="btn-icon" title="Удалить">
                                <Trash2 size={18}/>
                            </button>
                        </div>
                    )}
                </header>

                <StarsStatic value={data.rate}/>

                <p className="mt-4 whitespace-pre-line text-gray-200 leading-relaxed">
                    {data.text}
                </p>

                <div className="mt-6 flex flex-wrap gap-2">
                    {data.tags.map(t => (
                        <TagBadge key={t.id} tag={t}/>
                    ))}
                </div>
            </article>

            {editing && (
                <ReviewFormModal
                    review={data}
                    onClose={() => setEditing(false)}
                    onSave={setData}
                />
            )}
        </main>
    );
}