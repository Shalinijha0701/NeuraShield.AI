import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Brain, Zap, TrendingUp } from 'lucide-react';

interface TrustScoreProps {
  score?: number;
  components?: {
    codeQuality: number;
    securityScore: number;
    pipelineEfficiency: number;
  };
}

const TrustScoreCard: React.FC<TrustScoreProps> = ({ 
  score = 0.87,
  components = {
    codeQuality: 0.92,
    securityScore: 0.85,
    pipelineEfficiency: 0.84
  }
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-400';
    if (score >= 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreGradient = (score: number) => {
    if (score >= 0.8) return 'from-green-500 to-emerald-500';
    if (score >= 0.6) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  const CircularProgress: React.FC<{ value: number; size?: number }> = ({ value, size = 120 }) => {
    const circumference = 2 * Math.PI * 45;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference - (value * circumference);

    return (
      <div className="relative" style={{ width: size, height: size }}>
        <svg
          className="transform -rotate-90"
          width={size}
          height={size}
          viewBox="0 0 100 100"
        >
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="currentColor"
            strokeWidth="8"
            fill="transparent"
            className="text-gray-700"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="url(#gradient)"
            strokeWidth="8"
            fill="transparent"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" className="stop-green-500" />
              <stop offset="100%" className="stop-emerald-500" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`text-2xl font-bold ${getScoreColor(value)}`}>
            {Math.round(value * 100)}%
          </span>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-purple-500/20">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-medium text-white">Overall Trust Score</h3>
        <TrendingUp className="h-5 w-5 text-green-400" />
      </div>

      {/* Main Trust Score */}
      <div className="flex items-center justify-center mb-8">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
        >
          <CircularProgress value={score} />
        </motion.div>
      </div>

      {/* Component Scores */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Brain className="h-4 w-4 text-blue-400" />
            <span className="text-gray-300 text-sm">Code Quality</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-700 rounded-full h-2">
              <motion.div
                className="bg-gradient-to-r from-blue-500 to-blue-400 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${components.codeQuality * 100}%` }}
                transition={{ delay: 0.4, duration: 1 }}
              />
            </div>
            <span className={`text-sm font-medium ${getScoreColor(components.codeQuality)}`}>
              {Math.round(components.codeQuality * 100)}%
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Shield className="h-4 w-4 text-red-400" />
            <span className="text-gray-300 text-sm">Security Score</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-700 rounded-full h-2">
              <motion.div
                className="bg-gradient-to-r from-red-500 to-red-400 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${components.securityScore * 100}%` }}
                transition={{ delay: 0.6, duration: 1 }}
              />
            </div>
            <span className={`text-sm font-medium ${getScoreColor(components.securityScore)}`}>
              {Math.round(components.securityScore * 100)}%
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Zap className="h-4 w-4 text-green-400" />
            <span className="text-gray-300 text-sm">Pipeline Efficiency</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-700 rounded-full h-2">
              <motion.div
                className="bg-gradient-to-r from-green-500 to-green-400 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${components.pipelineEfficiency * 100}%` }}
                transition={{ delay: 0.8, duration: 1 }}
              />
            </div>
            <span className={`text-sm font-medium ${getScoreColor(components.pipelineEfficiency)}`}>
              {Math.round(components.pipelineEfficiency * 100)}%
            </span>
          </div>
        </div>
      </div>

      {/* Trust Level Indicator */}
      <div className="mt-6 pt-4 border-t border-gray-700">
        <div className="flex items-center justify-between">
          <span className="text-gray-300 text-sm">Trust Level</span>
          <span className={`text-sm font-medium ${getScoreColor(score)}`}>
            {score >= 0.8 ? 'High' : score >= 0.6 ? 'Medium' : 'Low'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default TrustScoreCard;