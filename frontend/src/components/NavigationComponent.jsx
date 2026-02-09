'use client';

import { usePathname } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';
import { useState } from 'react';
import { UserCircleIcon, ChevronDownIcon } from '@heroicons/react/24/outline';

export default function NavigationComponent() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    setDropdownOpen(false);
  };

  return (
    <nav className="flex space-x-1">
      <a href="/" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/' ? 'bg-white bg-opacity-20' : ''}`}>Home</a>
      <a href="/dashboard" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/dashboard' ? 'bg-white bg-opacity-20' : ''}`}>Dashboard</a>
      <a href="/classes" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/classes' ? 'bg-white bg-opacity-20' : ''}`}>Classes</a>
      <a href="/students" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/students' ? 'bg-white bg-opacity-20' : ''}`}>Students</a>
      <a href="/subjects" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/subjects' ? 'bg-white bg-opacity-20' : ''}`}>Subjects</a>
      <a href="/results" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/results' ? 'bg-white bg-opacity-20' : ''}`}>Results</a>
      
      {user ? (
        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300"
          >
            <UserCircleIcon className="h-5 w-5 mr-1" />
            {user.first_name || user.email}
            <ChevronDownIcon className="h-4 w-4 ml-1" />
          </button>
          
          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
              <a
                href="/profile"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                onClick={() => setDropdownOpen(false)}
              >
                Profile
              </a>
              <button
                onClick={handleLogout}
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      ) : (
        <>
          <a href="/login" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/login' ? 'bg-white bg-opacity-20' : ''}`}>Login</a>
          <a href="/register" className={`text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${pathname === '/register' ? 'bg-white bg-opacity-20' : ''}`}>Register</a>
        </>
      )}
    </nav>
  );
}