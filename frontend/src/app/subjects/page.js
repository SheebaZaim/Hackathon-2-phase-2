'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import ProtectedRoute from '../../components/ui/ProtectedRoute';
import { PlusIcon, TrashIcon, AcademicCapIcon } from '@heroicons/react/24/outline';

export default function SubjectsPage() {
  const { user, loading: authLoading } = useAuth();
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: ''
  });

  useEffect(() => {
    if (user) {
      fetchSubjects();
    }
  }, [user]);

  const fetchSubjects = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/subjects', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSubjects(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching subjects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/v1/subjects', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const newSubject = await response.json();
      setSubjects(prev => [...prev, newSubject]);
      setFormData({ name: '', code: '', description: '' });
      setShowForm(false);
    } catch (err) {
      setError(err.message);
      console.error('Error creating subject:', err);
    }
  };

  const handleDelete = async (subjectId) => {
    if (window.confirm('Are you sure you want to delete this subject?')) {
      try {
        const response = await fetch(`/api/v1/subjects/${subjectId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        setSubjects(prev => prev.filter(subject => subject.id !== subjectId));
      } catch (err) {
        setError(err.message);
        console.error('Error deleting subject:', err);
      }
    }
  };

  if (authLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                  <AcademicCapIcon className="h-6 w-6 mr-2 text-indigo-600" />
                  Subjects
                </h2>
                <button
                  onClick={() => setShowForm(!showForm)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors duration-200"
                >
                  <PlusIcon className="h-5 w-5 mr-1" />
                  Add Subject
                </button>
              </div>
              <p className="mt-1 text-sm text-gray-600">Manage subjects for your classes</p>
            </div>

            <div className="p-6">
              {error && (
                <div className="mb-6 rounded-lg bg-red-50 p-4 border border-red-200">
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              )}

              {showForm && (
                <div className="mb-8 bg-gray-50 p-6 rounded-xl border border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Subject</h3>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                        Subject Name
                      </label>
                      <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        placeholder="e.g., Mathematics"
                      />
                    </div>
                    <div>
                      <label htmlFor="code" className="block text-sm font-medium text-gray-700 mb-1">
                        Subject Code
                      </label>
                      <input
                        type="text"
                        id="code"
                        name="code"
                        value={formData.code}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        placeholder="e.g., MATH101"
                      />
                    </div>
                    <div>
                      <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                        Description
                      </label>
                      <textarea
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleInputChange}
                        rows="3"
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        placeholder="Brief description of the subject..."
                      ></textarea>
                    </div>
                    <div className="flex space-x-3">
                      <button
                        type="submit"
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                      >
                        Create Subject
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setShowForm(false);
                          setFormData({ name: '', code: '', description: '' });
                        }}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg transition-colors duration-200"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {loading ? (
                <div className="flex justify-center items-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Subject Name
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Code
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Description
                        </th>
                        <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {subjects.length > 0 ? (
                        subjects.map((subject) => (
                          <tr key={subject.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm font-medium text-gray-900">{subject.name}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">{subject.code}</div>
                            </td>
                            <td className="px-6 py-4">
                              <div className="text-sm text-gray-900">{subject.description}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                              <button
                                onClick={() => handleDelete(subject.id)}
                                className="text-red-600 hover:text-red-900 flex items-center justify-end w-full"
                              >
                                <TrashIcon className="h-5 w-5 mr-1" />
                                Delete
                              </button>
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan="4" className="px-6 py-4 text-center text-sm text-gray-500">
                            No subjects found. Create your first subject!
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}