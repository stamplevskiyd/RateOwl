// src/pages/TitleDetails.tsx
import {useEffect, useState} from 'react';
import {Link, useParams} from 'react-router-dom';
import api from '@/api';
import {TitleRead, ReviewRead} from '@/types';
import ReviewCard from '@/components/ReviewCard';

export default function TitleDetails() {
    const {id} = useParams();
    const [title, setTitle] = useState<TitleRead | null>(null);
    const [reviews, setReviews] = useState<ReviewRead[]>([]);

    useEffect(() => {
        api.get<TitleRead>(`/api/v1/titles/${id}`).then(r => setTitle(r.data));
        api.get<ReviewRead[]>(`/api/v1/titles/${id}/reviews`).then(r =>
            setReviews(r.data),
        );
    }, [id]);

    if (!title) return <p className="p-6">Загрузка…</p>;

    return (
        <main className="mx-auto mt-6 w-full max-w-3xl px-4 pb-24">
            <Link to="/titles" className="text-spruce-400 hover:underline">
                ← К списку медиа
            </Link>

            <h1 className="my-4 text-2xl font-bold text-gray-100">{title.name}</h1>

            <div className="space-y-6">
                {reviews.map(r => (
                    <ReviewCard key={r.id} review={r}/>
                ))}
            </div>
        </main>
    );
}