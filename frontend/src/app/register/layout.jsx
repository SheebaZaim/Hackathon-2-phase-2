// Register Page Layout
import '../globals.css';

export default function RegisterLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="min-h-screen flex flex-col">
          <main className="flex-grow flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}