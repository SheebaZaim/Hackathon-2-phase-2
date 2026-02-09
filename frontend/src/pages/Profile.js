import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ProtectedRoute from '../components/auth/ProtectedRoute';

const ProfilePage = () => {
  const { user, loading } = useAuth();
  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    username: '',
  });
  const [isEditing, setIsEditing] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (user) {
      setProfileData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email,
        username: user.username,
      });
    }
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('accessToken');
      
      const response = await fetch('/api/v1/auth/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          first_name: profileData.first_name,
          last_name: profileData.last_name,
        }),
      });

      if (response.ok) {
        setMessage('Profile updated successfully!');
        setTimeout(() => setMessage(''), 3000); // Clear message after 3 seconds
        setIsEditing(false);
      } else {
        const errorData = await response.json();
        setMessage(errorData.detail || 'Failed to update profile');
      }
    } catch (error) {
      setMessage('An error occurred while updating profile');
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <ProtectedRoute>
      <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6">User Profile</h1>
        
        {message && (
          <div className={`mb-4 p-3 rounded ${
            message.includes('successfully') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {message}
          </div>
        )}
        
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <span className="font-medium w-32">Email:</span>
            <span>{profileData.email}</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="font-medium w-32">Username:</span>
            <span>{profileData.username}</span>
          </div>
          
          {!isEditing ? (
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <span className="font-medium w-32">First Name:</span>
                <span>{profileData.first_name || 'Not provided'}</span>
              </div>
              
              <div className="flex items-center space-x-4">
                <span className="font-medium w-32">Last Name:</span>
                <span>{profileData.last_name || 'Not provided'}</span>
              </div>
              
              <button
                onClick={() => setIsEditing(true)}
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Edit Profile
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="first_name" className="block text-gray-700 font-medium mb-2">
                  First Name
                </label>
                <input
                  type="text"
                  id="first_name"
                  name="first_name"
                  value={profileData.first_name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label htmlFor="last_name" className="block text-gray-700 font-medium mb-2">
                  Last Name
                </label>
                <input
                  type="text"
                  id="last_name"
                  name="last_name"
                  value={profileData.last_name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                >
                  Save Changes
                </button>
                
                <button
                  type="button"
                  onClick={() => {
                    setIsEditing(false);
                    // Reset form to original values
                    setProfileData({
                      first_name: user?.first_name || '',
                      last_name: user?.last_name || '',
                      email: user?.email || '',
                      username: user?.username || '',
                    });
                  }}
                  className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default ProfilePage;