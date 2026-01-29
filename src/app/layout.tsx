import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '待办事项 - MyMoltbot',
  description: '一个简单高效的待办事项管理应用',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  );
}
