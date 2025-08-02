import axios from 'axios';
import { HVACSystem, Project, ChatMessage, SystemDiagnosis, OptimizationSuggestion, APIReponse, ChatAPIResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Chat API
export const chatAPI = {
  sendMessage: async (message: string, sessionId?: string): Promise<APIReponse<ChatAPIResponse>> => {
    try {
      const response = await api.post('/api/chat', {
        message,
        sessionId: sessionId || `session-${Date.now()}`,
      });
      return response.data;
    } catch (error) {
      console.error('Chat API error:', error);
      throw error;
    }
  },

  searchKnowledge: async (query: string, maxResults: number = 5): Promise<APIReponse<any[]>> => {
    try {
      const response = await api.post('/api/search', {
        query,
        maxResults,
      });
      return response.data;
    } catch (error) {
      console.error('Search API error:', error);
      throw error;
    }
  },
};

// HVAC Systems API
export const hvacAPI = {
  getSystems: async (): Promise<APIReponse<HVACSystem[]>> => {
    try {
      const response = await api.get('/api/hvac/systems');
      return response.data;
    } catch (error) {
      console.error('HVAC Systems API error:', error);
      throw error;
    }
  },

  getSystemStatus: async (): Promise<APIReponse<string>> => {
    try {
      const response = await api.get('/api/hvac/status');
      return response.data;
    } catch (error) {
      console.error('HVAC Status API error:', error);
      throw error;
    }
  },

  diagnoseSystem: async (systemId: string): Promise<APIReponse<SystemDiagnosis>> => {
    try {
      const response = await api.get(`/api/hvac/systems/${systemId}/diagnose`);
      return response.data;
    } catch (error) {
      console.error('System Diagnosis API error:', error);
      throw error;
    }
  },

  getOptimizationSuggestions: async (systemId: string): Promise<APIReponse<string[]>> => {
    try {
      const response = await api.get(`/api/hvac/systems/${systemId}/optimize`);
      return response.data;
    } catch (error) {
      console.error('Optimization API error:', error);
      throw error;
    }
  },

  setTemperature: async (systemId: string, temperature: number): Promise<APIReponse<any>> => {
    try {
      const response = await api.post(`/api/hvac/systems/${systemId}/temperature`, {
        temperature,
      });
      return response.data;
    } catch (error) {
      console.error('Set Temperature API error:', error);
      throw error;
    }
  },

  setOperationMode: async (systemId: string, mode: string): Promise<APIReponse<any>> => {
    try {
      const response = await api.post(`/api/hvac/systems/${systemId}/mode`, {
        mode,
      });
      return response.data;
    } catch (error) {
      console.error('Set Operation Mode API error:', error);
      throw error;
    }
  },
};

// System Status API
export const systemAPI = {
  getHealth: async (): Promise<APIReponse<any>> => {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('Health API error:', error);
      throw error;
    }
  },

  getSystemStatus: async (): Promise<APIReponse<any>> => {
    try {
      const response = await api.get('/api/system-status');
      return response.data;
    } catch (error) {
      console.error('System Status API error:', error);
      throw error;
    }
  },
};

// Mock data for development
export const mockData = {
  hvacModels: [
    'Thermia Diplomat Duo',
    'Thermia Calibra',
    'Thermia Atlas',
    'Thermia Mega',
    'Thermia Classic',
    'Thermia Compact',
    'Other',
  ],
  
  projectStatuses: [
    { value: 'active', label: 'Active' },
    { value: 'resolved', label: 'Resolved' },
    { value: 'pending', label: 'Pending' },
  ],

  diagnosisStatuses: [
    { value: 'EXCELLENT', label: 'Excellent', color: 'text-green-600' },
    { value: 'GOOD', label: 'Good', color: 'text-blue-600' },
    { value: 'FAIR', label: 'Fair', color: 'text-yellow-600' },
    { value: 'POOR', label: 'Poor', color: 'text-orange-600' },
    { value: 'ERROR', label: 'Error', color: 'text-red-600' },
  ],
};

export default api; 