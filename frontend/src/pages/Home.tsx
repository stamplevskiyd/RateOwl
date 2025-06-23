import { useEffect, useState } from 'react';
import api from '@/api';
import { Review } from '@/types';
import ReviewCard from '@/components/ReviewCard';

export default function Home() {
  const [reviews, setReviews] = useState<Review[]>([]);

  useEffect(() => {
    api.get<Review[]>('/reviews/').then((res) => setReviews(res.data));
  }, []);

  return (
    <div className="max-h-[calc(100vh-80px)] overflow-y-auto pr-2">
      {reviews.map((r) => (
        <ReviewCard key={r.id} review={r} />
      ))}
    </div>
  );
}
