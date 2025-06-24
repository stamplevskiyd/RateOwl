import { useEffect, useState } from 'react';
import CreatableSelect from 'react-select/creatable';
import api from '@/api';
import { TagRead } from '@/types';

interface Option { label: string; value: TagRead }

export default function TagSelector({
  selected,
  onChange,
}: {
  selected: TagRead[];
  onChange: (tags: TagRead[]) => void;
}) {
  const [options, setOptions] = useState<Option[]>([]);

  // 1) загружаем все теги
  useEffect(() => {
    api.get<TagRead[]>('/api/v1/tags/').then(r =>
      setOptions(r.data.map(t => ({ label: t.name, value: t }))),
    );
  }, []);

  // 2) превращаем selected → react-select format
  const value = selected.map(t => ({ label: t.name, value: t }));

  // 3) обработчик выбора/создания
  const handleChange = async (opts: Option[]) => {
    const newTags: TagRead[] = [];

    for (const o of opts) {
      if (!o.value.id) {
        // тег создан «на лету» → POST /tags
        const { data } = await api.post<TagRead>('/api/v1/tags/add', {
          name: o.label,
        });
        newTags.push(data);
      } else {
        newTags.push(o.value);
      }
    }
    onChange(newTags);
  };

  return (
    <CreatableSelect
      isMulti
      options={options}
      value={value}
      onChange={handleChange}
      placeholder="Выберите или введите тег…"
      className="text-sm"
      styles={{
        control: base => ({
          ...base,
          background: '#27272a', // zinc-800
          borderColor: '#3f3f46', // zinc-700
        }),
        menu: base => ({ ...base, background: '#27272a' }),
        multiValue: base => ({
          ...base,
          background: '#14532d40', // spruce-700/25
        }),
        multiValueLabel: base => ({ ...base, color: '#34d399' }), // emerald-400
      }}
    />
  );
}