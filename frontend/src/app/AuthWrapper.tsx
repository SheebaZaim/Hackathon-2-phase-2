/**
 * Auth Wrapper Component
 * Simple wrapper for the app - can be extended for global auth state
 */

'use client';

import { ReactNode } from 'react';

interface AuthWrapperProps {
  children: ReactNode;
}

export default function AuthWrapper({ children }: AuthWrapperProps) {
  return <>{children}</>;
}
