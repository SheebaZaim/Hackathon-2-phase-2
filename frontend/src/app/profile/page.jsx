'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const ProfilePage = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('better-auth-token');
    if (!token) {
      router.push('/login');
      return;
    }

    fetchUserProfile(token);
  }, []);

  const fetchUserProfile = async (token) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/users/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        const errorData = await response.json();
        localStorage.removeItem('better-auth-token');
        router.push('/login');
      }
    } catch (err) {
      setError('Failed to fetch user profile');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('better-auth-token');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="px-6 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-2xl font-bold">User Profile</h1>
                <p className="text-blue-100">Manage your account settings</p>
              </div>
              <button
                onClick={handleLogout}
                className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors duration-200"
              >
                Logout
              </button>
            </div>
          </div>

          <div className="p-8">
            {error && (
              <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Profile Picture Section */}
              <div className="md:col-span-1">
                <div className="bg-gray-50 rounded-lg p-6 text-center">
                  <div className="mx-auto mb-4">
                    <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto">
                      <span className="text-white text-3xl font-bold">
                        {user?.email?.charAt(0)?.toUpperCase() || 'U'}
                      </span>
                    </div>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">{user?.email || 'User'}</h3>
                  <p className="text-sm text-gray-500">Member since {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'today'}</p>
                </div>
              </div>

              {/* User Information Section */}
              <div className="md:col-span-2">
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h3>

                  <div className="space-y-4">
                    <div className="flex justify-between py-2 border-b border-gray-200">
                      <span className="text-gray-600">Email Address</span>
                      <span className="text-gray-900 font-medium">{user?.email || 'N/A'}</span>
                    </div>

                    <div className="flex justify-between py-2 border-b border-gray-200">
                      <span className="text-gray-600">Account ID</span>
                      <span className="text-gray-900 font-mono text-sm">{user?.id || 'N/A'}</span>
                    </div>

                    <div className="flex justify-between py-2 border-b border-gray-200">
                      <span className="text-gray-600">Account Created</span>
                      <span className="text-gray-900">{user?.created_at ? new Date(user.created_at).toLocaleString() : 'N/A'}</span>
                    </div>

                    <div className="flex justify-between py-2">
                      <span className="text-gray-600">Last Updated</span>
                      <span className="text-gray-900">{user?.updated_at ? new Date(user.updated_at).toLocaleString() : 'N/A'}</span>
                    </div>
                  </div>

                  <div className="mt-8 pt-6 border-t border-gray-200">
                    <h4 className="text-md font-semibold text-gray-900 mb-3">Account Actions</h4>
                    <div className="flex space-x-4">
                      <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200">
                        Edit Profile
                      </button>
                      <button className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors duration-200">
                        Change Password
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;