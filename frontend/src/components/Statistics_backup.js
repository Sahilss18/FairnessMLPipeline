import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TrendingUp, 
  Target, 
  Activity,
  Database,
  Layers,
  Award,
  BarChart3,
  PieChart as PieIcon
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const COLORS = ['#8b5cf6', '#ec4899', '#10b981', '#f59e0b'];

const Statistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/stats`);
      setStats(response.data);
    } catch (err) {
      setError('Failed to load model statistics');
      console.error('Stats fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-16 h-16 border-4 border-purple-600 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-white text-lg font-semibold">Loading statistics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-3xl shadow-xl p-8 text-center">
        <p className="text-red-800 font-bold mb-4">{error}</p>
        <button 
          onClick={fetchStats}
          className="px-6 py-3 bg-red-600 text-white font-bold rounded-xl hover:bg-red-700 transition-all"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!stats || !stats.baseline_model || !stats.embedding_model) {
    return (
      <div className="bg-amber-50 border-2 border-amber-300 rounded-3xl shadow-xl p-8 text-center">
        <p className="text-amber-800 font-bold">No statistics available</p>
      </div>
    );
  }

  // Prepare data for visualizations
  const phaseComparison = [
    { 
      phase: 'Phase 1: Baseline', 
      accuracy: (stats.baseline_model.accuracy || 0) * 100,
      'ROC-AUC': (stats.baseline_model.roc_auc || 0) * 100
    },
    { 
      phase: 'Phase 2: Embeddings', 
      accuracy: (stats.embedding_model.accuracy || 0) * 100,
      'ROC-AUC': (stats.embedding_model.roc_auc || 0) * 100
    }
  ];

  const datasetDistribution = [
    { name: 'Training Set', value: stats.dataset.train_size },
    { name: 'Test Set', value: stats.dataset.test_size }
  ];

  const modelParams = [
    { model: 'Baseline', trees: stats.baseline_model.n_estimators, features: stats.baseline_model.n_features },
    { model: 'Embedding', trees: stats.embedding_model.n_estimators, features: stats.embedding_model.n_features }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-3 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl">
            <TrendingUp className="w-7 h-7 text-white" />
          </div>
          <div>
            <h2 className="text-3xl font-extrabold text-gray-800">
              Model Performance Statistics
            </h2>
            <p className="text-gray-600 text-lg font-medium mt-1">
              Comprehensive analysis of the two-phase ML system
            </p>
          </div>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-3xl shadow-2xl p-6 text-white transform hover:scale-105 transition-all duration-300">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              <Target className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold">Phase 1 Accuracy</h3>
          </div>
          <p className="text-4xl font-black mb-2">{(stats.baseline_model.accuracy * 100).toFixed(2)}%</p>
          <p className="text-purple-100 font-medium">Baseline Random Forest</p>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-3xl shadow-2xl p-6 text-white transform hover:scale-105 transition-all duration-300">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              <Activity className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold">Phase 2 Accuracy</h3>
          </div>
          <p className="text-4xl font-black mb-2">{(stats.embedding_model.accuracy * 100).toFixed(2)}%</p>
          <p className="text-blue-100 font-medium">Sentence-BERT + RF</p>
        </div>

        <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-3xl shadow-2xl p-6 text-white transform hover:scale-105 transition-all duration-300">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              <Database className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold">Total Samples</h3>
          </div>
          <p className="text-4xl font-black mb-2">{stats.dataset.total_samples.toLocaleString()}</p>
          <p className="text-emerald-100 font-medium">Training Dataset Size</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-3xl shadow-2xl p-6 text-white transform hover:scale-105 transition-all duration-300">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              <Layers className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold">Embedding Dim</h3>
          </div>
          <p className="text-4xl font-black mb-2">{stats.embedding_model.n_features}</p>
          <p className="text-orange-100 font-medium">Vector Dimensions</p>
        </div>
      </div>

      {/* Phase Comparison Chart */}
      <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl">
            <Award className="w-6 h-6 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-gray-800">
            Phase Performance Comparison
          </h3>
        </div>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={phaseComparison}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="phase" stroke="#6b7280" style={{ fontSize: '14px', fontWeight: '600' }} />
            <YAxis domain={[0, 100]} stroke="#6b7280" />
            <Tooltip formatter={(value) => `${value.toFixed(2)}%`} contentStyle={{ borderRadius: '12px' }} />
            <Legend />
            <Bar dataKey="accuracy" fill="#8b5cf6" radius={[12, 12, 0, 0]} />
            <Bar dataKey="ROC-AUC" fill="#ec4899" radius={[12, 12, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Dataset Distribution */}
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-xl">
              <PieIcon className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-gray-800">
              Dataset Distribution
            </h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={datasetDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {datasetDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => value.toLocaleString()} />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-2 mt-4">
            <div className="flex justify-between items-center bg-purple-50 rounded-lg p-3 border border-purple-200">
              <span className="text-gray-700 font-medium">Training Samples:</span>
              <strong className="text-purple-700 text-lg">{stats.dataset.train_size.toLocaleString()}</strong>
            </div>
            <div className="flex justify-between items-center bg-pink-50 rounded-lg p-3 border border-pink-200">
              <span className="text-gray-700 font-medium">Test Samples:</span>
              <strong className="text-pink-700 text-lg">{stats.dataset.test_size.toLocaleString()}</strong>
            </div>
            <div className="flex justify-between items-center bg-blue-50 rounded-lg p-3 border border-blue-200">
              <span className="text-gray-700 font-medium">Train/Test Split:</span>
              <strong className="text-blue-700 text-lg">80/20</strong>
            </div>
          </div>
        </div>

        {/* Model Parameters */}
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-gray-800">
              Model Architecture
            </h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={modelParams}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="model" stroke="#6b7280" style={{ fontSize: '14px', fontWeight: '600' }} />
              <YAxis stroke="#6b7280" />
              <Tooltip contentStyle={{ borderRadius: '12px' }} />
              <Legend />
              <Bar dataKey="trees" fill="#10b981" name="Trees" radius={[8, 8, 0, 0]} />
              <Bar dataKey="features" fill="#f59e0b" name="Features" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="space-y-2 mt-4">
            <div className="flex justify-between items-center bg-emerald-50 rounded-lg p-3 border border-emerald-200">
              <span className="text-gray-700 font-medium">Baseline Trees:</span>
              <strong className="text-emerald-700 text-lg">{stats.baseline_model.n_estimators}</strong>
            </div>
            <div className="flex justify-between items-center bg-amber-50 rounded-lg p-3 border border-amber-200">
              <span className="text-gray-700 font-medium">Embedding Trees:</span>
              <strong className="text-amber-700 text-lg">{stats.embedding_model.n_estimators}</strong>
            </div>
            <div className="flex justify-between items-center bg-blue-50 rounded-lg p-3 border border-blue-200">
              <span className="text-gray-700 font-medium">Embedding Model:</span>
              <strong className="text-blue-700 text-lg">all-MiniLM-L6-v2</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Metrics Table */}
      <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
        <h3 className="text-2xl font-bold text-gray-800 mb-6">Detailed Performance Metrics</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gradient-to-r from-purple-100 to-pink-100 border-b-2 border-purple-300">
                <th className="text-left p-4 font-bold text-gray-800">Metric</th>
                <th className="text-center p-4 font-bold text-gray-800">Phase 1: Baseline</th>
                <th className="text-center p-4 font-bold text-gray-800">Phase 2: Embeddings</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-gray-200 hover:bg-purple-50 transition-colors">
                <td className="p-4 font-medium text-gray-700">Accuracy</td>
                <td className="p-4 text-center font-bold text-purple-600">{(stats.baseline_model.accuracy * 100).toFixed(4)}%</td>
                <td className="p-4 text-center font-bold text-pink-600">{(stats.embedding_model.accuracy * 100).toFixed(4)}%</td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-purple-50 transition-colors">
                <td className="p-4 font-medium text-gray-700">ROC-AUC Score</td>
                <td className="p-4 text-center font-bold text-purple-600">{stats.baseline_model.roc_auc.toFixed(4)}</td>
                <td className="p-4 text-center font-bold text-pink-600">{stats.embedding_model.roc_auc.toFixed(4)}</td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-purple-50 transition-colors">
                <td className="p-4 font-medium text-gray-700">Number of Trees</td>
                <td className="p-4 text-center font-bold text-purple-600">{stats.baseline_model.n_estimators}</td>
                <td className="p-4 text-center font-bold text-pink-600">{stats.embedding_model.n_estimators}</td>
              </tr>
              <tr className="hover:bg-purple-50 transition-colors">
                <td className="p-4 font-medium text-gray-700">Feature Count</td>
                <td className="p-4 text-center font-bold text-purple-600">{stats.baseline_model.n_features}</td>
                <td className="p-4 text-center font-bold text-pink-600">{stats.embedding_model.n_features}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* System Information */}
      <div className="bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-indigo-300 rounded-3xl shadow-2xl p-8">
        <h3 className="text-2xl font-bold text-indigo-900 mb-6">System Configuration</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-white/70 rounded-xl p-4 border border-indigo-200">
            <span className="text-indigo-700 font-semibold text-sm">Dataset:</span>
            <p className="text-indigo-900 font-bold text-lg mt-1">AiFairness.csv</p>
          </div>
          <div className="bg-white/70 rounded-xl p-4 border border-indigo-200">
            <span className="text-indigo-700 font-semibold text-sm">Total Samples:</span>
            <p className="text-indigo-900 font-bold text-lg mt-1">{stats.dataset.total_samples.toLocaleString()}</p>
          </div>
          <div className="bg-white/70 rounded-xl p-4 border border-indigo-200">
            <span className="text-indigo-700 font-semibold text-sm">Baseline Features:</span>
            <p className="text-indigo-900 font-bold text-lg mt-1">{stats.baseline_model.n_features} toxicity scores</p>
          </div>
          <div className="bg-white/70 rounded-xl p-4 border border-indigo-200">
            <span className="text-indigo-700 font-semibold text-sm">Embedding Model:</span>
            <p className="text-indigo-900 font-bold text-lg mt-1">Sentence-BERT</p>
          </div>
          <div className="bg-white/70 rounded-xl p-4 border border-indigo-200">
            <span className="text-indigo-700 font-semibold text-sm">Vector Dimensions:</span>
            <p className="text-indigo-900 font-bold text-lg mt-1">{stats.embedding_model.n_features}</p>
          </div>
          <div className="bg-white/70 rounded-xl p-4 border border-indigo-200">
            <span className="text-indigo-700 font-semibold text-sm">Algorithm:</span>
            <p className="text-indigo-900 font-bold text-lg mt-1">Random Forest</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Statistics;
