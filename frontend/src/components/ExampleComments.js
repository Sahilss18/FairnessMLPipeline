import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Copy, CheckCircle, Lightbulb, Shield, AlertTriangle, Sparkles } from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const ExampleComments = ({ onExampleClick }) => {
  const [examples, setExamples] = useState([]);
  const [loading, setLoading] = useState(true);
  const [copiedIndex, setCopiedIndex] = useState(null);

  useEffect(() => {
    fetchExamples();
  }, []);

  const fetchExamples = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/examples`);
      setExamples(response.data.examples);
    } catch (error) {
      console.error('Failed to fetch examples:', error);
      setExamples([
        { comment: "This is a fair and balanced statement.", label: "fair" },
        { comment: "That group is always causing problems.", label: "biased" },
        { comment: "The data shows interesting trends.", label: "fair" },
        { comment: "People from that country can't be trusted.", label: "biased" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-16 h-16 border-4 border-pink-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-gray-400 text-lg font-semibold">Loading examples...</p>
      </div>
    );
  }

  const biasedExamples = examples.filter(ex => ex.label === 'biased' || ex.label === 1);
  const fairExamples = examples.filter(ex => ex.label === 'fair' || ex.label === 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-[#1a1a1a] border border-gray-800 rounded-3xl p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl blur opacity-50"></div>
            <div className="relative p-2 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl">
              <Lightbulb className="w-6 h-6 text-white" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-white">
            Sample Comments
          </h2>
        </div>
        <p className="text-gray-400">
          Click to analyze or copy to modify
        </p>
      </div>

      {/* Examples Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Fair Examples */}
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-2xl p-4">
            <div className="flex items-center gap-3 text-emerald-400">
              <CheckCircle className="w-6 h-6" />
              <h3 className="text-xl font-bold">Fair Comments</h3>
              <span className="ml-auto bg-emerald-500/20 px-3 py-1 rounded-full text-sm font-bold">
                {fairExamples.length}
              </span>
            </div>
          </div>
          
          <div className="space-y-3">
            {fairExamples.map((example, index) => (
              <div 
                key={`fair-${index}`}
                className="bg-[#1a1a1a] border border-gray-800 hover:border-emerald-500/50 rounded-2xl p-4 transition-all hover:shadow-lg hover:shadow-emerald-500/10 group"
              >
                <div className="flex items-start gap-3 mb-3">
                  <div className="p-2 bg-emerald-500/10 rounded-lg">
                    <Shield className="w-4 h-4 text-emerald-400" />
                  </div>
                  <p className="text-gray-300 leading-relaxed flex-1 text-sm">
                    {example.comment}
                  </p>
                </div>
                
                <div className="flex gap-2">
                  <button
                    onClick={() => onExampleClick(example.comment)}
                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-sm font-bold rounded-xl hover:shadow-lg hover:shadow-emerald-500/30 transition-all"
                  >
                    <Sparkles className="w-3 h-3" />
                    Analyze
                  </button>
                  <button
                    onClick={() => handleCopy(example.comment, `fair-${index}`)}
                    className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                      copiedIndex === `fair-${index}`
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        : 'bg-[#0f0f0f] text-gray-400 border border-gray-800 hover:border-gray-700'
                    }`}
                  >
                    {copiedIndex === `fair-${index}` ? (
                      <CheckCircle className="w-4 h-4" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Biased Examples */}
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-red-500/20 to-orange-500/20 border border-red-500/30 rounded-2xl p-4">
            <div className="flex items-center gap-3 text-red-400">
              <AlertTriangle className="w-6 h-6" />
              <h3 className="text-xl font-bold">Biased Comments</h3>
              <span className="ml-auto bg-red-500/20 px-3 py-1 rounded-full text-sm font-bold">
                {biasedExamples.length}
              </span>
            </div>
          </div>
          
          <div className="space-y-3">
            {biasedExamples.map((example, index) => (
              <div 
                key={`biased-${index}`}
                className="bg-[#1a1a1a] border border-gray-800 hover:border-red-500/50 rounded-2xl p-4 transition-all hover:shadow-lg hover:shadow-red-500/10 group"
              >
                <div className="flex items-start gap-3 mb-3">
                  <div className="p-2 bg-red-500/10 rounded-lg">
                    <AlertTriangle className="w-4 h-4 text-red-400" />
                  </div>
                  <p className="text-gray-300 leading-relaxed flex-1 text-sm">
                    {example.comment}
                  </p>
                </div>
                
                <div className="flex gap-2">
                  <button
                    onClick={() => onExampleClick(example.comment)}
                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gradient-to-r from-red-500 to-orange-500 text-white text-sm font-bold rounded-xl hover:shadow-lg hover:shadow-red-500/30 transition-all"
                  >
                    <Sparkles className="w-3 h-3" />
                    Analyze
                  </button>
                  <button
                    onClick={() => handleCopy(example.comment, `biased-${index}`)}
                    className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                      copiedIndex === `biased-${index}`
                        ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                        : 'bg-[#0f0f0f] text-gray-400 border border-gray-800 hover:border-gray-700'
                    }`}
                  >
                    {copiedIndex === `biased-${index}` ? (
                      <CheckCircle className="w-4 h-4" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Info Card */}
      <div className="bg-blue-500/5 border border-blue-500/30 rounded-3xl p-6">
        <h3 className="text-lg font-bold text-blue-400 mb-4">💡 How to Use</h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div className="bg-[#1a1a1a] border border-gray-800 rounded-xl p-4">
            <p className="font-bold text-blue-400 mb-2">🔍 Analyze</p>
            <p className="text-gray-400">Click "Analyze" to test the AI model instantly</p>
          </div>
          <div className="bg-[#1a1a1a] border border-gray-800 rounded-xl p-4">
            <p className="font-bold text-blue-400 mb-2">📋 Copy</p>
            <p className="text-gray-400">Copy and modify to test edge cases</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExampleComments;
