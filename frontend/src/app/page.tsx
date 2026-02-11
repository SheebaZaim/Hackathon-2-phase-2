/**
 * Homepage - Simple and clean landing page
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth-simple';
import Link from 'next/link';
import Image from 'next/image';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-100">
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">📝 Todo App</h1>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-between gap-12 mb-20">
          {/* Left Side - Text Content */}
          <div className="flex-1 text-center md:text-left">
            <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
              Organize Your Life
            </h2>
            <p className="text-xl text-gray-700 mb-10 max-w-lg">
              Simple, powerful task management to help you stay productive and focused on what matters most.
            </p>

            {/* CTA Buttons - Enhanced */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
              <Link
                href="/register"
                className="px-10 py-4 bg-green-600 text-white text-lg font-semibold rounded-xl hover:bg-green-700 transition-all shadow-xl hover:shadow-2xl hover:scale-105 text-center"
              >
                🚀 Get Started Free
              </Link>
              <Link
                href="/login"
                className="px-10 py-4 bg-white text-green-700 text-lg font-semibold rounded-xl hover:bg-green-50 transition-all shadow-lg hover:shadow-xl border-2 border-green-600 hover:scale-105 text-center"
              >
                🔑 Sign In
              </Link>
            </div>
          </div>

          {/* Right Side - Hero Image */}
          <div className="flex-1 flex justify-center">
            <div className="relative">
              <div className="w-48 h-48 rounded-3xl shadow-2xl overflow-hidden transform hover:scale-105 transition-transform duration-300 border-4 border-green-400 relative">
                <Image
                  src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1000&h=1000&fit=crop"
                  alt="Professional working on tasks"
                  fill
                  className="object-cover"
                  priority
                />
              </div>
              {/* Decorative elements */}
              <div className="absolute -top-4 -right-4 w-16 h-16 bg-green-300 rounded-full opacity-50 blur-xl"></div>
              <div className="absolute -bottom-4 -left-4 w-20 h-20 bg-emerald-300 rounded-full opacity-50 blur-xl"></div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow border-t-4 border-green-500">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Create Tasks Easily</h3>
            <p className="text-gray-600">Add tasks with priority levels, due dates, and categories to stay organized.</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow border-t-4 border-emerald-500">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Track Your Progress</h3>
            <p className="text-gray-600">Monitor completed tasks and visualize your productivity in a clean table view.</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow border-t-4 border-teal-500">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure & Private</h3>
            <p className="text-gray-600">Your data is protected with JWT authentication and secure database storage.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
