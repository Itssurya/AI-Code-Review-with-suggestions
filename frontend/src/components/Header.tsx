import React from 'react';
import { RefreshCw, Wifi, WifiOff, Loader } from 'lucide-react';

interface HeaderProps {
  apiStatus: 'connected' | 'disconnected' | 'checking';
  onRefreshStatus: () => void;
}

export const Header: React.FC<HeaderProps> = ({ apiStatus, onRefreshStatus }) => {
  const getStatusIcon = () => {
    switch (apiStatus) {
      case 'connected':
        return <Wifi className="w-4 h-4 text-green-500" />;
      case 'disconnected':
        return <WifiOff className="w-4 h-4 text-red-500" />;
      case 'checking':
        return <Loader className="w-4 h-4 text-yellow-500 animate-spin" />;
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case 'connected':
        return 'API Connected';
      case 'disconnected':
        return 'API Disconnected';
      case 'checking':
        return 'Checking...';
    }
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">AI Code Reviewer</h1>
                <p className="text-sm text-gray-500">Intelligent code analysis and review</p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 px-3 py-1 bg-gray-100 rounded-full">
              {getStatusIcon()}
              <span className="text-sm font-medium text-gray-700">{getStatusText()}</span>
            </div>
            
            <button
              onClick={onRefreshStatus}
              className="p-2 text-gray-500 hover:text-gray-700 transition-colors duration-200"
              title="Refresh API Status"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

