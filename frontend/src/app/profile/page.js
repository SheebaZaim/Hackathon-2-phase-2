'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import ProtectedRoute from '../../components/ui/ProtectedRoute';
import { UserCircleIcon, EnvelopeIcon, AcademicCapIcon } from '@heroicons/react/24/outline';

export default function ProfilePage() {
  const { user, loading: authLoading, fetchUserProfile } = useAuth();
  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    email: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      setProfileData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || ''
      });
      setLoading(false);
    }
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    setError('');

    try {
      const response = await fetch('/api/v1/auth/profile', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(profileData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setMessage('Profile updated successfully!');
      // Refresh the user profile in the auth context
      await fetchUserProfile();
    } catch (err) {
      setError(err.message);
      console.error('Error updating profile:', err);
    } finally {
      setSaving(false);
    }
  };

  if (authLoading || loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-8">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                <UserCircleIcon className="h-6 w-6 mr-2 text-indigo-600" />
                My Profile
              </h2>
              <p className="mt-1 text-sm text-gray-600">Manage your account information</p>
            </div>

            <div className="p-6">
              {error && (
                <div className="mb-6 rounded-lg bg-red-50 p-4 border border-red-200">
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              )}

              {message && (
                <div className="mb-6 rounded-lg bg-green-50 p-4 border border-green-200">
                  <div className="text-sm text-green-700">{message}</div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
                      First Name
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <UserCircleIcon className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        type="text"
                        id="first_name"
                        name="first_name"
                        value={profileData.first_name}
                        onChange={handleInputChange}
                        required
                        className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        placeholder="Enter your first name"
                      />
                    </div>
                  </div>

                  <div>
                    <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
                      Last Name
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <AcademicCapIcon className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        type="text"
                        id="last_name"
                        name="last_name"
                        value={profileData.last_name}
                        onChange={handleInputChange}
                        required
                        className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        placeholder="Enter your last name"
                      />
                    </div>
                  </div>
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email Address
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={profileData.email}
                      onChange={handleInputChange}
                      required
                      className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                      placeholder="Enter your email"
                    />
                  </div>
                </div>

                <div className="flex justify-end">
                  <button
                    type="submit"
                    disabled={saving}
                    className={`px-6 py-2.5 rounded-lg font-medium ${
                      saving 
                        ? 'bg-indigo-400 cursor-not-allowed' 
                        : 'bg-indigo-600 hover:bg-indigo-700'
                    } text-white transition-colors duration-200`}
                  >
                    {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}