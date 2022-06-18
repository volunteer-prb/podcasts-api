export interface AuthResponse<T> {
  status: string;
  message?: string;
  data?: T;
}
