// Root Layout
import './globals.css';
import AuthWrapper from './AuthWrapper';
import NavigationComponent from './components/NavigationComponent';

export const metadata = {
  title: 'Teacher Planning App',
  description: 'A secure multi-user application for teachers to manage school plannings, student results, and task lists',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <AuthWrapper>
          <div className="min-h-screen flex flex-col">
            <header className="bg-gradient-to-r from-indigo-700 via-purple-700 to-indigo-800 h-16 w-full shadow-[0_2px_10px_-3px_rgba(0,0,0,0.1)]">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-full">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3 backdrop-blur-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                    </svg>
                  </div>
                  <span className="text-white font-bold text-xl">Teacher Planning</span>
                </div>
                
                <NavigationComponent />
              </div>
            </header>
            <main className="flex-grow py-8">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {children}
              </div>
            </main>
            <footer className="py-6 text-center text-sm text-gray-600 bg-white bg-opacity-50 border-t border-gray-200 backdrop-blur-sm">
              <div className="container mx-auto">
                <p>© {new Date().getFullYear()} Teacher Planning App. All rights reserved.</p>
                <p className="mt-1 text-xs text-gray-500">Designed for educators, by educators</p>
              </div>
            </footer>
          </div>
        </AuthWrapper>
      </body>
    </html>
  );
}