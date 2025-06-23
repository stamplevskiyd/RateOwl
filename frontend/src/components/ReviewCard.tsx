import dayjs from 'dayjs';
import { ReviewRead } from '@/types';

interface Props { review: ReviewRead }

export default function ReviewCard({ review }: Props) {
  return (
    <article
      /* ⬇︎ border-2 вместо border (толще) */
      className="rounded-xl border-2 border-zinc-700 bg-surface
                 px-6 py-5 shadow-sm shadow-zinc-900/40
                 transition hover:-translate-y-0.5 hover:border-spruce-500/70
                 hover:shadow-md">
      <header className="mb-3 flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-100">
            {review.title.name}
          </h3>
          <span className="text-xs text-zinc-400">
            by {review.author.username} ·{' '}
            {dayjs(review.created_at).format('DD.MM.YYYY')}
          </span>
        </div>

        {/* ⬇︎ API возвращает поле rate, а не rating */}
        <span className="mt-1 rounded-md bg-spruce-600 px-2 py-1 text-xs font-bold text-gray-100">
          {review.rate}/10
        </span>
      </header>

      <p className="text-sm leading-relaxed text-gray-200">
        {review.text /* название поля в OpenAPI — text */}
      </p>
    </article>
  );
}