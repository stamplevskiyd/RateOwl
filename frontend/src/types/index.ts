export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name?: string | null;
  active: boolean;
}

export interface Title {
  id: number;
  name: string;
  slug: string;
}

export interface Review {
  id: number;
  description: string;
  text: string;
  rate: number;
  created_at: string;
  updated_at: string;
  title: Title;
  author: User;
}
