import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../hooks/useAuth';
import { Spinner } from './Spinner'; // Assuming we have a spinner component

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      // Redirect to login if not authenticated
      router.push('/login');
    }
  }, [user, loading, router]);

  // Show loading spinner while checking auth status
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  // If user is authenticated, render the protected content
  if (user) {
    return children;
  }

  // If not authenticated and not loading, return null (redirect will happen via useEffect)
  return null;
};

export default ProtectedRoute;