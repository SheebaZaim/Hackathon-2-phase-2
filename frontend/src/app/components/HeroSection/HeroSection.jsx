import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../../../hooks/useAuth';
import HeroImage from './HeroImage';
import InputContainer from './InputContainer';

const HeroSection = ({ title, subtitle, imageSrc, placeholder, buttonText, onSubmit }) => {
  const { user, loading } = useAuth();
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSubmit(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="relative w-full min-h-screen overflow-hidden">
      <Head>
        <title>{title} - Teacher Planning App</title>
        <meta name="description" content={subtitle} />
      </Head>

      {/* Background image */}
      <HeroImage src={imageSrc} alt={title} priority={true} />

      {/* Overlay content */}
      <div className="absolute inset-0 bg-black bg-opacity-30 flex flex-col items-center justify-center p-4">
        <div className="text-center z-10 max-w-3xl w-full">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 drop-shadow-lg">
            {title}
          </h1>
          <p className="text-xl text-white mb-8 drop-shadow-md">
            {subtitle}
          </p>

          {/* Input container with centered layout */}
          <div className="w-full max-w-2xl mx-auto">
            <InputContainer 
              placeholder={placeholder}
              buttonText={buttonText}
              onSubmit={handleSubmit}
              inputValue={inputValue}
              setInputValue={setInputValue}
            />
          </div>

          {/* Navigation based on auth status */}
          <div className="mt-8 flex flex-col sm:flex-row justify-center gap-4">
            {loading ? (
              <div className="text-white">Loading...</div>
            ) : user ? (
              <>
                <Link href="/dashboard" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300">
                  Go to Dashboard
                </Link>
                <Link href="/api/auth/logout" className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition duration-300">
                  Logout
                </Link>
              </>
            ) : (
              <>
                <Link href="/login" className="px-6 py-3 bg-white text-blue-600 rounded-lg hover:bg-gray-100 transition duration-300">
                  Login
                </Link>
                <Link href="/register" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;