// frontend/src/components/ReviewCard.tsx
import {Link} from 'react-router-dom';
import dayjs from 'dayjs';
import {Edit3, Trash2} from 'lucide-react';

import {ReviewRead} from '@/types';
import {useAuth} from '@/context/AuthContext';
import TagBadge from '@/components/TagBadge';
import StarsStatic from '@/components/StarsStatic';
import api from '@/api';

interface Props {
    review: ReviewRead;
    /** колбэк — родитель убирает карточку из стейта */
    onRemove?: (id: number) => void;
    /** колбэк — родитель открывает модальное редактирование */
    onEdit?: (r: ReviewRead) => void;
}

export default function ReviewCard({review, onRemove, onEdit}: Props) {
    const {user} = useAuth();
    const isMine = user?.id === review.created_by.id;

    /* удаляем обзор и уведомляем родителя */
    const handleDelete = async () => {
        if (!confirm('Удалить этот обзор?')) return;
        await api.delete(`api/v1/reviews/${review.id}`);
        onRemove?.(review.id);
    };

    return (
        <Link to={`/reviews/${review.id}`} className="block group">
            <article
                className="rounded-xl border-2 border-zinc-700 bg-surface px-6 py-5
                   shadow-sm shadow-zinc-900/40 transition
                   hover:-translate-y-0.5 hover:border-spruce-500/70
                   hover:shadow-md">
                {/* Заголовок и рейтинг */}
                <header className="mb-3 flex items-start justify-between">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-100">
                            {review.title.name}
                        </h3>
                        <span className="text-xs text-zinc-400">
              by {review.created_by.username} ·{' '}
                            {dayjs(review.created_on).format('DD.MM.YYYY')}
            </span>
                    </div>

                    <StarsStatic value={review.rate}/>
                </header>

                {/* Текст обзора (коротко) */}
                <p className="line-clamp-4 text-sm leading-relaxed text-gray-200">
                    {review.text}
                </p>

                {/* Теги */}
                <div className="mt-3 flex flex-wrap gap-2">
                    {review.tags.map(t => (
                        <TagBadge key={t.id} tag={t}/>
                    ))}
                </div>

                {/* Кнопки управления – только свои обзоры */}
                {isMine && (
                    <div className="mt-4 flex gap-2">
                        <button
                            onClick={e => {
                                e.preventDefault();
                                onEdit?.(review);
                            }}
                            className="btn-icon"
                            title="Редактировать">
                            <Edit3 size={16}/>
                        </button>

                        <button
                            onClick={e => {
                                e.preventDefault();
                                handleDelete();
                            }}
                            className="btn-icon"
                            title="Удалить">
                            <Trash2 size={16}/>
                        </button>
                    </div>
                )}
            </article>
        </Link>
    );
}

/* tailwind helper – можно положить в src/index.css */
//
// .btn-icon {
//   @apply rounded bg-zinc-700/50 p-1 text-gray-300 transition
//          hover:bg-zinc-600 hover:text-gray-100;
// }