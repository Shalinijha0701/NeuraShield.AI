import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Shield, Bug, Zap, DollarSign, Activity } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface Stats {
  totalAnalyses: number;
  avgTrustScore: number;
  vulnerabilitiesFound: number;
  bugsPrevented: number;
  pipelineOptimizations: number;
  costSavingsPercentage: number;
}

const DashboardStats: React.FC = () => {
  const [stats, setStats] = useState<Stats>({
    totalAnalyses: 1247,
    avgTrustScore: 0.87,
    vulnerabilitiesFound: 23,
    bugsPrevented: 156,
    pipelineOptimizations: 42,
    costSavingsPercentage: 35.2
  });

  const [chartData] = useState([
    { name: 'Mon', trustScore: 0.82, analyses: 45 },
    { name: 'Tue', trustScore: 0.85, analyses: 52 },
    { name: 'Wed', trustScore: 0.83, analyses: 48 },
    { name: 'Thu', trustScore: 0.88, analyses: 61 },
    { name: 'Fri', trustScore: 0.87, analyses: 58 },
    { name: 'Sat', trustScore: 0.89, analyses: 34 },
    { name: 'Sun', trustScore: 0.86, analyses: 29 }
  ]);

  const statCards = [
    {
      title: 'Total Analyses',
      value: stats.totalAnalyses.toLocaleString(),
      icon: Activity,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/20'
    },
    {
      title: 'Avg Trust Score',
      value: `${(stats.avgTrustScore * 100).toFixed(1)}%`,
      icon: TrendingUp,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-green-500/20'
    },
    {
      title: 'Vulnerabilities Found',
      value: stats.vulnerabilitiesFound.toString(),
      icon: Shield,
      color: 'text-red-400',
      bgColor: 'bg-red-500/10',
      borderColor: 'border-red-500/20'
    },
    {
      title: 'Bugs Prevented',
      value: stats.bugsPrevented.toString(),
      icon: Bug,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      borderColor: 'border-purple-500/20'
    },
    {
      title: 'Pipeline Optimizations',
      value: stats.pipelineOptimizations.toString(),
      icon: Zap,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      borderColor: 'border-yellow-500/20'
    },
    {
      title: 'Cost Savings',
      value: `${stats.costSavingsPercentage}%`,
      icon: DollarSign,
      color: 'text-emerald-400',
      bgColor: 'bg-emerald-500/10',
      borderColor: 'border-emerald-500/20'
    }
  ];

  return (
    <div>
      <h2 className="text-xl font-semibold text-white mb-6">Platform Metrics</h2>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            className={`${stat.bgColor} backdrop-blur-sm rounded-lg p-6 border ${stat.borderColor}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">{stat.title}</p>
                <p className={`text-2xl font-bold ${stat.color} mt-1`}>{stat.value}</p>
              </div>
              <stat.icon className={`h-8 w-8 ${stat.color}`} />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Trust Score Trend Chart */}
      <motion.div
        className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-purple-500/20"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <h3 className="text-lg font-medium text-white mb-4">Trust Score Trend (Last 7 Days)</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="name" 
                stroke="#9CA3AF"
                fontSize={12}
              />
              <YAxis 
                domain={[0.7, 1]}
                stroke="#9CA3AF"
                fontSize={12}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#F3F4F6'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="trustScore" 
                stroke="#8B5CF6" 
                strokeWidth={3}
                dot={{ fill: '#8B5CF6', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#8B5CF6', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    </div>
  );
};

export default DashboardStats;