'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    // Check if user is logged in by checking for token in localStorage
    const token = localStorage.getItem('better-auth-token');
    setIsLoggedIn(!!token);
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem('better-auth-token');
    setIsLoggedIn(false);
    window.location.href = '/login';
  };

  const navLinks = isLoggedIn
    ? [
        { name: 'Dashboard', href: '/dashboard' },
        { name: 'Profile', href: '/profile' },
      ]
    : [
        { name: 'Home', href: '/' },
        { name: 'Login', href: '/login' },
        { name: 'Register', href: '/register' },
      ];

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-purple-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <div className="bg-white p-2 rounded-lg shadow-md">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <span className="ml-3 text-white text-xl font-bold">TodoMaster</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                href={link.href}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  pathname === link.href
                    ? 'bg-white text-indigo-600 shadow-md'
                    : 'text-white hover:bg-blue-500 hover:text-white'
                }`}
              >
                {link.name}
              </Link>
            ))}

            {isLoggedIn && (
              <button
                onClick={handleLogout}
                className="ml-4 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors duration-200 text-sm font-medium"
              >
                Logout
              </button>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <MobileMenu navLinks={navLinks} isLoggedIn={isLoggedIn} handleLogout={handleLogout} pathname={pathname} />
          </div>
        </div>
      </div>
    </nav>
  );
}

function MobileMenu({ navLinks, isLoggedIn, handleLogout, pathname }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center justify-center p-2 rounded-md text-white hover:text-white hover:bg-blue-500 focus:outline-none"
      >
        <svg
          className={`${isOpen ? 'hidden' : 'block'} h-6 w-6`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg
          className={`${isOpen ? 'block' : 'hidden'} h-6 w-6`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      {isOpen && (
        <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              href={link.href}
              className={`block px-4 py-2 text-sm ${
                pathname === link.href
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
              onClick={() => setIsOpen(false)}
            >
              {link.name}
            </Link>
          ))}
          {isLoggedIn && (
            <button
              onClick={() => {
                handleLogout();
                setIsOpen(false);
              }}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Logout
            </button>
          )}
        </div>
      )}
    </>
  );
}