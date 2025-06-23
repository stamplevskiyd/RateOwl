import { Review } from '@/types';

export default function ReviewCard({ review }: { review: Review }) {
  return (
    <div className="bg-white rounded-xl shadow p-4 mb-4">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">{review.title.name}</h2>
        <span className="text-sm font-medium">{review.rate}/10</span>
      </div>
      <p className="text-gray-600">{review.description}</p>
      <p className="mt-2">{review.text}</p>
      <p className="text-xs text-gray-400 mt-2">
        by {review.author.username} • {new Date(review.created_at).toLocaleDateString()}
      </p>
    </div>
  );
}
