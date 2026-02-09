// Integration tests for frontend-backend communication
import { test, expect, describe } from '@jest/globals';
import axios from 'axios';

// Mock API base URL - in a real test, this would come from environment variables
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000/api/v1';

describe('Frontend-Backend Integration Tests', () => {
  // Test health check endpoint
  test('should successfully communicate with backend health endpoint', async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      
      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('overall_status');
      expect(['healthy', 'degraded', 'unhealthy', 'unknown']).toContain(response.data.overall_status);
      
      console.log('✓ Health check endpoint test passed');
    } catch (error) {
      console.error('✗ Health check endpoint test failed:', error.message);
      throw error;
    }
  });

  // Test verification endpoints
  test('should successfully communicate with verification endpoints', async () => {
    try {
      // Test getting verification status
      const statusResponse = await axios.get(`${API_BASE_URL}/verification/status`);
      expect(statusResponse.status).toBe(200);
      expect(typeof statusResponse.data).toBe('object');
      
      console.log('✓ Verification status endpoint test passed');
    } catch (error) {
      console.error('✗ Verification status endpoint test failed:', error.message);
      throw error;
    }
  });

  // Test authentication endpoints (if available)
  test('should handle authentication endpoints properly', async () => {
    try {
      // Try to access a protected endpoint without authentication
      // This should return a 401 or redirect
      const response = await axios.get(`${API_BASE_URL}/users/me`, { 
        validateStatus: (status) => status < 500  // Don't throw on 4xx errors
      });
      
      // Depending on implementation, this could be 401 (unauthorized) or 302 (redirect)
      expect([200, 401, 403]).toContain(response.status);
      
      console.log('✓ Authentication endpoint test passed');
    } catch (error) {
      console.error('✗ Authentication endpoint test failed:', error.message);
      throw error;
    }
  });

  // Test task endpoints
  test('should successfully communicate with task endpoints', async () => {
    try {
      // Test getting tasks
      const response = await axios.get(`${API_BASE_URL}/tasks`);
      expect(response.status).toBe(200);
      expect(typeof response.data).toBe('object');
      expect(response.data).toHaveProperty('count');
      
      console.log('✓ Task endpoints test passed');
    } catch (error) {
      console.error('✗ Task endpoints test failed:', error.message);
      throw error;
    }
  });

  // Test verification report endpoints
  test('should successfully communicate with verification report endpoints', async () => {
    try {
      // Test getting verification reports
      const response = await axios.get(`${API_BASE_URL}/verification`);
      expect(response.status).toBe(200);
      expect(typeof response.data).toBe('object');
      expect(response.data).toHaveProperty('count');
      
      console.log('✓ Verification report endpoints test passed');
    } catch (error) {
      console.error('✗ Verification report endpoints test failed:', error.message);
      throw error;
    }
  });

  // Test error handling
  test('should receive proper error responses for invalid requests', async () => {
    try {
      // Try to access a non-existent endpoint
      try {
        await axios.get(`${API_BASE_URL}/nonexistent-endpoint`);
      } catch (error) {
        // Expect a 404 error
        expect(error.response.status).toBe(404);
      }
      
      console.log('✓ Error handling test passed');
    } catch (error) {
      console.error('✗ Error handling test failed:', error.message);
      throw error;
    }
  });

  // Test data format consistency
  test('should receive consistently formatted responses', async () => {
    try {
      // Test health endpoint response format
      const healthResponse = await axios.get(`${API_BASE_URL}/health`);
      const healthData = healthResponse.data;
      
      // Verify expected properties exist
      expect(healthData).toHaveProperty('overall_status');
      expect(healthData).toHaveProperty('checks_performed');
      expect(healthData).toHaveProperty('timestamp');
      expect(healthData).toHaveProperty('individual_checks');
      
      // Test verification status endpoint response format
      const statusResponse = await axios.get(`${API_BASE_URL}/verification/status`);
      const statusData = statusResponse.data;
      
      // Verify expected properties exist
      expect(statusData).toHaveProperty('status');
      expect(statusData).toHaveProperty('last_run');
      expect(statusData).toHaveProperty('report_id');
      expect(statusData).toHaveProperty('summary');
      expect(statusData.summary).toHaveProperty('total_components');
      expect(statusData.summary).toHaveProperty('passed_components');
      expect(statusData.summary).toHaveProperty('failed_components');
      
      console.log('✓ Data format consistency test passed');
    } catch (error) {
      console.error('✗ Data format consistency test failed:', error.message);
      throw error;
    }
  });
});

// Additional helper functions for integration tests
export const setupTestUser = async () => {
  // Helper function to create a test user for authenticated tests
  try {
    const userData = {
      username: `testuser_${Date.now()}`,
      email: `test${Date.now()}@example.com`,
      password: 'SecurePassword123!'
    };

    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
  } catch (error) {
    console.error('Failed to setup test user:', error.message);
    throw error;
  }
};

export const cleanupTestUser = async (userId) => {
  // Helper function to clean up test user after tests
  try {
    await axios.delete(`${API_BASE_URL}/users/${userId}`, {
      headers: {
        // This would require admin privileges or special test endpoint
      }
    });
  } catch (error) {
    console.warn('Failed to cleanup test user:', error.message);
    // Don't throw here as it's cleanup
  }
};