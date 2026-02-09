// Frontend health monitoring service
class HealthMonitor {
  constructor(options = {}) {
    this.options = {
      healthCheckInterval: options.healthCheckInterval || 30000, // 30 seconds
      apiUrl: options.apiUrl || '/api/health',
      onHealthChange: options.onHealthChange || (() => {}),
      onCriticalFailure: options.onCriticalFailure || (() => {}),
      maxRetryAttempts: options.maxRetryAttempts || 3,
      retryDelay: options.retryDelay || 5000, // 5 seconds
      ...options
    };
    
    this.isMonitoring = false;
    this.currentHealthStatus = 'unknown';
    this.lastCheckTime = null;
    this.retryCount = 0;
    this.healthCheckIntervalId = null;
  }

  async checkHealth() {
    try {
      const response = await fetch(this.options.apiUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        // Disable caching for health checks
        cache: 'no-cache'
      });

      const healthData = await response.json();
      
      this.lastCheckTime = new Date();
      this.retryCount = 0; // Reset retry count on success
      
      const newStatus = this.evaluateHealthStatus(healthData);
      
      if (newStatus !== this.currentHealthStatus) {
        const previousStatus = this.currentHealthStatus;
        this.currentHealthStatus = newStatus;
        
        // Notify listeners of health change
        this.options.onHealthChange({
          previousStatus,
          currentStatus: newStatus,
          healthData,
          timestamp: this.lastCheckTime
        });
        
        // If we transitioned to a critical state, trigger critical failure callback
        if (this.isCriticalStatus(newStatus)) {
          this.options.onCriticalFailure({
            status: newStatus,
            healthData,
            timestamp: this.lastCheckTime
          });
        }
      }
      
      return {
        success: true,
        status: newStatus,
        healthData,
        timestamp: this.lastCheckTime
      };
    } catch (error) {
      console.error('Health check failed:', error);
      
      this.retryCount++;
      
      // If we've exceeded max retry attempts, consider it a critical failure
      if (this.retryCount >= this.options.maxRetryAttempts) {
        const previousStatus = this.currentHealthStatus;
        this.currentStatus = 'critical';
        
        this.options.onCriticalFailure({
          status: 'critical',
          error: error.message,
          retryCount: this.retryCount,
          timestamp: new Date()
        });
        
        return {
          success: false,
          status: 'critical',
          error: error.message,
          timestamp: new Date()
        };
      }
      
      return {
        success: false,
        status: 'error',
        error: error.message,
        timestamp: new Date()
      };
    }
  }

  evaluateHealthStatus(healthData) {
    // Evaluate the overall health status based on the health check response
    if (!healthData || typeof healthData !== 'object') {
      return 'critical';
    }
    
    // If there's an overall status property, use that
    if (healthData.overall_status) {
      switch (healthData.overall_status.toLowerCase()) {
        case 'healthy':
          return 'healthy';
        case 'degraded':
          return 'degraded';
        case 'unhealthy':
          return 'unhealthy';
        default:
          return 'unknown';
      }
    }
    
    // Fallback: check if the response contains basic success indicators
    if (healthData.status && healthData.status.toLowerCase() === 'healthy') {
      return 'healthy';
    }
    
    // If there are individual checks, evaluate them
    if (healthData.individual_checks) {
      const checkValues = Object.values(healthData.individual_checks);
      
      // If any check is unhealthy, mark overall as unhealthy
      if (checkValues.some(check => 
        check.status && check.status.toLowerCase() === 'unhealthy'
      )) {
        return 'unhealthy';
      }
      
      // If any check is degraded, mark overall as degraded (if no unhealthy)
      if (checkValues.some(check => 
        check.status && check.status.toLowerCase() === 'degraded'
      )) {
        return 'degraded';
      }
      
      // If all checks are healthy, mark overall as healthy
      if (checkValues.every(check => 
        check.status && check.status.toLowerCase() === 'healthy'
      )) {
        return 'healthy';
      }
    }
    
    return 'unknown';
  }

  isCriticalStatus(status) {
    return ['critical', 'unhealthy'].includes(status.toLowerCase());
  }

  async startMonitoring() {
    if (this.isMonitoring) {
      console.warn('Health monitoring is already running');
      return;
    }
    
    this.isMonitoring = true;
    
    // Perform initial health check
    await this.checkHealth();
    
    // Set up periodic health checks
    this.healthCheckIntervalId = setInterval(async () => {
      await this.checkHealth();
    }, this.options.healthCheckInterval);
    
    console.log('Health monitoring started');
  }

  stopMonitoring() {
    if (!this.isMonitoring) {
      console.warn('Health monitoring is not running');
      return;
    }
    
    this.isMonitoring = false;
    
    if (this.healthCheckIntervalId) {
      clearInterval(this.healthCheckIntervalId);
      this.healthCheckIntervalId = null;
    }
    
    console.log('Health monitoring stopped');
  }

  getStatus() {
    return {
      status: this.currentHealthStatus,
      isMonitoring: this.isMonitoring,
      lastCheckTime: this.lastCheckTime,
      retryCount: this.retryCount
    };
  }

  // Method to manually trigger a health check
  async triggerHealthCheck() {
    if (!this.isMonitoring) {
      // If not monitoring, just perform a one-time check
      return await this.checkHealth();
    }
    
    // If monitoring, perform check and return result
    return await this.checkHealth();
  }
}

// Export a singleton instance by default, but allow creating new instances
const healthMonitor = new HealthMonitor();

export default healthMonitor;
export { HealthMonitor };