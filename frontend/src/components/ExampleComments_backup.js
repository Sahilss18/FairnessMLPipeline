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
      // Fallback examples
      setExamples([
        { comment: "This is a fair and balanced statement.", label: "fair" },
        { comment: "That group is always causing problems.", label: "biased" },
        { comment: "The data shows interesting trends.", label: "fair" },
        { comment: "People from that country can't be trusted.", label: "biased" },
        { comment: "We should consider all perspectives.", label: "fair" }
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
        <div className="w-16 h-16 border-4 border-purple-600 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-white text-lg font-semibold">Loading examples...</p>
      </div>
    );
  }

  const biasedExamples = examples.filter(ex => ex.label === 'biased' || ex.label === 1);
  const fairExamples = examples.filter(ex => ex.label === 'fair' || ex.label === 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-3 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl">
            <Lightbulb className="w-7 h-7 text-white" />
          </div>
          <h2 className="text-3xl font-extrabold text-gray-800">
            Sample Comments Library
          </h2>
        </div>
        <p className="text-gray-600 text-lg font-medium">
          Click any example to analyze it instantly, or copy to modify and test variations
        </p>
      </div>

      {/* Examples Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Fair Examples */}
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl shadow-xl p-6">
            <div className="flex items-center gap-3 text-white">
              <CheckCircle className="w-7 h-7" />
              <h3 className="text-2xl font-extrabold">Fair Comments</h3>
              <span className="ml-auto bg-white/30 px-4 py-1 rounded-full text-sm font-bold">
                {fairExamples.length} examples
              </span>
            </div>
          </div>
          
          <div className="space-y-4">
            {fairExamples.map((example, index) => (
              <div 
                key={`fair-${index}`}
                className="bg-white/95 backdrop-blur-xl rounded-2xl shadow-lg p-6 border-2 border-emerald-300 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 group"
              >
                <div className="flex items-start gap-3 mb-4">
                  <div className="p-2 bg-emerald-100 rounded-lg group-hover:bg-emerald-200 transition-colors">
                    <Shield className="w-5 h-5 text-emerald-600" />
                  </div>
                  <p className="text-gray-800 font-medium leading-relaxed flex-1">
                    {example.comment}
                  </p>
                </div>
                
                <div className="flex gap-3">
                  <button
                    onClick={() => onExampleClick(example.comment)}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-bold rounded-xl hover:shadow-lg hover:scale-105 transform transition-all duration-300"
                  >
                    <Sparkles className="w-4 h-4" />
                    Analyze
                  </button>
                  <button
                    onClick={() => handleCopy(example.comment, `fair-${index}`)}
                    className={`px-5 py-3 rounded-xl font-bold transition-all duration-300 transform hover:scale-105 ${
                      copiedIndex === `fair-${index}`
                        ? 'bg-emerald-100 text-emerald-700 border-2 border-emerald-400'
                        : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200'
                    }`}
                  >
                    {copiedIndex === `fair-${index}` ? (
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4" />
                        Copied!
                      </div>
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
          <div className="bg-gradient-to-r from-red-500 to-orange-500 rounded-2xl shadow-xl p-6">
            <div className="flex items-center gap-3 text-white">
              <AlertTriangle className="w-7 h-7" />
              <h3 className="text-2xl font-extrabold">Biased Comments</h3>
              <span className="ml-auto bg-white/30 px-4 py-1 rounded-full text-sm font-bold">
                {biasedExamples.length} examples
              </span>
            </div>
          </div>
          
          <div className="space-y-4">
            {biasedExamples.map((example, index) => (
              <div 
                key={`biased-${index}`}
                className="bg-white/95 backdrop-blur-xl rounded-2xl shadow-lg p-6 border-2 border-red-300 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 group"
              >
                <div className="flex items-start gap-3 mb-4">
                  <div className="p-2 bg-red-100 rounded-lg group-hover:bg-red-200 transition-colors">
                    <AlertTriangle className="w-5 h-5 text-red-600" />
                  </div>
                  <p className="text-gray-800 font-medium leading-relaxed flex-1">
                    {example.comment}
                  </p>
                </div>
                
                <div className="flex gap-3">
                  <button
                    onClick={() => onExampleClick(example.comment)}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-red-500 to-orange-500 text-white font-bold rounded-xl hover:shadow-lg hover:scale-105 transform transition-all duration-300"
                  >
                    <Sparkles className="w-4 h-4" />
                    Analyze
                  </button>
                  <button
                    onClick={() => handleCopy(example.comment, `biased-${index}`)}
                    className={`px-5 py-3 rounded-xl font-bold transition-all duration-300 transform hover:scale-105 ${
                      copiedIndex === `biased-${index}`
                        ? 'bg-red-100 text-red-700 border-2 border-red-400'
                        : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200'
                    }`}
                  >
                    {copiedIndex === `biased-${index}` ? (
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4" />
                        Copied!
                      </div>
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
      <div className="bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-300 rounded-3xl shadow-xl p-8">
        <h3 className="text-xl font-bold text-blue-900 mb-4">💡 How to Use Examples</h3>
        <div className="grid md:grid-cols-2 gap-4 text-gray-700">
          <div className="bg-white/70 rounded-xl p-4 border border-blue-200">
            <p className="font-bold text-blue-900 mb-2">🔍 Analyze</p>
            <p className="text-sm">Click "Analyze" to instantly test the AI model on that specific example and see detailed results</p>
          </div>
          <div className="bg-white/70 rounded-xl p-4 border border-blue-200">
            <p className="font-bold text-blue-900 mb-2">📋 Copy & Modify</p>
            <p className="text-sm">Copy examples and modify them to test edge cases and see how small changes affect the model's predictions</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExampleComments;
