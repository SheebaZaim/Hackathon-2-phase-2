// Simple auth utilities
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function login(email: string, password: string) {
  const response = await axios.post(`${API_URL}/auth/login`, { email, password });
  const { access_token } = response.data;
  localStorage.setItem('auth_token', access_token);
  return { token: access_token };
}

export async function register(email: string, password: string) {
  const response = await axios.post(`${API_URL}/auth/register`, { email, password });
  const { access_token } = response.data;
  localStorage.setItem('auth_token', access_token);
  return { token: access_token };
}

export function logout() {
  localStorage.removeItem('auth_token');
}

export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false;
  return !!localStorage.getItem('auth_token');
}

export function getCurrentUser() {
  const token = localStorage.getItem('auth_token');
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return { email: payload.sub };
  } catch {
    return null;
  }
}
