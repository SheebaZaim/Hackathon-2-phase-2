// components/ui/ProtectedRoute.jsx
'use client';

import { useAuth } from '../../hooks/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { Spinner } from './Spinner';

export default function ProtectedRoute({ children }) {
  const { user, loading, isInitialized } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isInitialized && !loading && !user) {
      router.push('/login');
    }
  }, [user, loading, isInitialized, router]);

  if (loading || !isInitialized) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner />
      </div>
    );
  }

  if (!user) {
    return null; // Render nothing while redirecting
  }

  return <>{children}</>;
}