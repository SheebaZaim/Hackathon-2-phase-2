import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ProtectedRoute from '../components/auth/ProtectedRoute';

const DevicesPage = () => {
  const { user } = useAuth();
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock data for devices - in a real app, this would come from an API
  useEffect(() => {
    // Simulate API call to get devices
    setTimeout(() => {
      setDevices([
        {
          id: 1,
          name: 'Chrome on Windows',
          type: 'Desktop',
          lastUsed: '2023-01-15T10:30:00Z',
          current: true,
          ip: '192.168.1.100',
        },
        {
          id: 2,
          name: 'Firefox on macOS',
          type: 'Desktop',
          lastUsed: '2023-01-14T15:45:00Z',
          current: false,
          ip: '192.168.1.101',
        },
        {
          id: 3,
          name: 'Safari on iPhone',
          type: 'Mobile',
          lastUsed: '2023-01-14T08:20:00Z',
          current: false,
          ip: '10.0.0.50',
        },
        {
          id: 4,
          name: 'Chrome on Android',
          type: 'Mobile',
          lastUsed: '2023-01-13T20:15:00Z',
          current: false,
          ip: '10.0.0.51',
        },
      ]);
      setLoading(false);
    }, 500);
  }, []);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const handleRemoveDevice = (deviceId) => {
    if (window.confirm('Are you sure you want to remove this device? This will log out the device.')) {
      // In a real app, this would make an API call to remove the device
      setDevices(devices.filter(device => device.id !== deviceId));
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="flex justify-center items-center h-screen">
          <p>Loading devices...</p>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">Manage Devices</h1>
        
        <div className="mb-6 p-4 bg-blue-50 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Current Device</h2>
          <p className="text-gray-700">
            You are currently signed in on this device. Other devices will be listed below.
          </p>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white rounded-lg overflow-hidden">
            <thead className="bg-gray-100">
              <tr>
                <th className="py-3 px-4 text-left">Device</th>
                <th className="py-3 px-4 text-left">Type</th>
                <th className="py-3 px-4 text-left">Last Used</th>
                <th className="py-3 px-4 text-left">IP Address</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {devices.map((device) => (
                <tr key={device.id} className={device.current ? 'bg-blue-50' : ''}>
                  <td className="py-3 px-4">
                    <div className="font-medium">{device.name}</div>
                    {device.current && (
                      <span className="inline-block mt-1 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                        Current
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4">{device.type}</td>
                  <td className="py-3 px-4">{formatDate(device.lastUsed)}</td>
                  <td className="py-3 px-4 font-mono text-sm">{device.ip}</td>
                  <td className="py-3 px-4 text-right">
                    {!device.current && (
                      <button
                        onClick={() => handleRemoveDevice(device.id)}
                        className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
                      >
                        Remove
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {devices.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-600">No other devices found.</p>
          </div>
        )}
        
        <div className="mt-8 p-4 bg-yellow-50 rounded-lg">
          <h3 className="font-semibold text-lg mb-2">Security Tip</h3>
          <p className="text-gray-700">
            Regularly review the devices signed into your account. Remove any unfamiliar devices immediately.
          </p>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default DevicesPage;