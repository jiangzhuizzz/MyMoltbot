export interface Todo {
  id: string;
  text: string;
  completed: boolean;
  createdAt: Date;
  category?: string;
}

export interface TodoCategory {
  id: string;
  name: string;
  color: string;
}
