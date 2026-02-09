'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import ProtectedRoute from '../../components/ui/ProtectedRoute';
import { PlusIcon, TrashIcon, ChartBarIcon } from '@heroicons/react/24/outline';

export default function ResultsPage() {
  const { user, loading: authLoading } = useAuth();
  const [results, setResults] = useState([]);
  const [students, setStudents] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student_id: '',
    subject_id: '',
    score: '',
    grade: '',
    assignment_name: ''
  });

  useEffect(() => {
    if (user) {
      fetchResults();
      fetchStudents();
      fetchSubjects();
    }
  }, [user]);

  const fetchResults = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/results', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching results:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStudents = async () => {
    try {
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
    }
  };

  const fetchSubjects = async () => {
    try {
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
      const response = await fetch('/api/v1/results', {
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

      const newResult = await response.json();
      setResults(prev => [...prev, newResult]);
      setFormData({ student_id: '', subject_id: '', score: '', grade: '', assignment_name: '' });
      setShowForm(false);
    } catch (err) {
      setError(err.message);
      console.error('Error creating result:', err);
    }
  };

  const handleDelete = async (resultId) => {
    if (window.confirm('Are you sure you want to delete this result?')) {
      try {
        const response = await fetch(`/api/v1/results/${resultId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        setResults(prev => prev.filter(result => result.id !== resultId));
      } catch (err) {
        setError(err.message);
        console.error('Error deleting result:', err);
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
                  <ChartBarIcon className="h-6 w-6 mr-2 text-indigo-600" />
                  Student Results
                </h2>
                <button
                  onClick={() => setShowForm(!showForm)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors duration-200"
                >
                  <PlusIcon className="h-5 w-5 mr-1" />
                  Add Result
                </button>
              </div>
              <p className="mt-1 text-sm text-gray-600">Track and manage student academic results</p>
            </div>

            <div className="p-6">
              {error && (
                <div className="mb-6 rounded-lg bg-red-50 p-4 border border-red-200">
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              )}

              {showForm && (
                <div className="mb-8 bg-gray-50 p-6 rounded-xl border border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Record New Result</h3>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="student_id" className="block text-sm font-medium text-gray-700 mb-1">
                          Student
                        </label>
                        <select
                          id="student_id"
                          name="student_id"
                          value={formData.student_id}
                          onChange={handleInputChange}
                          required
                          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        >
                          <option value="">Select a student</option>
                          {students.map(student => (
                            <option key={student.id} value={student.id}>
                              {student.first_name} {student.last_name} ({student.student_id})
                            </option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label htmlFor="subject_id" className="block text-sm font-medium text-gray-700 mb-1">
                          Subject
                        </label>
                        <select
                          id="subject_id"
                          name="subject_id"
                          value={formData.subject_id}
                          onChange={handleInputChange}
                          required
                          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        >
                          <option value="">Select a subject</option>
                          {subjects.map(subject => (
                            <option key={subject.id} value={subject.id}>
                              {subject.name} ({subject.code})
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="score" className="block text-sm font-medium text-gray-700 mb-1">
                          Score (%)
                        </label>
                        <input
                          type="number"
                          id="score"
                          name="score"
                          value={formData.score}
                          onChange={handleInputChange}
                          required
                          min="0"
                          max="100"
                          step="0.01"
                          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                          placeholder="e.g., 85.5"
                        />
                      </div>
                      <div>
                        <label htmlFor="grade" className="block text-sm font-medium text-gray-700 mb-1">
                          Grade
                        </label>
                        <input
                          type="text"
                          id="grade"
                          name="grade"
                          value={formData.grade}
                          onChange={handleInputChange}
                          required
                          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                          placeholder="e.g., A, B+, etc."
                        />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="assignment_name" className="block text-sm font-medium text-gray-700 mb-1">
                        Assignment Name
                      </label>
                      <input
                        type="text"
                        id="assignment_name"
                        name="assignment_name"
                        value={formData.assignment_name}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200"
                        placeholder="e.g., Midterm Exam, Unit 3 Quiz"
                      />
                    </div>
                    <div className="flex space-x-3">
                      <button
                        type="submit"
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                      >
                        Record Result
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setShowForm(false);
                          setFormData({ student_id: '', subject_id: '', score: '', grade: '', assignment_name: '' });
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
                          Student
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Subject
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Assignment
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Score
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Grade
                        </th>
                        <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {results.length > 0 ? (
                        results.map((result) => (
                          <tr key={result.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm font-medium text-gray-900">
                                {students.find(s => s.id === result.student_id)?.first_name} {students.find(s => s.id === result.student_id)?.last_name}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">
                                {subjects.find(sub => sub.id === result.subject_id)?.name}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">{result.assignment_name}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">{result.score}%</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">{result.grade}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                              <button
                                onClick={() => handleDelete(result.id)}
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
                          <td colSpan="6" className="px-6 py-4 text-center text-sm text-gray-500">
                            No results found. Record your first student result!
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