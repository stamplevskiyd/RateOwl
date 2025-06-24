import {useEffect, useState} from 'react';
import api from '@/api';
import {Review} from '@/types';
import ReviewCard from '@/components/ReviewCard';

export default function Home() {
    const [reviews, setReviews] = useState<Review[]>([]);

    useEffect(() => {
        api.get<Review[]>('/api/v1/reviews/').then((res) => setReviews(res.data));
    }, []);

    // frontend/src/pages/Home.tsx  (фрагмент)

    return (
        <main className="mx-auto mt-6 w-full max-w-3xl">
            <div className="space-y-6 px-4 pb-8">         {/* ← добавили отступы */}
                {reviews.map(r => (
                    <ReviewCard key={r.id} review={r}/>
                ))}
            </div>
        </main>
    );
}
