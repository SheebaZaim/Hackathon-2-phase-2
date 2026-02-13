/**
 * Homepage - Simple and clean landing page
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth-simple';
import Link from 'next/link';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 tracking-tight">📝 Todo App</h1>
        </div>

        <div className="max-w-3xl mx-auto text-center mb-16">
          {/* Text Content - Centered */}
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
            Organize Your Life
          </h2>
          <p className="text-xl text-gray-700 mb-10 max-w-2xl mx-auto">
            Simple, powerful task management to help you stay productive and focused on what matters most.
          </p>

          {/* CTA Buttons - Centered */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="px-10 py-4 bg-blue-600 text-white text-lg font-semibold rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all shadow-xl hover:shadow-2xl hover:scale-105 text-center"
            >
              🚀 Get Started Free
            </Link>
            <Link
              href="/login"
              className="px-10 py-4 bg-white text-blue-700 text-lg font-semibold rounded-xl hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all shadow-lg hover:shadow-xl border-2 border-blue-600 hover:scale-105 text-center"
            >
              🔑 Sign In
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-6 lg:gap-8">
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all border-t-4 border-blue-500 focus-within:ring-2 focus-within:ring-blue-500">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Create Tasks Easily</h3>
            <p className="text-gray-600">Add tasks with priority levels, due dates, and categories to stay organized.</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all border-t-4 border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-500">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Track Your Progress</h3>
            <p className="text-gray-600">Monitor completed tasks and visualize your productivity in a clean table view.</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all border-t-4 border-purple-500 focus-within:ring-2 focus-within:ring-purple-500">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure & Private</h3>
            <p className="text-gray-600">Your data is protected with JWT authentication and secure database storage.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
