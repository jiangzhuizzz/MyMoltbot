'use client';

import { ClipboardList, CheckCircle2, Circle } from 'lucide-react';

interface TodoStatsProps {
  total: number;
  active: number;
  completed: number;
}

export default function TodoStats({ total, active, completed }: TodoStatsProps) {
  const progress = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-medium text-slate-600">进度</span>
        <span className="text-sm font-bold text-slate-800">{progress}%</span>
      </div>
      
      {/* 进度条 */}
      <div className="h-2 bg-slate-100 rounded-full overflow-hidden mb-4">
        <div
          className="h-full bg-gradient-to-r from-amber-400 to-orange-500 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* 统计数字 */}
      <div className="grid grid-cols-3 gap-4">
        <div className="text-center">
          <div className="flex items-center justify-center gap-1.5 mb-1">
            <ClipboardList className="w-4 h-4 text-slate-400" />
            <span className="text-lg font-bold text-slate-700">{total}</span>
          </div>
          <span className="text-xs text-slate-400">总计</span>
        </div>
        
        <div className="text-center">
          <div className="flex items-center justify-center gap-1.5 mb-1">
            <Circle className="w-4 h-4 text-amber-500" />
            <span className="text-lg font-bold text-slate-700">{active}</span>
          </div>
          <span className="text-xs text-slate-400">进行中</span>
        </div>
        
        <div className="text-center">
          <div className="flex items-center justify-center gap-1.5 mb-1">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span className="text-lg font-bold text-slate-700">{completed}</span>
          </div>
          <span className="text-xs text-slate-400">已完成</span>
        </div>
      </div>
    </div>
  );
}
