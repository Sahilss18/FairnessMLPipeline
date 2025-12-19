import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  AlertCircle, 
  CheckCircle, 
  Send, 
  TrendingUp, 
  BarChart3,
  FileText,
  Lightbulb
} from 'lucide-react';
import './App.css';
import AnalysisResults from './components/AnalysisResults';
import ExampleComments from './components/ExampleComments';
import Statistics from './components/Statistics';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [apiHealth, setApiHealth] = useState(null);
  const [activeTab, setActiveTab] = useState('analyze');

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/health`);
      setApiHealth(response.data);
    } catch (err) {
      setApiHealth({ status: 'unhealthy', model_loaded: false });
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    
    if (!comment.trim()) {
      setError('Please enter a comment to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze`, {
        comment: comment
      });
      
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze comment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleText) => {
    setComment(exampleText);
    setActiveTab('analyze');
  };

  const clearResults = () => {
    setComment('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <BarChart3 size={40} />
            <div>
              <h1>Fairness & Bias Detection System</h1>
              <p>AI-Powered Content Analysis for Autonomous Agents</p>
            </div>
          </div>
          
          {apiHealth && (
            <div className={`api-status ${apiHealth.model_loaded ? 'healthy' : 'unhealthy'}`}>
              {apiHealth.model_loaded ? (
                <>
                  <CheckCircle size={16} />
                  <span>Model Ready</span>
                </>
              ) : (
                <>
                  <AlertCircle size={16} />
                  <span>Model Not Loaded</span>
                </>
              )}
            </div>
          )}
        </div>
      </header>

      <main className="main-content">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'analyze' ? 'active' : ''}`}
            onClick={() => setActiveTab('analyze')}
          >
            <Send size={18} />
            Analyze
          </button>
          <button 
            className={`tab ${activeTab === 'examples' ? 'active' : ''}`}
            onClick={() => setActiveTab('examples')}
          >
            <Lightbulb size={18} />
            Examples
          </button>
          <button 
            className={`tab ${activeTab === 'statistics' ? 'active' : ''}`}
            onClick={() => setActiveTab('statistics')}
          >
            <TrendingUp size={18} />
            Model Stats
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'analyze' && (
            <div className="analyze-section">
              <div className="input-card">
                <h2>
                  <FileText size={24} />
                  Enter Comment for Analysis
                </h2>
                
                <form onSubmit={handleAnalyze}>
                  <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    placeholder="Type or paste a comment to analyze for bias and fairness..."
                    rows={6}
                    disabled={loading}
                  />
                  
                  <div className="button-group">
                    <button 
                      type="submit" 
                      className="analyze-btn"
                      disabled={loading || !apiHealth?.model_loaded}
                    >
                      {loading ? (
                        <>
                          <div className="spinner"></div>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <Send size={18} />
                          Analyze Comment
                        </>
                      )}
                    </button>
                    
                    {(result || error) && (
                      <button 
                        type="button" 
                        className="clear-btn"
                        onClick={clearResults}
                      >
                        Clear
                      </button>
                    )}
                  </div>
                </form>

                {error && (
                  <div className="error-message">
                    <AlertCircle size={20} />
                    <span>{error}</span>
                  </div>
                )}
              </div>

              {result && <AnalysisResults result={result} />}
            </div>
          )}

          {activeTab === 'examples' && (
            <ExampleComments onExampleClick={handleExampleClick} />
          )}

          {activeTab === 'statistics' && (
            <Statistics />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Multi-Phase Machine Learning System for Identifying Bias in Autonomous Agents</p>
        <p className="footer-note">Phase 1: Baseline Model | Phase 2: Sentence-BERT Embeddings | Phase 3: Autoregressive Reasoning (Planned)</p>
      </footer>
    </div>
  );
}

export default App;
