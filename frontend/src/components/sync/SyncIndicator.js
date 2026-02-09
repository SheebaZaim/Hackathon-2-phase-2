import { useState, useEffect } from 'react';

const SyncIndicator = () => {
  const [syncStatus, setSyncStatus] = useState('synced'); // synced, syncing, error
  const [lastSyncTime, setLastSyncTime] = useState(null);

  // Simulate sync status - in a real app, this would connect to actual sync status
  useEffect(() => {
    // Initially show synced
    setSyncStatus('synced');
    setLastSyncTime(new Date());

    // Set up interval to simulate sync status changes
    const interval = setInterval(() => {
      // Randomly change status for demo purposes
      const statuses = ['synced', 'syncing', 'error'];
      const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
      setSyncStatus(randomStatus);
      if (randomStatus === 'synced') {
        setLastSyncTime(new Date());
      }
    }, 10000); // Change status every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (syncStatus) {
      case 'synced':
        return 'text-green-500';
      case 'syncing':
        return 'text-yellow-500 animate-pulse';
      case 'error':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  const getStatusText = () => {
    switch (syncStatus) {
      case 'synced':
        return 'Synced';
      case 'syncing':
        return 'Syncing...';
      case 'error':
        return 'Sync error';
      default:
        return 'Unknown';
    }
  };

  const getIcon = () => {
    switch (syncStatus) {
      case 'synced':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'syncing':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 animate-spin" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
          </svg>
        );
      case 'error':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex items-center space-x-2 text-sm">
      <div className={getStatusColor()}>
        {getIcon()}
      </div>
      <div>
        <span className="font-medium">{getStatusText()}</span>
        {syncStatus === 'synced' && lastSyncTime && (
          <span className="text-gray-500 ml-2">
            at {lastSyncTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        )}
      </div>
    </div>
  );
};

export default SyncIndicator;