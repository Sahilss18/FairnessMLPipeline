import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  AlertCircle, 
  CheckCircle, 
  Send, 
  TrendingUp, 
  BarChart3,
  Sparkles,
  Lightbulb,
  Brain,
  Shield,
  Zap
} from 'lucide-react';
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
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      {/* Animated Background Overlay */}
      <div className="fixed inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIj48cGF0aCBkPSJNMzYgMzRjMi4yMSAwIDQtMS43OSA0LTRzLTEuNzktNC00LTQtNCAxLjc5LTQgNCAxLjc5IDQgNCA0em0wLTZ2MiIvPjwvZz48L2c+PC9zdmc+')] opacity-20 pointer-events-none"></div>
      
      <div className="relative z-10">
        {/* Header */}
        <header className="backdrop-blur-lg bg-white/10 border-b border-white/20 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4 animate-float">
                <div className="p-3 bg-gradient-to-br from-white/20 to-white/5 rounded-2xl backdrop-blur-xl border border-white/30 shadow-2xl">
                  <Brain className="w-10 h-10 text-white" />
                </div>
                <div>
                  <h1 className="text-3xl font-extrabold text-white flex items-center gap-2">
                    AI Fairness Detector
                    <Sparkles className="w-6 h-6 text-yellow-300 animate-pulse" />
                  </h1>
                  <p className="text-white/80 text-sm font-medium mt-1">
                    Neural Bias Detection System • Powered by Transformer Models
                  </p>
                </div>
              </div>
              
              {apiHealth && (
                <div className={`flex items-center gap-2 px-5 py-3 rounded-xl backdrop-blur-xl border shadow-lg transition-all duration-300 ${
                  apiHealth.model_loaded 
                    ? 'bg-emerald-500/20 border-emerald-300/50 text-emerald-100' 
                    : 'bg-red-500/20 border-red-300/50 text-red-100'
                }`}>
                  {apiHealth.model_loaded ? (
                    <>
                      <CheckCircle className="w-5 h-5" />
                      <span className="font-semibold">Model Active</span>
                    </>
                  ) : (
                    <>
                      <AlertCircle className="w-5 h-5" />
                      <span className="font-semibold">Offline</span>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Tab Navigation */}
          <div className="flex space-x-2 mb-8">
            {[
              { id: 'analyze', icon: Zap, label: 'Analyze' },
              { id: 'examples', icon: Lightbulb, label: 'Examples' },
              { id: 'statistics', icon: TrendingUp, label: 'Statistics' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 ${
                  activeTab === tab.id
                    ? 'bg-white text-purple-600 shadow-2xl'
                    : 'bg-white/10 text-white backdrop-blur-md hover:bg-white/20 border border-white/20'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="transition-all duration-500">
            {activeTab === 'analyze' && (
              <div className="space-y-6">
                {/* Input Card */}
                <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl">
                      <Shield className="w-6 h-6 text-white" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800">
                      Bias Detection Analysis
                    </h2>
                  </div>
                  
                  <form onSubmit={handleAnalyze} className="space-y-6">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-3">
                        Enter text to analyze for bias and fairness
                      </label>
                      <textarea
                        value={comment}
                        onChange={(e) => setComment(e.target.value)}
                        placeholder="Type or paste a comment here... Our AI will analyze it for potential bias, discrimination, or unfair language patterns."
                        rows={6}
                        disabled={loading}
                        className="w-full px-5 py-4 rounded-2xl border-2 border-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-200 transition-all duration-300 text-gray-800 placeholder-gray-400 font-medium resize-none disabled:opacity-50 disabled:cursor-not-allowed"
                      />
                    </div>
                    
                    <div className="flex gap-4">
                      <button 
                        type="submit" 
                        disabled={loading || !apiHealth?.model_loaded}
                        className="flex-1 flex items-center justify-center gap-3 px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold rounded-2xl hover:shadow-2xl hover:scale-105 transform transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                      >
                        {loading ? (
                          <>
                            <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                            Analyzing with AI...
                          </>
                        ) : (
                          <>
                            <Send className="w-5 h-5" />
                            Analyze Comment
                          </>
                        )}
                      </button>
                      
                      {(result || error) && (
                        <button 
                          type="button" 
                          onClick={clearResults}
                          className="px-8 py-4 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold rounded-2xl transition-all duration-300 hover:scale-105 transform"
                        >
                          Clear
                        </button>
                      )}
                    </div>
                  </form>

                  {error && (
                    <div className="mt-6 flex items-center gap-3 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
                      <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
                      <span className="text-red-800 font-medium">{error}</span>
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

        {/* Footer */}
        <footer className="mt-16 pb-8 text-center text-white/70">
          <p className="text-sm">
            Built with React, Flask & Sentence-BERT • Trained on AiFairness Dataset
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
