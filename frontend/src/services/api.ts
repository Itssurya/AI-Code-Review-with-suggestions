import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface CodeReviewRequest {
  code: string;
  language: string;
  file_name: string;
  include_static_analysis?: boolean;
  include_ai_analysis?: boolean;
  focus_areas?: string[];
}

export interface CodeReviewResponse {
  review_id: string;
  timestamp: string;
  language: string;
  file_name: string;
  static_analysis?: {
    tool: string;
    issues: Array<{
      type: string;
      severity: 'low' | 'medium' | 'high';
      line?: number;
      column?: number;
      message: string;
      suggestion?: string;
      rule_id?: string;
      tool: string;
    }>;
    score: number;
    summary: string;
  };
  ai_analysis?: {
    score: number;
    issues: Array<{
      type: string;
      severity: 'low' | 'medium' | 'high';
      message: string;
      line?: number;
      suggestion?: string;
    }>;
    suggestions: Array<{
      type: string;
      description: string;
      code?: string;
      reason?: string;
    }>;
    security_concerns: Array<{
      type: string;
      severity: 'low' | 'medium' | 'high' | 'critical';
      description: string;
      mitigation: string;
      cwe_id?: string;
    }>;
    performance_notes: Array<{
      area: string;
      issue: string;
      suggestion: string;
      impact_level?: string;
    }>;
    readability_score: number;
    maintainability_score: number;
    summary: string;
    raw_response: any;
  };
  overall_score: number;
  total_issues: number;
  critical_issues: number;
  security_issues: number;
  summary: string;
  recommendations: string[];
  processing_time_ms: number;
  tools_used: string[];
}

export interface BatchReviewRequest {
  files: Array<{
    code: string;
    language: string;
    file_name: string;
  }>;
  include_static_analysis?: boolean;
  include_ai_analysis?: boolean;
}

export interface DashboardMetrics {
  total_reviews: number;
  average_score: number;
  most_common_issues: Array<{
    type: string;
    count: number;
  }>;
  language_distribution: Record<string, number>;
  security_issues_count: number;
  performance_issues_count: number;
  recent_reviews: Array<{
    review_id: string;
    timestamp: string;
    file_name: string;
    language: string;
    overall_score: number;
    total_issues: number;
    summary: string;
  }>;
}

export const apiService = {
  // Health check
  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await api.get('/health');
    return response.data;
  },

  // Single code review
  async reviewCode(request: CodeReviewRequest): Promise<CodeReviewResponse> {
    const response = await api.post('/api/v1/review', request);
    return response.data;
  },

  // Batch code review
  async reviewBatch(request: BatchReviewRequest): Promise<any> {
    const response = await api.post('/api/v1/review/batch', request);
    return response.data;
  },

  // Get dashboard metrics
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    const response = await api.get('/api/v1/dashboard/metrics');
    return response.data;
  },

  // Get supported languages
  async getSupportedLanguages(): Promise<string[]> {
    const response = await api.get('/api/v1/languages');
    return response.data;
  },

  // Code refactoring
  async refactorCode(code: string, language: string, improvementType: string): Promise<any> {
    const response = await api.post('/api/v1/refactor', {
      code,
      language,
      improvement_type: improvementType,
    });
    return response.data;
  },
};

export default apiService;
