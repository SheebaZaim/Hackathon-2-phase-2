'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import ProtectedRoute from '../../components/ui/ProtectedRoute';
import { PlusIcon, TrashIcon, UserGroupIcon } from '@heroicons/react/24/outline';

export default function StudentsPage() {
  const { user, loading: authLoading } = useAuth();
  const [students, setStudents] = useState([]);
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    student_id: '',
    class_id: ''
  });

  useEffect(() => {
    if (user) {
      fetchStudents();
      fetchClasses();
    }
  }, [user]);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/students', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setStudents(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching students:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchClasses = async () => {
    try {
      const response = await fetch('/api/v1/classes', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setClasses(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching classes:', err);
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
      const response = await fetch('/api/v1/students', {
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

      const newStudent = await response.json();
      setStudents(prev => [...prev, newStudent]);
      setFormData({ first_name: '', last_name: '', student_id: '', class_id: '' });
      setShowForm(false);
    } catch (err) {
      setError(err.message);
      console.error('Error creating student:', err);
    }
  };

  const handleDelete = async (studentId) => {
    if (window.confirm('Are you sure you want to remove this student?')) {
      try {
        const response = await fetch(`/api/v1/students/${studentId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        setStudents(prev => prev.filter(student => student.id !== studentId));
      } catch (err) {
        setError(err.message);
        console.error('Error removing student:', err);
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
                  <UserGroupIcon className="h-6 w-6 mr-2 text-indigo-600" />
                  My Students
                </h2>
                <button
                  onClick={() => setShowForm(!showForm)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors duration-200"
                >
                  <PlusIcon className="h-5 w-5 mr-1" />
                  Add Student
                </button>
              </div>
              <p className="mt-1 text-sm text-gray-600">Manage your student rosters</p>
            </div>

            <div className="p-6">
              {error && (
                <div className="mb-6 rounded-lg bg-red-50 p-4 border border-red-200">
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              )}

              {showForm && (
                <div className="mb-8 bg-gray-50 p-6 rounded-xl border border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Student</h3>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
                          First Name
                        </label>
                        <input
                          type="text"
                          id="first_name"
                          name="first_name"
                          value={formData.first_name}
                          onChange={handleInputChange}
                          required
                          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                          placeholder="e.g., John"
                        />
                      </div>
                      <div>
                        <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
                          Last Name
                        </label>
                        <input
                          type="text"
                          id="last_name"
                          name="last_name"
                          value={formData.last_name}
                          onChange={handleInputChange}
                          required
                          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                          placeholder="e.g., Smith"
                        />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="student_id" className="block text-sm font-medium text-gray-700 mb-1">
                        Student ID
                      </label>
                      <input
                        type="text"
                        id="student_id"
                        name="student_id"
                        value={formData.student_id}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        placeholder="e.g., STUDENT001"
                      />
                    </div>
                    <div>
                      <label htmlFor="class_id" className="block text-sm font-medium text-gray-700 mb-1">
                        Class
                      </label>
                      <select
                        id="class_id"
                        name="class_id"
                        value={formData.class_id}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                      >
                        <option value="">Select a class</option>
                        {classes.map(cls => (
                          <option key={cls.id} value={cls.id}>
                            {cls.name} ({cls.subject})
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="flex space-x-3">
                      <button
                        type="submit"
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                      >
                        Add Student
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setShowForm(false);
                          setFormData({ first_name: '', last_name: '', student_id: '', class_id: '' });
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
                          Student Name
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Student ID
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Class
                        </th>
                        <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {students.length > 0 ? (
                        students.map((student) => (
                          <tr key={student.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm font-medium text-gray-900">{student.first_name} {student.last_name}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">{student.student_id}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">
                                {classes.find(c => c.id === student.class_id)?.name || 'Unknown Class'}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                              <button
                                onClick={() => handleDelete(student.id)}
                                className="text-red-600 hover:text-red-900 flex items-center justify-end w-full"
                              >
                                <TrashIcon className="h-5 w-5 mr-1" />
                                Remove
                              </button>
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan="4" className="px-6 py-4 text-center text-sm text-gray-500">
                            No students found. Add your first student!
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