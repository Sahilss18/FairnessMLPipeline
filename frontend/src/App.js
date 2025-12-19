import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  AlertCircle, 
  CheckCircle, 
  Send, 
  TrendingUp, 
  Sparkles,
  Lightbulb,
  Brain,
  Shield,
  Zap,
  Menu,
  X
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
  const [menuOpen, setMenuOpen] = useState(false);

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
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="bg-gradient-to-r from-[#1a1a1a] to-[#0f0f0f] border-b border-gray-800 sticky top-0 z-50 backdrop-blur-xl bg-opacity-90">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <button 
                onClick={() => setMenuOpen(!menuOpen)}
                className="lg:hidden p-2 rounded-xl bg-gradient-to-r from-pink-500 to-purple-600 text-white"
              >
                {menuOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-pink-500 to-purple-600 rounded-2xl blur-lg opacity-50"></div>
                  <div className="relative p-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-2xl">
                    <Brain className="w-7 h-7 text-white" />
                  </div>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">AI Fairness Detector</h1>
                  <p className="text-xs text-gray-400">Neural bias detection</p>
                </div>
              </div>
            </div>
            
            {apiHealth && (
              <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold ${
                apiHealth.model_loaded 
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' 
                  : 'bg-red-500/20 text-red-400 border border-red-500/30'
              }`}>
                {apiHealth.model_loaded ? (
                  <>
                    <CheckCircle size={14} />
                    <span className="hidden sm:inline">Active</span>
                  </>
                ) : (
                  <>
                    <AlertCircle size={14} />
                    <span className="hidden sm:inline">Offline</span>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      {menuOpen && (
        <div className="lg:hidden fixed inset-0 z-40 bg-black/90 backdrop-blur-sm" onClick={() => setMenuOpen(false)}>
          <div className="absolute top-20 left-4 right-4 bg-[#1a1a1a] border border-gray-800 rounded-2xl p-4 space-y-2">
            {[
              { id: 'analyze', icon: Zap, label: 'Analyze' },
              { id: 'examples', icon: Lightbulb, label: 'Examples' },
              { id: 'statistics', icon: TrendingUp, label: 'Statistics' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => { setActiveTab(tab.id); setMenuOpen(false); }}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
              >
                <tab.icon size={18} />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Desktop Tab Navigation */}
        <div className="hidden lg:flex space-x-2 mb-6">
          {[
            { id: 'analyze', icon: Zap, label: 'Analyze' },
            { id: 'examples', icon: Lightbulb, label: 'Examples' },
            { id: 'statistics', icon: TrendingUp, label: 'Statistics' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white shadow-lg shadow-pink-500/30'
                  : 'bg-[#1a1a1a] text-gray-400 hover:text-white border border-gray-800 hover:border-gray-700'
              }`}
            >
              <tab.icon size={18} />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="transition-all duration-300">
          {activeTab === 'analyze' && (
            <div className="space-y-6">
              {/* Input Card */}
              <div className="bg-[#1a1a1a] border border-gray-800 rounded-3xl shadow-2xl p-6 sm:p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-pink-500 to-purple-600 rounded-xl blur opacity-50"></div>
                    <div className="relative p-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-xl">
                      <Shield className="w-5 h-5 text-white" />
                    </div>
                  </div>
                  <h2 className="text-xl sm:text-2xl font-bold text-white">
                    Analyze Content
                  </h2>
                </div>
                
                <form onSubmit={handleAnalyze} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">
                      Enter text to analyze
                    </label>
                    <textarea
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      placeholder="Type or paste content to check for bias..."
                      rows={4}
                      disabled={loading}
                      className="w-full px-4 py-3 bg-[#0f0f0f] border border-gray-800 rounded-2xl focus:border-pink-500 focus:ring-2 focus:ring-pink-500/20 transition-all text-white placeholder-gray-500 resize-none disabled:opacity-50"
                    />
                  </div>
                  
                  <div className="flex gap-3">
                    <button 
                      type="submit" 
                      disabled={loading || !apiHealth?.model_loaded}
                      className="flex-1 flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white font-bold rounded-2xl hover:shadow-lg hover:shadow-pink-500/30 transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                    >
                      {loading ? (
                        <>
                          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <Send size={18} />
                          Analyze
                        </>
                      )}
                    </button>
                    
                    {(result || error) && (
                      <button 
                        type="button" 
                        onClick={clearResults}
                        className="px-6 py-4 bg-[#0f0f0f] hover:bg-gray-900 text-gray-400 hover:text-white font-bold rounded-2xl border border-gray-800 hover:border-gray-700 transition-all"
                      >
                        Clear
                      </button>
                    )}
                  </div>
                </form>

                {error && (
                  <div className="mt-4 flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/30 rounded-xl">
                    <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                    <span className="text-red-400 font-medium">{error}</span>
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
      <footer className="mt-16 pb-8 text-center text-gray-500 text-sm">
        <div className="flex items-center justify-center gap-2">
          <Sparkles size={14} className="text-pink-500" />
          <span>Powered by Sentence-BERT & Random Forest</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
