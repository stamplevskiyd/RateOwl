import {useState} from 'react';
import {Star} from 'lucide-react';

interface Props {
    value: number;
    onChange: (v: number) => void;
}

export default function StarRating({value, onChange}: Props) {
    const [hover, setHover] = useState<number | null>(null);

    return (
        <div className="flex items-center gap-1">
            {[...Array(10)].map((_, i) => {
                const score = i + 1;
                const active = (hover ?? value) >= score;

                return (
                    <button
                        key={score}
                        type="button"
                        onClick={() => onChange(score)}
                        onMouseEnter={() => setHover(score)}
                        onMouseLeave={() => setHover(null)}
                        aria-label={`${score} звёзд`}
                        /* убираем дефолтные стили, чтобы ничего не «прыгало» */
                        className="cursor-pointer bg-transparent p-0 leading-none
                       outline-none focus-visible:outline-none">
                        <Star
                            size={20}
                            strokeWidth={1.5}
                            /* жёлтая заливка+контур для активных,
                               серый контур без заливки для неактивных */
                            className={
                                active
                                    ? 'fill-yellow-400 text-yellow-400'
                                    : 'text-zinc-500'
                            }
                        />
                    </button>
                );
            })}

            <span className="ml-2 text-sm tabular-nums text-gray-300">
        {value}/10
      </span>
        </div>
    );
}