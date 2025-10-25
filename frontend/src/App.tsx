import React, { useState, useEffect } from 'react';
import { CodeEditor } from './components/CodeEditor';
import { ReviewResults } from './components/ReviewResults';
import { Dashboard } from './components/Dashboard';
import { History } from './components/History';
import { Header } from './components/Header';
import { LoadingSpinner } from './components/LoadingSpinner';
import { apiService, CodeReviewResponse } from './services/api';
import { Code2, BarChart3, FileText, Settings } from 'lucide-react';

type TabType = 'editor' | 'dashboard' | 'history';

interface ReviewHistoryItem {
  id: string;
  timestamp: string;
  file_name: string;
  language: string;
  overall_score: number;
  total_issues: number;
  summary: string;
  review_data: CodeReviewResponse;
}

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('editor');
  const [isLoading, setIsLoading] = useState(false);
  const [reviewResult, setReviewResult] = useState<CodeReviewResponse | null>(null);
  const [apiStatus, setApiStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');
  const [reviewHistory, setReviewHistory] = useState<ReviewHistoryItem[]>([]);

  useEffect(() => {
    checkApiStatus();
    loadReviewHistory();
  }, []);

  const loadReviewHistory = () => {
    try {
      const saved = localStorage.getItem('ai-code-reviewer-history');
      if (saved) {
        setReviewHistory(JSON.parse(saved));
      }
    } catch (error) {
      console.error('Failed to load review history:', error);
    }
  };

  const saveReviewHistory = (history: ReviewHistoryItem[]) => {
    try {
      localStorage.setItem('ai-code-reviewer-history', JSON.stringify(history));
    } catch (error) {
      console.error('Failed to save review history:', error);
    }
  };

  const checkApiStatus = async () => {
    try {
      await apiService.healthCheck();
      setApiStatus('connected');
    } catch (error) {
      setApiStatus('disconnected');
    }
  };

  const handleCodeReview = async (code: string, language: string, fileName: string) => {
    setIsLoading(true);
    try {
      const result = await apiService.reviewCode({
        code,
        language,
        file_name: fileName,
        include_static_analysis: true,
        include_ai_analysis: true,
        focus_areas: ['security', 'performance', 'readability'],
      });
      setReviewResult(result);
      
      // Save to history
      const historyItem: ReviewHistoryItem = {
        id: result.review_id,
        timestamp: result.timestamp,
        file_name: result.file_name,
        language: result.language,
        overall_score: result.overall_score,
        total_issues: result.total_issues,
        summary: result.summary,
        review_data: result,
      };
      
      const newHistory = [historyItem, ...reviewHistory];
      setReviewHistory(newHistory);
      saveReviewHistory(newHistory);
      
      setActiveTab('editor'); // Stay on editor tab to show results
    } catch (error) {
      console.error('Review failed:', error);
      // You could add a toast notification here
      alert('Code review failed. Please check the console for details.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadReview = (review: CodeReviewResponse) => {
    setReviewResult(review);
    setActiveTab('editor');
  };

  const handleDeleteReview = (id: string) => {
    const newHistory = reviewHistory.filter(item => item.id !== id);
    setReviewHistory(newHistory);
    saveReviewHistory(newHistory);
  };

  const tabs = [
    { id: 'editor' as TabType, label: 'Code Editor', icon: Code2 },
    { id: 'dashboard' as TabType, label: 'Dashboard', icon: BarChart3 },
    { id: 'history' as TabType, label: 'History', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header apiStatus={apiStatus} onRefreshStatus={checkApiStatus} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Main Content */}
        <div className="space-y-8">
          {activeTab === 'editor' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="space-y-6">
                <CodeEditor onReview={handleCodeReview} isLoading={isLoading} />
              </div>
              <div className="space-y-6">
                <ReviewResults result={reviewResult} isLoading={isLoading} />
              </div>
            </div>
          )}

          {activeTab === 'dashboard' && (
            <Dashboard />
          )}

          {activeTab === 'history' && (
            <History 
              reviewHistory={reviewHistory}
              onLoadReview={handleLoadReview}
              onDeleteReview={handleDeleteReview}
            />
          )}
        </div>
      </div>

      {/* Loading Overlay */}
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 flex items-center space-x-4">
            <LoadingSpinner />
            <span className="text-lg font-medium text-gray-900">Analyzing your code...</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
