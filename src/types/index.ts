export interface HVACSystem {
  id: string;
  name: string;
  model: string;
  is_online: boolean;
  indoor_temperature?: number;
  outdoor_temperature?: number;
  hot_water_temperature?: number;
  heat_temperature?: number;
  operation_mode: string;
  active_alarms: string[];
  compressor_operational_time?: number;
  last_online?: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  hvac_model: string;
  issue_description: string;
  created_at: string;
  status: 'active' | 'resolved' | 'pending';
}

export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  system_id?: string;
}

export interface ChatAPIResponse {
  response: string;
  sessionId: string;
  timestamp: string;
}

export interface SystemDiagnosis {
  system_id: string;
  timestamp: string;
  status: 'EXCELLENT' | 'GOOD' | 'FAIR' | 'POOR' | 'ERROR';
  issues: string[];
  recommendations: string[];
  efficiency_score?: number;
}

export interface OptimizationSuggestion {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  category: 'temperature' | 'efficiency' | 'maintenance' | 'safety';
}

export interface APIReponse<T> {
  data?: T;
  error?: string;
  message?: string;
  timestamp: string;
} 