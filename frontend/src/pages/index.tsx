import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Brain, Zap, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import DashboardStats from '../components/DashboardStats';
import TrustScoreCard from '../components/TrustScoreCard';
import RecentAnalyses from '../components/RecentAnalyses';

const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-purple-500/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <Shield className="h-8 w-8 text-purple-400" />
              <h1 className="text-2xl font-bold text-white">NeuraShield.AI</h1>
              <span className="text-sm text-purple-300">v1.0.0</span>
            </motion.div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-green-400">
                <CheckCircle className="h-4 w-4" />
                <span className="text-sm">All Shields Active</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Neural Shields Overview */}
        <motion.section 
          className="mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <h2 className="text-xl font-semibold text-white mb-6">Neural Shields Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Neural Code Brain */}
            <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-blue-500/20">
              <div className="flex items-center space-x-3 mb-4">
                <Brain className="h-6 w-6 text-blue-400" />
                <h3 className="text-lg font-medium text-white">Neural Code Brain</h3>
              </div>
              <p className="text-gray-300 text-sm mb-3">AI Code Reviewer + Bug Predictor</p>
              <div className="flex items-center justify-between">
                <span className="text-green-400 text-sm">Active</span>
                <span className="text-blue-400 text-sm">95% Accuracy</span>
              </div>
            </div>

            {/* Quantum Security Shield */}
            <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-red-500/20">
              <div className="flex items-center space-x-3 mb-4">
                <Shield className="h-6 w-6 text-red-400" />
                <h3 className="text-lg font-medium text-white">Quantum Security Shield</h3>
              </div>
              <p className="text-gray-300 text-sm mb-3">AI-Driven Code Protection</p>
              <div className="flex items-center justify-between">
                <span className="text-green-400 text-sm">Active</span>
                <span className="text-red-400 text-sm">0 Threats</span>
              </div>
            </div>

            {/* Adaptive DevOps Optimizer */}
            <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-green-500/20">
              <div className="flex items-center space-x-3 mb-4">
                <Zap className="h-6 w-6 text-green-400" />
                <h3 className="text-lg font-medium text-white">DevOps Optimizer</h3>
              </div>
              <p className="text-gray-300 text-sm mb-3">Smart Process Brain</p>
              <div className="flex items-center justify-between">
                <span className="text-green-400 text-sm">Learning</span>
                <span className="text-green-400 text-sm">35% Faster</span>
              </div>
            </div>
          </div>
        </motion.section>

        {/* Dashboard Stats */}
        <motion.section 
          className="mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <DashboardStats />
        </motion.section>

        {/* Trust Score and Recent Analyses */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <motion.section
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <TrustScoreCard />
          </motion.section>

          <motion.section
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <RecentAnalyses />
          </motion.section>
        </div>

        {/* Quick Actions */}
        <motion.section 
          className="mt-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <h2 className="text-xl font-semibold text-white mb-6">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded-lg transition-colors">
              Analyze Repository
            </button>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg transition-colors">
              Security Scan
            </button>
            <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded-lg transition-colors">
              Optimize Pipeline
            </button>
            <button className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-3 rounded-lg transition-colors">
              View Reports
            </button>
          </div>
        </motion.section>
      </main>
    </div>
  );
};

export default Dashboard;