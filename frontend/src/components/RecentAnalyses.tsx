import React from 'react';
import { motion } from 'framer-motion';
import { FileCode, Shield, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

interface Analysis {
  id: string;
  fileName: string;
  type: 'code' | 'security' | 'pipeline';
  status: 'completed' | 'running' | 'failed';
  trustScore: number;
  timestamp: string;
  issues: number;
}

const RecentAnalyses: React.FC = () => {
  const analyses: Analysis[] = [
    {
      id: '1',
      fileName: 'auth.py',
      type: 'security',
      status: 'completed',
      trustScore: 0.92,
      timestamp: '2 minutes ago',
      issues: 0
    },
    {
      id: '2',
      fileName: 'pipeline.yml',
      type: 'pipeline',
      status: 'completed',
      trustScore: 0.78,
      timestamp: '5 minutes ago',
      issues: 2
    },
    {
      id: '3',
      fileName: 'user-service.js',
      type: 'code',
      status: 'running',
      trustScore: 0,
      timestamp: '1 minute ago',
      issues: 0
    },
    {
      id: '4',
      fileName: 'database.py',
      type: 'security',
      status: 'completed',
      trustScore: 0.65,
      timestamp: '8 minutes ago',
      issues: 3
    },
    {
      id: '5',
      fileName: 'api-gateway.ts',
      type: 'code',
      status: 'completed',
      trustScore: 0.88,
      timestamp: '12 minutes ago',
      issues: 1
    }
  ];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'code':
        return <FileCode className="h-4 w-4 text-blue-400" />;
      case 'security':
        return <Shield className="h-4 w-4 text-red-400" />;
      case 'pipeline':
        return <Clock className="h-4 w-4 text-green-400" />;
      default:
        return <FileCode className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-400" />;
      case 'running':
        return <Clock className="h-4 w-4 text-yellow-400 animate-spin" />;
      case 'failed':
        return <AlertTriangle className="h-4 w-4 text-red-400" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const getTrustScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-400';
    if (score >= 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'code':
        return 'Code Analysis';
      case 'security':
        return 'Security Scan';
      case 'pipeline':
        return 'Pipeline Check';
      default:
        return 'Analysis';
    }
  };

  return (
    <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-purple-500/20">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-medium text-white">Recent Analyses</h3>
        <button className="text-purple-400 hover:text-purple-300 text-sm transition-colors">
          View All
        </button>
      </div>

      <div className="space-y-4">
        {analyses.map((analysis, index) => (
          <motion.div
            key={analysis.id}
            className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-purple-500/30 transition-colors"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                {getTypeIcon(analysis.type)}
                {getStatusIcon(analysis.status)}
              </div>
              
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-white font-medium text-sm">
                    {analysis.fileName}
                  </span>
                  {analysis.issues > 0 && (
                    <span className="bg-red-500/20 text-red-400 px-2 py-1 rounded text-xs">
                      {analysis.issues} issue{analysis.issues > 1 ? 's' : ''}
                    </span>
                  )}
                </div>
                <div className="flex items-center space-x-2 mt-1">
                  <span className="text-gray-400 text-xs">
                    {getTypeLabel(analysis.type)}
                  </span>
                  <span className="text-gray-500 text-xs">•</span>
                  <span className="text-gray-400 text-xs">
                    {analysis.timestamp}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              {analysis.status === 'completed' && (
                <div className="text-right">
                  <div className={`text-sm font-medium ${getTrustScoreColor(analysis.trustScore)}`}>
                    {Math.round(analysis.trustScore * 100)}%
                  </div>
                  <div className="text-xs text-gray-400">Trust Score</div>
                </div>
              )}
              
              {analysis.status === 'running' && (
                <div className="text-right">
                  <div className="text-sm text-yellow-400">Running...</div>
                  <div className="text-xs text-gray-400">In Progress</div>
                </div>
              )}

              <button className="text-purple-400 hover:text-purple-300 text-sm transition-colors">
                View
              </button>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Quick Stats */}
      <div className="mt-6 pt-4 border-t border-gray-700">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-lg font-semibold text-green-400">
              {analyses.filter(a => a.status === 'completed').length}
            </div>
            <div className="text-xs text-gray-400">Completed</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-yellow-400">
              {analyses.filter(a => a.status === 'running').length}
            </div>
            <div className="text-xs text-gray-400">Running</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-red-400">
              {analyses.reduce((sum, a) => sum + a.issues, 0)}
            </div>
            <div className="text-xs text-gray-400">Issues Found</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecentAnalyses;