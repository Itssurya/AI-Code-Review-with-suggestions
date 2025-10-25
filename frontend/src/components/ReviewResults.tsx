import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Clock, Star, Shield, Zap, Eye } from 'lucide-react';
import { CodeReviewResponse } from '../services/api';

interface ReviewResultsProps {
  result: CodeReviewResponse | null;
  isLoading: boolean;
}

export const ReviewResults: React.FC<ReviewResultsProps> = ({ result, isLoading }) => {
  if (isLoading) {
    return (
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Clock className="w-5 h-5 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Review Results</h2>
        </div>
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-gray-600">Analyzing your code...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Star className="w-5 h-5 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Review Results</h2>
        </div>
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Star className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Review</h3>
          <p className="text-gray-600">Enter your code and click "Review Code" to get AI-powered analysis and suggestions.</p>
        </div>
      </div>
    );
  }

  const overallScore = result.overall_score || 0;
  const aiAnalysis = result.ai_analysis;
  const staticAnalysis = result.static_analysis;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <CheckCircle className="w-5 h-5" />;
    if (score >= 60) return <AlertTriangle className="w-5 h-5" />;
    return <XCircle className="w-5 h-5" />;
  };

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Review Results</h2>
          <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${getScoreColor(overallScore)}`}>
            {getScoreIcon(overallScore)}
            <span className="font-semibold">{overallScore}/100</span>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{result.file_name}</div>
            <div className="text-sm text-gray-600">{result.language}</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{result.processing_time_ms}ms</div>
            <div className="text-sm text-gray-600">Processing Time</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{result.review_id.substring(0, 8)}...</div>
            <div className="text-sm text-gray-600">Review ID</div>
          </div>
        </div>
      </div>

      {/* AI Analysis */}
      {aiAnalysis && (
        <div className="card">
          <div className="flex items-center space-x-2 mb-4">
            <Zap className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-bold text-gray-900">AI Analysis</h3>
            <div className={`ml-auto flex items-center space-x-1 px-2 py-1 rounded-full ${getScoreColor(aiAnalysis.score)}`}>
              {getScoreIcon(aiAnalysis.score)}
              <span className="text-sm font-medium">{aiAnalysis.score}/100</span>
            </div>
          </div>

          <div className="space-y-4">
            {/* Summary */}
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Summary</h4>
              <p className="text-gray-700 bg-gray-50 p-3 rounded-lg">
                {aiAnalysis.summary || result.summary || 'No summary available'}
              </p>
            </div>

            {/* Issues */}
            {aiAnalysis.issues && aiAnalysis.issues.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Issues Found</h4>
                <div className="space-y-2">
                  {aiAnalysis.issues.map((issue, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                      <div className={`mt-1 ${issue.severity === 'high' ? 'text-red-500' : issue.severity === 'medium' ? 'text-yellow-500' : 'text-blue-500'}`}>
                        {issue.severity === 'high' ? <XCircle className="w-4 h-4" /> : 
                         issue.severity === 'medium' ? <AlertTriangle className="w-4 h-4" /> : 
                         <CheckCircle className="w-4 h-4" />}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">{issue.message}</div>
                        {issue.line && <div className="text-sm text-gray-600">Line {issue.line}</div>}
                        {issue.suggestion && (
                          <div className="text-sm text-gray-700 mt-1 p-2 bg-white rounded border-l-2 border-primary-500">
                            💡 {issue.suggestion}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Security Concerns */}
            {aiAnalysis.security_concerns && aiAnalysis.security_concerns.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Security Concerns</h4>
                <div className="space-y-2">
                  {aiAnalysis.security_concerns.map((concern, index) => (
                    <div key={index} className="p-3 bg-red-50 rounded-lg border-l-4 border-red-500">
                      <div className="font-medium text-red-900">{concern.type || 'Security Issue'}</div>
                      <div className="text-red-800 mt-1">{concern.description}</div>
                      {concern.mitigation && (
                        <div className="text-red-700 mt-2 text-sm">
                          <strong>Mitigation:</strong> {concern.mitigation}
                        </div>
                      )}
                      {concern.severity && (
                        <div className="text-red-600 mt-1 text-xs">
                          Severity: {concern.severity}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Performance Notes */}
            {aiAnalysis.performance_notes && aiAnalysis.performance_notes.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Performance Notes</h4>
                <div className="space-y-2">
                  {aiAnalysis.performance_notes.map((note, index) => (
                    <div key={index} className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
                      <div className="font-medium text-yellow-900">{note.area || 'Performance Issue'}</div>
                      <div className="text-yellow-800 mt-1">{note.issue}</div>
                      {note.suggestion && (
                        <div className="text-yellow-700 mt-2 text-sm">
                          <strong>Suggestion:</strong> {note.suggestion}
                        </div>
                      )}
                      {note.impact_level && (
                        <div className="text-yellow-600 mt-1 text-xs">
                          Impact: {note.impact_level}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Suggestions */}
            {aiAnalysis.suggestions && aiAnalysis.suggestions.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Suggestions</h4>
                <div className="space-y-2">
                  {aiAnalysis.suggestions.map((suggestion, index) => (
                    <div key={index} className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                      <div className="font-medium text-blue-900">{suggestion.type}</div>
                      <div className="text-blue-800 mt-1">{suggestion.description}</div>
                      {suggestion.reason && (
                        <div className="text-blue-700 mt-2 text-sm">
                          <strong>Why:</strong> {suggestion.reason}
                        </div>
                      )}
                      {suggestion.code && (
                        <pre className="mt-2 text-sm bg-blue-100 p-2 rounded overflow-x-auto">
                          <code>{suggestion.code}</code>
                        </pre>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Static Analysis */}
      {staticAnalysis && (
        <div className="card">
          <div className="flex items-center space-x-2 mb-4">
            <Shield className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-bold text-gray-900">Static Analysis</h3>
          </div>

          <div className="space-y-4">
            {/* Pylint Score */}
            {staticAnalysis && (
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-900">{staticAnalysis.tool} Score</span>
                  <span className={`px-2 py-1 rounded-full text-sm font-medium ${getScoreColor(staticAnalysis.score * 10)}`}>
                    {staticAnalysis.score}/10
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${staticAnalysis.score >= 8 ? 'bg-green-500' : staticAnalysis.score >= 6 ? 'bg-yellow-500' : 'bg-red-500'}`}
                    style={{ width: `${(staticAnalysis.score / 10) * 100}%` }}
                  ></div>
                </div>
                <div className="mt-2 text-sm text-gray-600">{staticAnalysis.summary}</div>
              </div>
            )}

            {/* Issues Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{result.total_issues}</div>
                <div className="text-sm text-gray-600">Total Issues</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{result.critical_issues}</div>
                <div className="text-sm text-gray-600">Critical Issues</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{result.security_issues}</div>
                <div className="text-sm text-gray-600">Security Issues</div>
              </div>
            </div>

            {/* Static Analysis Issues */}
            {staticAnalysis && staticAnalysis.issues && staticAnalysis.issues.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Static Analysis Issues</h4>
                <div className="space-y-2">
                  {staticAnalysis.issues.map((issue, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                      <div className={`mt-1 ${issue.severity === 'high' ? 'text-red-500' : issue.severity === 'medium' ? 'text-yellow-500' : 'text-blue-500'}`}>
                        {issue.severity === 'high' ? <XCircle className="w-4 h-4" /> : 
                         issue.severity === 'medium' ? <AlertTriangle className="w-4 h-4" /> : 
                         <CheckCircle className="w-4 h-4" />}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">{issue.message}</div>
                        {issue.line && <div className="text-sm text-gray-600">Line {issue.line}</div>}
                        {issue.rule_id && <div className="text-xs text-gray-500">Rule: {issue.rule_id}</div>}
                        {issue.suggestion && (
                          <div className="text-sm text-gray-700 mt-1 p-2 bg-white rounded border-l-2 border-primary-500">
                            💡 {issue.suggestion}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {result.recommendations && result.recommendations.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Recommendations</h4>
                <div className="space-y-2">
                  {result.recommendations.map((recommendation, index) => (
                    <div key={index} className="p-3 bg-green-50 rounded-lg border-l-4 border-green-500">
                      <div className="text-green-800">{recommendation}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
