// pages/index.js or app/page.js (Next.js 13+ App Router)
'use client';

import { AcademicCapIcon, BookOpenIcon, ChartBarIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../hooks/useAuth';
import Spinner from './components/ui/Spinner';

export default function HomePage() {
  const { user, loading, error } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <Spinner />
      </div>
    );
  }

  if (error) {
    console.error("Auth error:", error);
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600">Error loading page</h2>
          <p className="text-gray-600">Please try refreshing the page</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Hero Section */}
      <div className="relative w-full min-h-screen flex items-center justify-center">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-50/30 to-emerald-50/30"></div>
        <div className="relative z-10 text-center max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-center mb-6">
            <AcademicCapIcon className="h-16 w-16 text-indigo-600" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Teacher Planning App
          </h1>
          <p className="text-xl text-gray-700 mb-8 max-w-2xl mx-auto">
            Manage your school plannings, track student results, and organize tasks efficiently
          </p>

          {!user && (
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <a
                href="/register"
                className="px-8 py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition duration-200 font-medium shadow-md hover:shadow-lg"
              >
                Create Account
              </a>
              <a
                href="/login"
                className="px-8 py-3.5 bg-white text-indigo-600 border border-indigo-200 rounded-lg hover:bg-indigo-50 transition duration-200 font-medium"
              >
                Sign In
              </a>
            </div>
          )}
        </div>
      </div>

      <main className="py-12 px-4 sm:px-6 lg:px-8">
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 text-center hover:shadow-xl transition-all duration-300 hover-lift">
              <div className="w-16 h-16 bg-indigo-100 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                <BookOpenIcon className="h-8 w-8 text-indigo-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4 text-gray-900">Plan Lessons</h3>
              <p className="text-gray-600">Create and organize your lesson plans with our intuitive tools designed for educators.</p>
            </div>
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 text-center hover:shadow-xl transition-all duration-300 hover-lift">
              <div className="w-16 h-16 bg-emerald-100 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                <ChartBarIcon className="h-8 w-8 text-emerald-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4 text-gray-900">Track Results</h3>
              <p className="text-gray-600">Easily record and monitor student results to track progress over time.</p>
            </div>
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 text-center hover:shadow-xl transition-all duration-300 hover-lift">
              <div className="w-16 h-16 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                <CheckCircleIcon className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4 text-gray-900">Manage Tasks</h3>
              <p className="text-gray-600">Keep track of your teaching tasks and never miss an important deadline.</p>
            </div>
          </div>
        </section>

        {!user && (
          <section className="text-center py-12 bg-white rounded-2xl shadow-lg border border-gray-100 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Ready to get started?</h2>
            <p className="text-gray-600 mb-8 max-w-2xl mx-auto">Join thousands of teachers who use our platform to streamline their planning process.</p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <a
                href="/register"
                className="px-8 py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition duration-200 font-medium shadow-md hover:shadow-lg"
              >
                Create Account
              </a>
              <a
                href="/login"
                className="px-8 py-3.5 bg-white text-indigo-600 border border-indigo-200 rounded-lg hover:bg-indigo-50 transition duration-200 font-medium"
              >
                Sign In
              </a>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}