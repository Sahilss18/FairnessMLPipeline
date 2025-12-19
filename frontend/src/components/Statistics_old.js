import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TrendingUp, 
  Target, 
  Activity,
  Database,
  Layers,
  Award
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
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import './Statistics.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const COLORS = ['#667eea', '#764ba2', '#10b981', '#f59e0b'];

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
      <div className="stats-loading">
        <div className="spinner-large"></div>
        <p>Loading model statistics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="stats-error">
        <p>{error}</p>
        <button onClick={fetchStats} className="retry-btn">Retry</button>
      </div>
    );
  }

  if (!stats || !stats.baseline_model || !stats.embedding_model) {
    return <div className="stats-error"><p>No statistics available</p></div>;
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
    <div className="statistics-container">
      <div className="stats-header">
        <h2>
          <TrendingUp size={28} />
          Model Performance Statistics
        </h2>
        <p>Comprehensive analysis of the two-phase ML system</p>
      </div>

      {/* Key Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card purple">
          <div className="metric-icon">
            <Target size={32} />
          </div>
          <div className="metric-content">
            <h3>Phase 1 Accuracy</h3>
            <p className="metric-value">{(stats.baseline_model.accuracy * 100).toFixed(2)}%</p>
            <p className="metric-label">Baseline Random Forest</p>
          </div>
        </div>

        <div className="metric-card blue">
          <div className="metric-icon">
            <Activity size={32} />
          </div>
          <div className="metric-content">
            <h3>Phase 2 Accuracy</h3>
            <p className="metric-value">{(stats.embedding_model.accuracy * 100).toFixed(2)}%</p>
            <p className="metric-label">Sentence-BERT + RF</p>
          </div>
        </div>

        <div className="metric-card green">
          <div className="metric-icon">
            <Database size={32} />
          </div>
          <div className="metric-content">
            <h3>Total Samples</h3>
            <p className="metric-value">{stats.dataset.total_samples.toLocaleString()}</p>
            <p className="metric-label">Training Dataset Size</p>
          </div>
        </div>

        <div className="metric-card orange">
          <div className="metric-icon">
            <Layers size={32} />
          </div>
          <div className="metric-content">
            <h3>Embedding Dim</h3>
            <p className="metric-value">{stats.embedding_model.n_features}</p>
            <p className="metric-label">Vector Dimensions</p>
          </div>
        </div>
      </div>

      {/* Phase Comparison Chart */}
      <div className="chart-card">
        <h3>
          <Award size={20} />
          Phase Performance Comparison
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={phaseComparison}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="phase" />
            <YAxis domain={[0, 100]} />
            <Tooltip formatter={(value) => `${value.toFixed(2)}%`} />
            <Legend />
            <Bar dataKey="accuracy" fill="#667eea" radius={[8, 8, 0, 0]} />
            <Bar dataKey="ROC-AUC" fill="#764ba2" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="charts-row">
        {/* Dataset Distribution */}
        <div className="chart-card">
          <h3>
            <Database size={20} />
            Dataset Distribution
          </h3>
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
          <div className="dataset-stats">
            <div className="stat-row">
              <span>Training Samples:</span>
              <strong>{stats.dataset.train_size.toLocaleString()}</strong>
            </div>
            <div className="stat-row">
              <span>Test Samples:</span>
              <strong>{stats.dataset.test_size.toLocaleString()}</strong>
            </div>
            <div className="stat-row">
              <span>Train/Test Split:</span>
              <strong>80/20</strong>
            </div>
          </div>
        </div>

        {/* Model Parameters */}
        <div className="chart-card">
          <h3>
            <Layers size={20} />
            Model Architecture
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={modelParams}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="model" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="trees" fill="#10b981" name="Trees" />
              <Bar dataKey="features" fill="#f59e0b" name="Features" />
            </BarChart>
          </ResponsiveContainer>
          <div className="model-details">
            <div className="detail-row">
              <span>Baseline Trees:</span>
              <strong>{stats.baseline_model.n_estimators}</strong>
            </div>
            <div className="detail-row">
              <span>Embedding Trees:</span>
              <strong>{stats.embedding_model.n_estimators}</strong>
            </div>
            <div className="detail-row">
              <span>Embedding Model:</span>
              <strong>all-MiniLM-L6-v2</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Metrics Table */}
      <div className="detailed-metrics">
        <h3>Detailed Performance Metrics</h3>
        <div className="metrics-table">
          <div className="table-header">
            <span>Metric</span>
            <span>Phase 1: Baseline</span>
            <span>Phase 2: Embeddings</span>
          </div>
          <div className="table-row">
            <span className="metric-name">Accuracy</span>
            <span className="metric-val">{(stats.baseline_model.accuracy * 100).toFixed(4)}%</span>
            <span className="metric-val">{(stats.embedding_model.accuracy * 100).toFixed(4)}%</span>
          </div>
          <div className="table-row">
            <span className="metric-name">ROC-AUC Score</span>
            <span className="metric-val">{stats.baseline_model.roc_auc.toFixed(4)}</span>
            <span className="metric-val">{stats.embedding_model.roc_auc.toFixed(4)}</span>
          </div>
          <div className="table-row">
            <span className="metric-name">Number of Trees</span>
            <span className="metric-val">{stats.baseline_model.n_estimators}</span>
            <span className="metric-val">{stats.embedding_model.n_estimators}</span>
          </div>
          <div className="table-row">
            <span className="metric-name">Feature Count</span>
            <span className="metric-val">{stats.baseline_model.n_features}</span>
            <span className="metric-val">{stats.embedding_model.n_features}</span>
          </div>
        </div>
      </div>

      {/* System Information */}
      <div className="system-info">
        <h3>System Configuration</h3>
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Dataset:</span>
            <span className="info-value">AiFairness.csv</span>
          </div>
          <div className="info-item">
            <span className="info-label">Total Samples:</span>
            <span className="info-value">{stats.dataset.total_samples.toLocaleString()}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Baseline Features:</span>
            <span className="info-value">{stats.baseline_model.n_features} toxicity scores</span>
          </div>
          <div className="info-item">
            <span className="info-label">Embedding Model:</span>
            <span className="info-value">Sentence-BERT (all-MiniLM-L6-v2)</span>
          </div>
          <div className="info-item">
            <span className="info-label">Vector Dimensions:</span>
            <span className="info-value">{stats.embedding_model.n_features}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Algorithm:</span>
            <span className="info-value">Random Forest Classifier</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Statistics;
