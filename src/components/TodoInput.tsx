'use client';

import { useState, KeyboardEvent } from 'react';
import { Plus, Sparkles } from 'lucide-react';

interface TodoInputProps {
  onSubmit: (text: string) => void;
}

export default function TodoInput({ onSubmit }: TodoInputProps) {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim()) {
      onSubmit(text);
      setText('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="relative">
      <div className="flex items-center gap-2 bg-white rounded-2xl shadow-sm border border-slate-200 p-2 focus-within:shadow-md focus-within:border-slate-300 transition-all duration-300">
        <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <input
          type="text"
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="添加一个新的待办事项..."
          className="flex-1 px-2 py-2 text-slate-700 placeholder-slate-400 focus:outline-none bg-transparent"
        />
        <button
          onClick={handleSubmit}
          disabled={!text.trim()}
          className={`flex-shrink-0 px-4 py-2.5 rounded-xl font-medium transition-all duration-200 flex items-center gap-1.5 ${
            text.trim()
              ? 'bg-slate-800 text-white hover:bg-slate-700 shadow-lg'
              : 'bg-slate-100 text-slate-400 cursor-not-allowed'
          }`}
        >
          <Plus className="w-4 h-4" />
          <span>添加</span>
        </button>
      </div>
    </div>
  );
}
