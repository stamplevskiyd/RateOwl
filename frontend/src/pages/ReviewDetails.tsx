// src/pages/ReviewDetails.tsx
import {useEffect, useState} from 'react';
import {useParams, Link} from 'react-router-dom';
import dayjs from 'dayjs';
import api from '@/api';
import StarsStatic from '@/components/StarsStatic';
import TagBadge from '@/components/TagBadge';
import {ReviewRead} from '@/types';

export default function ReviewDetails() {
    const {id} = useParams();
    const [data, setData] = useState<ReviewRead | null>(null);
    const [err, setErr] = useState('');

    useEffect(() => {
        api
            .get(`/api/v1/reviews/${id}`)
            .then(r => setData(r.data))
            .catch(() => setErr('Не удалось загрузить обзор'));
    }, [id]);

    if (err) return <p className="p-6 text-center text-red-400">{err}</p>;
    if (!data) return <p className="p-6 text-center">Загрузка…</p>;

    return (
        <main className="mx-auto mt-6 w-full max-w-3xl px-4 pb-16">
            <Link to="/" className="mb-4 inline-block text-spruce-400 hover:underline">
                ← Назад к списку
            </Link>

            <article className="rounded-xl border-2 border-zinc-700 bg-surface p-6 shadow">
                <header className="mb-4">
                    <h2 className="mb-1 text-2xl font-bold text-gray-100">
                        {data.title.name}
                    </h2>
                    <div className="flex flex-wrap items-center gap-2 text-sm text-zinc-400">
                        <span>by {data.author.username}</span>
                        <span>·</span>
                        <time dateTime={data.created_at}>
                            {dayjs(data.created_at).format('DD.MM.YYYY')}
                        </time>
                    </div>
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
        </main>
    );
}