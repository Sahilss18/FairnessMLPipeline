import React, { useState } from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  Activity,
  Eye,
  Hash,
  Brain,
  Info,
  Sparkles,
  Target,
  TrendingUp,
  Shield,
  CheckCircle2
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { API_BASE_URL } from '../config';

const AnalysisResults = ({ result, mode = 'baseline' }) => {
  // State for audit verification (must be before early return)
  const [verifying, setVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);
  
  if (!result) return null;

  const {
    prediction,
    confidence,
    semantic_analysis,
    embedding_stats,
    comment,
    reasoning,
    autoregressive_reasoning: autoregressiveReasoning,
    model_comparison: modelComparisonData,
    audit
  } = result;
  
  // Verify audit chain integrity
  const handleVerifyChain = async () => {
    setVerifying(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/audit/verify`);
      const data = await response.json();
      setVerificationResult(data);
    } catch (error) {
      setVerificationResult({ verified: false, error: error.message });
    } finally {
      setVerifying(false);
    }
  };
  
  // Use the autoregressive model prediction when selected, otherwise use baseline.
  const displayPrediction = (mode === 'autoregressive' && autoregressiveReasoning?.prediction !== undefined) 
    ? autoregressiveReasoning.prediction 
    : prediction;
  const displayConfidence = (mode === 'autoregressive' && autoregressiveReasoning?.reasoning_confidence !== undefined)
    ? autoregressiveReasoning.reasoning_confidence
    : confidence;

  const autoregressiveModel = modelComparisonData?.autoregressive_model;
  const autoregressiveDetailed = modelComparisonData?.comparison_metrics?.autoregressive_detailed;
  
  // Debug logging
  console.log('AnalysisResults Debug:', {
    mode,
    baseline_prediction: prediction,
    autoregressive_prediction: autoregressiveReasoning?.prediction,
    displayPrediction,
    hasAutoregressiveReasoning: !!autoregressiveReasoning
  });
  
  // Handle both string ('biased'/'fair') and numeric (1/0) prediction formats
  const isBiased = displayPrediction === 'biased' || displayPrediction === 1;
  // Prepare semantic comparison data
  const semanticComparison = semantic_analysis ? [
    { 
      name: 'Fair', 
      similarity: parseFloat((semantic_analysis.similarity_to_positive * 100).toFixed(1)),
    },
    { 
      name: 'Biased', 
      similarity: parseFloat((semantic_analysis.similarity_to_toxic * 100).toFixed(1)),
    }
  ] : [];

  // Embedding stats radar
  const embeddingRadarData = embedding_stats ? [
    { metric: 'Mean', value: Math.abs(embedding_stats.mean * 100) },
    { metric: 'Std', value: embedding_stats.std * 100 },
    { metric: 'Min', value: Math.abs(embedding_stats.min * 100) },
    { metric: 'Max', value: embedding_stats.max * 100 },
    { metric: 'Norm', value: (embedding_stats.norm / 10) * 100 }
  ] : [];

  const confidenceLevel = reasoning?.confidence_level || (displayConfidence > 0.7 ? 'high' : displayConfidence > 0.5 ? 'medium' : 'low');

  return (
    <div className="space-y-4 animate-in slide-in-from-bottom duration-500">
      {/* Main Result - Chat Bubble Style */}
      <div className={`rounded-3xl overflow-hidden border ${
        isBiased 
          ? 'bg-gradient-to-br from-red-500/10 to-orange-500/10 border-red-500/30' 
          : 'bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border-emerald-500/30'
      }`}>
        <div className="p-6">
          <div className="flex items-start gap-4 mb-4">
            <div className={`p-3 rounded-2xl ${
              isBiased ? 'bg-red-500' : 'bg-emerald-500'
            } shadow-lg`}>
              {isBiased ? (
                <AlertTriangle className="w-8 h-8 text-white" />
              ) : (
                <CheckCircle className="w-8 h-8 text-white" />
              )}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <h2 className={`text-2xl font-bold ${
                  isBiased ? 'text-red-400' : 'text-emerald-400'
                }`}>
                  {isBiased ? 'Biased Content Detected' : 'Fair Content'}
                </h2>
                {mode === 'autoregressive' && (
                  <span className="px-3 py-1 bg-gradient-to-r from-purple-500 to-indigo-600 text-white text-xs font-bold rounded-full">
                    Autoregressive Model
                  </span>
                )}
                {mode === 'baseline' && (
                  <span className="px-3 py-1 bg-gradient-to-r from-pink-500 to-purple-600 text-white text-xs font-bold rounded-full">
                    Baseline
                  </span>
                )}
              </div>
              <p className="text-gray-400">
                {mode === 'autoregressive' 
                  ? (isBiased 
                      ? 'Autoregressive model detected bias or disrespectful language in this content' 
                      : 'Autoregressive model found this content to be fair and respectful')
                  : (isBiased 
                      ? 'This content may contain bias or discriminatory patterns' 
                      : 'This content appears fair and unbiased')}
              </p>
            </div>
          </div>

          {/* Confidence Bar - Only show for Baseline mode */}
          {mode !== 'autoregressive' && (
            <div className="bg-[#1a1a1a] border border-gray-800 rounded-2xl p-4 mb-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-pink-500" />
                  <span className="font-semibold text-gray-300">Confidence</span>
                </div>
                <span className="text-2xl font-black bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
                  {(displayConfidence * 100).toFixed(1)}%
                </span>
              </div>
              <div className="relative h-3 bg-gray-900 rounded-full overflow-hidden">
                <div 
                  className={`absolute top-0 left-0 h-full rounded-full transition-all duration-1000 bg-gradient-to-r ${
                    confidenceLevel === 'high' 
                      ? 'from-emerald-500 to-teal-500' 
                      : confidenceLevel === 'medium'
                      ? 'from-amber-500 to-orange-500'
                      : 'from-red-500 to-pink-500'
                  }`}
                  style={{ width: `${displayConfidence * 100}%` }}
                />
              </div>
              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>Low</span>
                <span>Medium</span>
                <span>High</span>
              </div>
            </div>
          )}

          {/* Analyzed Text */}
          <div className="bg-[#0f0f0f] border border-gray-800 rounded-2xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-pink-500" />
              <span className="text-sm font-semibold text-gray-400">Analyzed Text</span>
            </div>
            <p className="text-white italic leading-relaxed">
              "{comment}"
            </p>
          </div>

          {/* Low Confidence Warning */}
          {displayConfidence < 0.3 && (
            <div className="mt-4 bg-amber-500/10 border border-amber-500/30 rounded-2xl p-4">
              <div className="flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-bold text-amber-400 mb-2">⚠️ Uncertain Prediction</h4>
                  <p className="text-sm text-gray-300 mb-2">
                    The model has very low confidence ({(displayConfidence * 100).toFixed(0)}%) in this prediction.
                  </p>
                  <p className="text-xs text-gray-400">
                    This comment may contain <strong className="text-amber-400">subtle or institutional bias</strong> that 
                    the model was not trained to detect (e.g., socioeconomic discrimination, implicit bias, context-dependent cases).
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* AI Reasoning */}
          {reasoning && (
            <div className="mt-4 bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/30 rounded-2xl p-4">
              <div className="flex items-center gap-2 mb-3">
                <Brain className="w-5 h-5 text-purple-400" />
                <h4 className="font-bold text-purple-400">AI Reasoning</h4>
              </div>
              <div className="space-y-2 text-sm text-gray-300">
                <p><span className="text-purple-400 font-semibold">Model:</span> {reasoning.model_type}</p>
                <div>
                  <p className="text-purple-400 font-semibold mb-1">Key Factors:</p>
                  <ul className="space-y-1 ml-4">
                    {reasoning.key_factors.map((factor, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-pink-500">•</span>
                        <span>{factor}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Autoregressive Reasoning (Phase III) */}
      {autoregressiveReasoning && autoregressiveReasoning.available && (
        <div className="bg-gradient-to-br from-purple-500/10 to-indigo-500/10 border border-purple-500/30 rounded-3xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-purple-500 to-indigo-600 rounded-2xl shadow-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Phase III: Autoregressive Reasoning</h3>
              <p className="text-sm text-gray-400">Independent AI analysis with bias detection</p>
            </div>
          </div>

          {/* Autoregressive Override Warning */}
          {autoregressiveReasoning.disagreement && (
            <div className="bg-amber-500/20 border border-amber-500/50 rounded-2xl p-4 mb-4">
              <div className="flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-bold text-amber-400 mb-2">⚠️ Autoregressive Model Disagrees with Baseline!</h4>
                  <p className="text-sm text-gray-200 mb-2">
                    <strong>Baseline Model:</strong> {autoregressiveReasoning.baseline_prediction === 1 ? 'Biased' : 'Fair'} 
                    {' → '}
                    <strong className="text-purple-400">Autoregressive Model:</strong> {autoregressiveReasoning.prediction === 1 ? 'Biased ⚠️' : 'Fair ✓'}
                  </p>
                  <p className="text-xs text-gray-400">
                    The autoregressive model detected bias patterns that the baseline model missed. Its prediction is shown below.
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="bg-[#1a1a1a] border border-gray-800 rounded-2xl p-5 mb-4">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-4 h-4 text-purple-400" />
              <h4 className="font-semibold text-purple-400">Autoregressive Model Analysis</h4>
            </div>
            <p className="text-gray-200 leading-relaxed italic">
              "{autoregressiveReasoning.explanation}"
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            <div className="bg-[#0f0f0f] border border-gray-800 rounded-xl p-3">
              <div className="text-xs text-gray-500 mb-1">AI Model</div>
              <div className="text-purple-400 font-bold">{autoregressiveReasoning.model}</div>
            </div>
            <div className="bg-[#0f0f0f] border border-gray-800 rounded-xl p-3">
              <div className="text-xs text-gray-500 mb-1">Prediction</div>
              <div className={`font-bold ${autoregressiveReasoning.prediction === 1 ? 'text-red-400' : 'text-emerald-400'}`}>
                {autoregressiveReasoning.prediction === 1 ? 'Biased' : 'Fair'}
              </div>
            </div>
            <div className="bg-[#0f0f0f] border border-gray-800 rounded-xl p-3">
              <div className="text-xs text-gray-500 mb-1">vs Baseline</div>
              <div className={`font-bold ${autoregressiveReasoning.disagreement ? 'text-amber-400' : 'text-emerald-400'}`}>
                {autoregressiveReasoning.disagreement ? 'Disagree' : 'Agree'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Model Comparison (Phase III) */}
      {modelComparisonData && (
        <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 rounded-3xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl shadow-lg">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Model Comparison</h3>
              <p className="text-sm text-gray-400">Baseline vs Autoregressive Reasoning</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4 mb-4">
            {/* Baseline Model */}
            <div className="bg-[#1a1a1a] border border-gray-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-3">
                <Activity className="w-5 h-5 text-emerald-400" />
                <h4 className="font-bold text-emerald-400">{modelComparisonData.baseline_model.name}</h4>
              </div>
              <p className="text-sm text-gray-300 mb-3 italic">
                "{modelComparisonData.baseline_model.explanation}"
              </p>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-500">Type:</span>
                <span className="text-emerald-400 font-semibold">{modelComparisonData.baseline_model.type}</span>
              </div>
              <div className="flex items-center justify-between text-xs mt-1">
                <span className="text-gray-500">Length:</span>
                <span className="text-emerald-400 font-semibold">{modelComparisonData.baseline_model.explanation_length} words</span>
              </div>
            </div>

            {/* Autoregressive Model */}
            <div className="bg-[#1a1a1a] border border-gray-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-3">
                <Brain className="w-5 h-5 text-purple-400" />
                <h4 className="font-bold text-purple-400">{autoregressiveModel?.name}</h4>
              </div>
              <p className="text-sm text-gray-300 mb-3 italic">
                "{autoregressiveModel?.explanation}"
              </p>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-500">Type:</span>
                <span className="text-purple-400 font-semibold">{autoregressiveModel?.type}</span>
              </div>
              <div className="flex items-center justify-between text-xs mt-1">
                <span className="text-gray-500">Length:</span>
                <span className="text-purple-400 font-semibold">{autoregressiveModel?.explanation_length} words</span>
              </div>
            </div>
          </div>

          {/* Comparison Metrics */}
          <div className="bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-2xl p-4">
            <div className="flex items-center gap-2 mb-3">
              <Info className="w-4 h-4 text-cyan-400" />
              <span className="font-bold text-cyan-400">Analysis</span>
            </div>
            <div className="grid grid-cols-2 gap-3 mb-3 text-sm">
              <div className="flex items-center gap-2">
                <span className={modelComparisonData.comparison_metrics.baseline_concise ? 'text-emerald-400' : 'text-gray-500'}>
                  {modelComparisonData.comparison_metrics.baseline_concise ? '✓' : '○'}
                </span>
                <span className="text-gray-300">Baseline is concise</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={autoregressiveDetailed ? 'text-purple-400' : 'text-gray-500'}>
                  {autoregressiveDetailed ? '✓' : '○'}
                </span>
                <span className="text-gray-300">Autoregressive model is detailed</span>
              </div>
            </div>
            <div className="bg-[#1a1a1a] border border-gray-800 rounded-xl p-3">
              <p className="text-sm font-semibold text-cyan-400">
                💡 {modelComparisonData.comparison_metrics.recommendation}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Semantic Similarity */}
        {semantic_analysis && (
          <div className="bg-[#1a1a1a] border border-gray-800 rounded-3xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl">
                <Eye className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-bold text-white">
                Semantic Analysis
              </h3>
            </div>
            
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-3 mb-4">
              <p className="text-sm text-blue-400">{semantic_analysis.explanation}</p>
            </div>

            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={semanticComparison}>
                <defs>
                  <linearGradient id="fairGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity={1}/>
                    <stop offset="100%" stopColor="#059669" stopOpacity={1}/>
                  </linearGradient>
                  <linearGradient id="biasedGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#ef4444" stopOpacity={1}/>
                    <stop offset="100%" stopColor="#dc2626" stopOpacity={1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
                <XAxis 
                  dataKey="name" 
                  stroke="#d1d5db" 
                  style={{ fontSize: '13px', fontWeight: '600', fill: '#d1d5db' }} 
                  tick={{ fill: '#d1d5db' }}
                />
                <YAxis 
                  domain={[0, 100]} 
                  stroke="#d1d5db" 
                  tick={{ fill: '#d1d5db' }}
                  style={{ fontSize: '12px' }}
                />
                <Tooltip 
                  formatter={(value) => [`${value}%`, 'Similarity']}
                  contentStyle={{ 
                    backgroundColor: '#1a1a1a', 
                    border: '2px solid #ec4899',
                    borderRadius: '12px',
                    color: '#fff',
                    fontWeight: 'bold'
                  }}
                  labelStyle={{ color: '#ec4899', fontWeight: 'bold' }}
                />
                {semanticComparison.map((entry, index) => (
                  <Bar 
                    key={index}
                    dataKey="similarity" 
                    data={[entry]}
                    radius={[8, 8, 0, 0]}
                    fill={entry.name === 'Fair' ? 'url(#fairGradient)' : 'url(#biasedGradient)'}
                    label={{ position: 'top', fill: '#fff', fontWeight: 'bold', fontSize: 14 }}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>

            <div className="grid grid-cols-2 gap-2 mt-4">
              <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 text-center">
                <div className="text-emerald-400 text-xs font-semibold mb-1">Fair</div>
                <div className="text-2xl font-black text-emerald-400">
                  {(semantic_analysis.similarity_to_positive * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 text-center">
                <div className="text-red-400 text-xs font-semibold mb-1">Biased</div>
                <div className="text-2xl font-black text-red-400">
                  {(semantic_analysis.similarity_to_toxic * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Embedding Vector */}
        {embeddingRadarData.length > 0 && (
          <div className="bg-[#1a1a1a] border border-gray-800 rounded-3xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl">
                <Hash className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-bold text-white">
                Vector Analysis
              </h3>
            </div>

            <div className="bg-purple-500/10 border border-purple-500/30 rounded-xl p-3 mb-4">
              <p className="text-sm text-purple-400">
                384-dimensional embedding vector statistics
              </p>
            </div>

            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={embeddingRadarData}>
                <PolarGrid stroke="#505050" strokeWidth={1.5} />
                <PolarAngleAxis 
                  dataKey="metric" 
                  stroke="#d1d5db" 
                  style={{ fontSize: '12px', fontWeight: '600' }} 
                  tick={{ fill: '#d1d5db' }}
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 100]} 
                  stroke="#d1d5db" 
                  tick={{ fill: '#d1d5db' }}
                  style={{ fontSize: '11px' }}
                />
                <Radar 
                  name="Stats" 
                  dataKey="value" 
                  stroke="#ec4899" 
                  fill="#ec4899" 
                  fillOpacity={0.6}
                  strokeWidth={3}
                />
                <Tooltip 
                  formatter={(value) => [value.toFixed(2), 'Value']}
                  contentStyle={{ 
                    backgroundColor: '#1a1a1a', 
                    border: '2px solid #8b5cf6',
                    borderRadius: '12px',
                    color: '#fff',
                    fontWeight: 'bold'
                  }}
                  labelStyle={{ color: '#8b5cf6', fontWeight: 'bold' }}
                />
              </RadarChart>
            </ResponsiveContainer>

            <div className="grid grid-cols-3 gap-2 mt-4 text-center text-xs">
              <div className="bg-[#0f0f0f] border border-gray-800 rounded-lg p-2">
                <div className="text-gray-500 mb-1">Dim</div>
                <div className="text-pink-400 font-bold">{embedding_stats.dimension}</div>
              </div>
              <div className="bg-[#0f0f0f] border border-gray-800 rounded-lg p-2">
                <div className="text-gray-500 mb-1">Norm</div>
                <div className="text-pink-400 font-bold">{embedding_stats.norm.toFixed(2)}</div>
              </div>
              <div className="bg-[#0f0f0f] border border-gray-800 rounded-lg p-2">
                <div className="text-gray-500 mb-1">Mean</div>
                <div className="text-pink-400 font-bold">{embedding_stats.mean.toFixed(3)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Model Limitations */}
      <div className="bg-amber-500/5 border border-amber-500/30 rounded-3xl p-6">
        <div className="flex items-start gap-3 mb-4">
          <Info className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="text-lg font-bold text-amber-400 mb-2">⚠️ Important: Model Limitations</h3>
            <p className="text-sm text-gray-300 mb-2">
              <strong>Training Focus:</strong> This model was trained on explicit toxic language and direct discrimination 
              (insults, hate speech, identity attacks). <strong>Accuracy: 80.08%</strong> on test data.
            </p>
            <p className="text-sm text-amber-400 mb-4">
              <strong>⚠️ May NOT detect subtle or institutional bias</strong> like socioeconomic discrimination, 
              implicit bias in decision-making, or context-dependent cases.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4">
            <p className="font-bold text-emerald-400 mb-2">✓ Detects Well:</p>
            <ul className="space-y-1 text-gray-300">
              <li>• Direct discrimination & hate speech</li>
              <li>• Toxic language & insults</li>
              <li>• Identity attacks (race, gender, religion)</li>
              <li>• Explicit stereotypes</li>
            </ul>
          </div>

          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4">
            <p className="font-bold text-red-400 mb-2">✗ Often Misses:</p>
            <ul className="space-y-1 text-gray-300">
              <li>• Socioeconomic bias (class discrimination)</li>
              <li>• Subtle institutional bias</li>
              <li>• Context-dependent discrimination</li>
              <li>• Sarcasm, irony & implicit bias</li>
            </ul>
          </div>
        </div>
      </div>
      
      {/* Audit Chain Badge */}
      {audit && audit.logged && (
        <div className="bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-blue-500/30 rounded-2xl p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500 rounded-lg">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h4 className="font-bold text-blue-400">🔐 Logged to Audit Chain</h4>
                <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 text-xs rounded-full">Verified</span>
              </div>
              <p className="text-xs text-gray-400 mb-2">
                ID: {audit.audit_id} | Hash: {audit.entry_hash.substring(0, 16)}... | {new Date(audit.timestamp).toLocaleString()}
              </p>
              
              {/* Verify Button */}
              <button
                onClick={handleVerifyChain}
                disabled={verifying}
                className="flex items-center gap-2 px-3 py-1.5 bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 text-xs rounded-lg transition-all disabled:opacity-50"
              >
                <CheckCircle2 className="w-3 h-3" />
                {verifying ? 'Verifying...' : 'Verify Chain Integrity'}
              </button>
              
              {/* Verification Result */}
              {verificationResult && (
                <div className={`mt-2 p-2 rounded-lg text-xs ${
                  verificationResult.verified 
                    ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300' 
                    : 'bg-red-500/10 border border-red-500/30 text-red-300'
                }`}>
                  {verificationResult.verified ? (
                    <>
                      <div className="flex items-center gap-1 font-bold mb-1">
                        <CheckCircle2 className="w-3 h-3" />
                        Chain Verified ✓
                      </div>
                      <div className="text-gray-400">
                        {verificationResult.total_entries} entries validated, 0 errors
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="flex items-center gap-1 font-bold mb-1">
                        <AlertTriangle className="w-3 h-3" />
                        Verification Failed ✗
                      </div>
                      <div className="text-gray-400">
                        {verificationResult.message || verificationResult.error}
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
