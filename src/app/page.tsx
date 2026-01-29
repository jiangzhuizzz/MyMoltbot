'use client';

import { useState, useEffect } from 'react';
import { Todo } from '@/types/todo';
import TodoItem from '@/components/TodoItem';
import TodoInput from '@/components/TodoInput';
import TodoStats from '@/components/TodoStats';
import { Trash2, FolderOpen, CheckCircle2 } from 'lucide-react';

const CATEGORIES = [
  { id: 'all', name: '全部', color: 'slate' },
  { id: 'active', name: '进行中', color: 'amber' },
  { id: 'completed', name: '已完成', color: 'emerald' },
];

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [isLoaded, setIsLoaded] = useState(false);

  // 从本地存储加载
  useEffect(() => {
    const saved = localStorage.getItem('todos');
    if (saved) {
      try {
        setTodos(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse todos:', e);
      }
    }
    setIsLoaded(true);
  }, []);

  // 保存到本地存储
  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem('todos', JSON.stringify(todos));
    }
  }, [todos, isLoaded]);

  const addTodo = (text: string) => {
    const newTodo: Todo = {
      id: crypto.randomUUID(),
      text: text.trim(),
      completed: false,
      createdAt: new Date(),
    };
    setTodos(prev => [newTodo, ...prev]);
  };

  const toggleTodo = (id: string) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const deleteTodo = (id: string) => {
    setTodos(prev => prev.filter(todo => todo.id !== id));
  };

  const updateTodo = (id: string, text: string) => {
    setTodos(prev =>
      prev.map(todo => (todo.id === id ? { ...todo, text: text.trim() } : todo))
    );
  };

  const clearCompleted = () => {
    setTodos(prev => prev.filter(todo => !todo.completed));
  };

  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });

  const activeTodos = todos.filter(todo => !todo.completed);
  const completedTodos = todos.filter(todo => todo.completed);

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-slate-400">加载中...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* 标题 */}
        <header className="text-center mb-8 animate-fade-in">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">
            待办事项
          </h1>
          <p className="text-slate-500">简单、高效、优雅</p>
        </header>

        {/* 输入框 */}
        <div className="mb-6 animate-slide-up">
          <TodoInput onSubmit={addTodo} />
        </div>

        {/* 统计信息 */}
        <div className="mb-4">
          <TodoStats
            total={todos.length}
            active={activeTodos.length}
            completed={completedTodos.length}
          />
        </div>

        {/* 筛选标签 */}
        <div className="flex gap-2 mb-4 animate-fade-in">
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              onClick={() => setFilter(cat.id as typeof filter)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                filter === cat.id
                  ? 'bg-slate-800 text-white shadow-lg'
                  : 'bg-white text-slate-600 hover:bg-slate-100'
              }`}
            >
              {cat.name}
              <span className="ml-2 text-xs opacity-70">
                {cat.id === 'all'
                  ? todos.length
                  : cat.id === 'active'
                  ? activeTodos.length
                  : completedTodos.length}
              </span>
            </button>
          ))}
        </div>

        {/* 待办列表 */}
        <div className="space-y-3 animate-slide-up">
          {filteredTodos.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-2xl shadow-sm border border-slate-100">
              {filter === 'all' ? (
                <>
                  <FolderOpen className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                  <p className="text-slate-400">暂无待办事项</p>
                  <p className="text-slate-300 text-sm mt-1">
                    添加一个新任务开始吧！
                  </p>
                </>
              ) : filter === 'active' ? (
                <>
                  <CheckCircle2 className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                  <p className="text-slate-400">所有任务都已完成！</p>
                </>
              ) : (
                <>
                  <Trash2 className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                  <p className="text-slate-400">暂无已完成的任务</p>
                </>
              )}
            </div>
          ) : (
            filteredTodos.map(todo => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onToggle={toggleTodo}
                onDelete={deleteTodo}
                onUpdate={updateTodo}
              />
            ))
          )}
        </div>

        {/* 清除已完成 */}
        {completedTodos.length > 0 && (
          <button
            onClick={clearCompleted}
            className="mt-6 w-full py-3 text-sm text-slate-400 hover:text-red-500 transition-colors flex items-center justify-center gap-2"
          >
            <Trash2 className="w-4 h-4" />
            清除已完成的 ({completedTodos.length})
          </button>
        )}
      </div>
    </div>
  );
}
