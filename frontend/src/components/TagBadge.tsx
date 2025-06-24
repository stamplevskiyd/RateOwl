import { TagRead } from '@/types';

export default function TagBadge({ tag }: { tag: TagRead }) {
  return (
    <span
      className="rounded-full bg-spruce-600/30 px-2 py-0.5 text-xs
                 font-medium text-spruce-300">
      {tag.name}
    </span>
  );
}