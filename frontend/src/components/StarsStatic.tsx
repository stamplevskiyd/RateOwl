// src/components/StarsStatic.tsx
import {Star} from 'lucide-react';

export default function StarsStatic({value}: { value: number }) {
    return (
        <div className="flex items-center gap-0.5">
            {[...Array(10)].map((_, i) => (
                <Star
                    key={i}
                    size={18}
                    strokeWidth={1.5}
                    className={
                        i < value ? 'fill-yellow-400 text-yellow-400' : 'text-zinc-500'
                    }
                />
            ))}
        </div>
    );
}