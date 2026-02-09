'use client';

import { AuthProvider } from '../hooks/useAuth';
import { NotificationProvider } from '../contexts/NotificationContext';

export default function AuthWrapper({ children }) {
  return (
    <NotificationProvider>
      <AuthProvider>{children}</AuthProvider>
    </NotificationProvider>
  );
}