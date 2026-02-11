/**
 * Root Layout
 * Main layout wrapper for Todo App
 */

import './globals.css';
import AuthWrapper from './AuthWrapper';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A secure multi-user todo application for organizing your tasks',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <AuthWrapper>
          {children}
        </AuthWrapper>
      </body>
    </html>
  );
}
