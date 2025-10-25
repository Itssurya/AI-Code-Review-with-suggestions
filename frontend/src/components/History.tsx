import React, { useState, useEffect } from 'react';
import { FileText, Clock, Star, AlertTriangle, CheckCircle, Trash2, Eye } from 'lucide-react';
import { CodeReviewResponse } from '../services/api';

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

interface HistoryProps {
  reviewHistory: ReviewHistoryItem[];
  onLoadReview: (review: CodeReviewResponse) => void;
  onDeleteReview: (id: string) => void;
}

export const History: React.FC<HistoryProps> = ({ reviewHistory, onLoadReview, onDeleteReview }) => {
  const [filteredHistory, setFilteredHistory] = useState<ReviewHistoryItem[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'date' | 'score' | 'issues'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    let filtered = [...reviewHistory];

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.file_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.language.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.summary.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Sort
    filtered.sort((a, b) => {
      let comparison = 0;
      switch (sortBy) {
        case 'date':
          comparison = new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
          break;
        case 'score':
          comparison = a.overall_score - b.overall_score;
          break;
        case 'issues':
          comparison = a.total_issues - b.total_issues;
          break;
      }
      return sortOrder === 'asc' ? comparison : -comparison;
    });

    setFilteredHistory(filtered);
  }, [reviewHistory, searchTerm, sortBy, sortOrder]);

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <CheckCircle className="w-4 h-4" />;
    if (score >= 60) return <AlertTriangle className="w-4 h-4" />;
    return <AlertTriangle className="w-4 h-4" />;
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  if (reviewHistory.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <FileText className="w-5 h-5 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Review History</h2>
        </div>
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FileText className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Reviews Yet</h3>
          <p className="text-gray-600">Start reviewing code to see your history here.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <FileText className="w-6 h-6 text-primary-600" />
          <h2 className="text-2xl font-bold text-gray-900">Review History</h2>
          <span className="bg-primary-100 text-primary-800 text-sm font-medium px-2 py-1 rounded-full">
            {reviewHistory.length} reviews
          </span>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search by file name, language, or summary..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Sort By */}
          <div className="flex gap-2">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'date' | 'score' | 'issues')}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="date">Sort by Date</option>
              <option value="score">Sort by Score</option>
              <option value="issues">Sort by Issues</option>
            </select>

            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              {sortOrder === 'asc' ? '↑' : '↓'}
            </button>
          </div>
        </div>
      </div>

      {/* History List */}
      <div className="space-y-4">
        {filteredHistory.map((item) => (
          <div key={item.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="flex items-center space-x-2">
                    {getScoreIcon(item.overall_score)}
                    <span className={`px-2 py-1 rounded-full text-sm font-medium ${getScoreColor(item.overall_score)}`}>
                      {item.overall_score}/100
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">{item.file_name}</h3>
                  <span className="bg-gray-100 text-gray-700 text-sm px-2 py-1 rounded-full">
                    {item.language}
                  </span>
                </div>

                <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-4 h-4" />
                    <span>{formatDate(item.timestamp)}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <AlertTriangle className="w-4 h-4" />
                    <span>{item.total_issues} issues</span>
                  </div>
                </div>

                <p className="text-gray-700 text-sm mb-3 line-clamp-2">
                  {item.summary}
                </p>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onLoadReview(item.review_data)}
                    className="flex items-center space-x-1 px-3 py-1 bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 transition-colors"
                  >
                    <Eye className="w-4 h-4" />
                    <span>View Details</span>
                  </button>
                  <button
                    onClick={() => onDeleteReview(item.id)}
                    className="flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                    <span>Delete</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredHistory.length === 0 && searchTerm && (
        <div className="text-center py-8 text-gray-500">
          <FileText className="w-8 h-8 mx-auto mb-2" />
          <p>No reviews found matching "{searchTerm}"</p>
        </div>
      )}
    </div>
  );
};

