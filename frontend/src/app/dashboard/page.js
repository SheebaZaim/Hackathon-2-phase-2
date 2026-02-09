// app/dashboard/page.js
'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import ProtectedRoute from '../../components/ui/ProtectedRoute';
import TaskList from '../../components/tasks/TaskList';
import TaskForm from '../../components/tasks/TaskForm';
import { Spinner } from '../../components/ui/Spinner';
import {
  UserCircleIcon,
  ClockIcon,
  DocumentTextIcon,
  CheckBadgeIcon,
  BookOpenIcon,
  ClipboardDocumentListIcon,
  AcademicCapIcon,
  CheckCircleIcon,
  UserGroupIcon,
  PresentationChartBarIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const [stats, setStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(true);
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    if (user) {
      fetchDashboardStats();
    }
  }, [user]);

  const fetchDashboardStats = async () => {
    try {
      setLoadingStats(true);
      // In a real implementation, this would fetch stats from the API
      // For now, we'll use mock data
      setTimeout(() => {
        setStats({
          totalPlannings: 24, // This will be used for Students
          upcomingTasks: 3,
          studentResults: 12,
          completedThisWeek: 2,
          totalTeachers: 5, // This will be used for Classes
          classesManaged: 8, // This will be used for Assignments Graded
          assignmentsGraded: 15
        });
        setLoadingStats(false);
      }, 500);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      setLoadingStats(false);
    }
  };

  const handleTaskCreated = (newTask) => {
    setTasks(prev => [...prev, newTask]);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner />
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Welcome back, {user?.first_name || user?.email}!
                </h1>
                <p className="text-sm text-gray-600 mt-1">Here's what's happening with your classes today</p>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-600">
                  <ClockIcon className="inline h-4 w-4 mr-1" />
                  {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Stats Section */}
            <div className="mb-8">
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
                <div className="bg-white overflow-hidden shadow rounded-2xl border border-gray-100">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-indigo-100 rounded-xl p-3">
                        <BookOpenIcon className="h-6 w-6 text-indigo-600" />
                      </div>
                      <div className="ml-4 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Classes</dt>
                          <dd className="flex items-baseline">
                            <div className="text-2xl font-semibold text-gray-900">
                              {loadingStats ? '...' : stats?.totalTeachers || 0}
                            </div>
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-2xl border border-gray-100">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-emerald-100 rounded-xl p-3">
                        <UserGroupIcon className="h-6 w-6 text-emerald-600" />
                      </div>
                      <div className="ml-4 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Students</dt>
                          <dd className="flex items-baseline">
                            <div className="text-2xl font-semibold text-gray-900">
                              {loadingStats ? '...' : stats?.totalPlannings || 0}
                            </div>
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-2xl border border-gray-100">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-amber-100 rounded-xl p-3">
                        <AcademicCapIcon className="h-6 w-6 text-amber-600" />
                      </div>
                      <div className="ml-4 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Results</dt>
                          <dd className="flex items-baseline">
                            <div className="text-2xl font-semibold text-gray-900">
                              {loadingStats ? '...' : stats?.studentResults || 0}
                            </div>
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-2xl border border-gray-100">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-purple-100 rounded-xl p-3">
                        <ClipboardDocumentListIcon className="h-6 w-6 text-purple-600" />
                      </div>
                      <div className="ml-4 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Tasks</dt>
                          <dd className="flex items-baseline">
                            <div className="text-2xl font-semibold text-gray-900">
                              {loadingStats ? '...' : stats?.upcomingTasks || 0}
                            </div>
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-2xl border border-gray-100">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-blue-100 rounded-xl p-3">
                        <CheckCircleIcon className="h-6 w-6 text-blue-600" />
                      </div>
                      <div className="ml-4 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Completed</dt>
                          <dd className="flex items-baseline">
                            <div className="text-2xl font-semibold text-gray-900">
                              {loadingStats ? '...' : stats?.completedThisWeek || 0}
                            </div>
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-2xl border border-gray-100">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-teal-100 rounded-xl p-3">
                        <PresentationChartBarIcon className="h-6 w-6 text-teal-600" />
                      </div>
                      <div className="ml-4 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Graded</dt>
                          <dd className="flex items-baseline">
                            <div className="text-2xl font-semibold text-gray-900">
                              {loadingStats ? '...' : stats?.classesManaged || 0}
                            </div>
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Task Form and List Section - Full width on mobile, spans 2 columns on large screens */}
              <div className="lg:col-span-2 space-y-8">
                <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
                  <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
                    <h3 className="text-lg font-medium text-gray-900 flex items-center">
                      <ClipboardDocumentListIcon className="h-5 w-5 mr-2 text-indigo-600" />
                      Create New Task
                    </h3>
                  </div>
                  <div className="p-6">
                    <TaskForm userId={user?.id} onTaskCreated={handleTaskCreated} />
                  </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
                  <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
                    <h3 className="text-lg font-medium text-gray-900 flex items-center">
                      <ClipboardDocumentListIcon className="h-5 w-5 mr-2 text-indigo-600" />
                      Your Tasks
                    </h3>
                    <p className="mt-1 text-sm text-gray-500">Manage your upcoming tasks</p>
                  </div>
                  <div className="p-6">
                    <TaskList userId={user?.id} />
                  </div>
                </div>
              </div>

              {/* Right Sidebar - Stats and Info */}
              <div className="space-y-8">
                <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                    <ChartBarIcon className="h-5 w-5 mr-2 text-indigo-600" />
                    Weekly Overview
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Completed Tasks</span>
                        <span>{stats?.completedThisWeek || 0}/10</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-emerald-500 h-2 rounded-full"
                          style={{ width: `${Math.min(100, ((stats?.completedThisWeek || 0) / 10) * 100)}%` }}
                        ></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Planned Lessons</span>
                        <span>{stats?.totalPlannings || 0}/15</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-indigo-500 h-2 rounded-full"
                          style={{ width: `${Math.min(100, ((stats?.totalPlannings || 0) / 15) * 100)}%` }}
                        ></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Student Assessments</span>
                        <span>{stats?.studentResults || 0}/20</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-purple-500 h-2 rounded-full"
                          style={{ width: `${Math.min(100, ((stats?.studentResults || 0) / 20) * 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                    <AcademicCapIcon className="h-5 w-5 mr-2 text-indigo-600" />
                    Quick Actions
                  </h3>
                  <div className="space-y-3">
                    <a href="/classes" className="block w-full text-left px-4 py-3 bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 transition-colors duration-200 font-medium">
                      Manage Classes
                    </a>
                    <a href="/students" className="block w-full text-left px-4 py-3 bg-emerald-50 text-emerald-700 rounded-lg hover:bg-emerald-100 transition-colors duration-200 font-medium">
                      View Students
                    </a>
                    <a href="/subjects" className="block w-full text-left px-4 py-3 bg-amber-50 text-amber-700 rounded-lg hover:bg-amber-100 transition-colors duration-200 font-medium">
                      Manage Subjects
                    </a>
                    <a href="/results" className="block w-full text-left px-4 py-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors duration-200 font-medium">
                      Enter Grades
                    </a>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-lg border border-indigo-300 p-6 text-white">
                  <h3 className="text-lg font-medium mb-2">Tip of the Day</h3>
                  <p className="text-indigo-100 text-sm">
                    Use the task templates feature to save time on repetitive planning tasks.
                    Create templates for common lesson types and reuse them with minor modifications.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}