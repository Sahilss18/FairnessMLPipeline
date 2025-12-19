import React from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  Activity,
  Percent,
  Eye,
  Hash,
  Brain,
  Info,
  Sparkles,
  TrendingUp,
  Target
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
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

const AnalysisResults = ({ result }) => {
  if (!result) return null;

  const { prediction, confidence, semantic_analysis, embedding_stats, comment, reasoning } = result;
  const isBiased = prediction === 'biased' || prediction === 1;

  // Prepare semantic comparison data
  const semanticComparison = semantic_analysis ? [
    { 
      name: 'Positive/Fair', 
      similarity: parseFloat((semantic_analysis.similarity_to_positive * 100).toFixed(1)),
    },
    { 
      name: 'Toxic/Biased', 
      similarity: parseFloat((semantic_analysis.similarity_to_toxic * 100).toFixed(1)),
    }
  ] : [];

  // Prepare confidence breakdown
  const confidenceData = [
    { name: 'Confidence', value: parseFloat((confidence * 100).toFixed(1)) },
    { name: 'Uncertainty', value: parseFloat(((1 - confidence) * 100).toFixed(1)) }
  ];

  // Embedding stats radar
  const embeddingRadarData = embedding_stats ? [
    { metric: 'Mean', value: Math.abs(embedding_stats.mean * 100) },
    { metric: 'Std Dev', value: embedding_stats.std * 100 },
    { metric: 'Min', value: Math.abs(embedding_stats.min * 100) },
    { metric: 'Max', value: embedding_stats.max * 100 },
    { metric: 'Norm', value: (embedding_stats.norm / 10) * 100 }
  ] : [];

  // Determine confidence level color
  const confidenceLevel = reasoning?.confidence_level || (confidence > 0.7 ? 'high' : confidence > 0.5 ? 'medium' : 'low');
  const confidenceLevelColor = confidenceLevel === 'high' ? 'text-emerald-600' : confidenceLevel === 'medium' ? 'text-amber-600' : 'text-red-600';

  return (
    <div className="space-y-6 animate-in slide-in-from-bottom duration-500">
      {/* Main Prediction Card with Gradient */}
      <div className={`rounded-3xl shadow-2xl overflow-hidden backdrop-blur-xl border-2 ${
        isBiased 
          ? 'bg-gradient-to-br from-red-50 to-orange-50 border-red-300' 
          : 'bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-300'
      }`}>
        <div className="p-8">
          <div className="flex items-start gap-4 mb-6">
            <div className={`p-4 rounded-2xl ${
              isBiased ? 'bg-red-500' : 'bg-emerald-500'
            } shadow-lg`}>
              {isBiased ? (
                <AlertTriangle className="w-12 h-12 text-white" />
              ) : (
                <CheckCircle className="w-12 h-12 text-white" />
              )}
            </div>
            <div className="flex-1">
              <h2 className={`text-3xl font-extrabold mb-2 ${
                isBiased ? 'text-red-700' : 'text-emerald-700'
              }`}>
                {isBiased ? '⚠️ Biased Content Detected' : '✓ Fair Content'}
              </h2>
              <p className="text-gray-700 text-lg font-medium">
                {isBiased 
                  ? 'This comment may contain bias, discrimination, or unfair language patterns' 
                  : 'This comment appears to be fair, balanced, and free of discriminatory language'}
              </p>
            </div>
          </div>

          {/* Confidence Meter */}
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 mb-6 border border-gray-200">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Target className="w-5 h-5 text-purple-600" />
                <span className="font-bold text-gray-700">Model Confidence Level:</span>
                <span className={`font-extrabold text-xl ${confidenceLevelColor}`}>
                  {confidenceLevel.toUpperCase()}
                </span>
              </div>
              <span className="text-3xl font-black text-purple-600">
                {(confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="relative h-4 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className={`absolute top-0 left-0 h-full rounded-full transition-all duration-1000 ${
                  confidenceLevel === 'high' 
                    ? 'bg-gradient-to-r from-emerald-400 to-emerald-600' 
                    : confidenceLevel === 'medium'
                    ? 'bg-gradient-to-r from-amber-400 to-amber-600'
                    : 'bg-gradient-to-r from-red-400 to-red-600'
                }`}
                style={{ width: `${confidence * 100}%` }}
              />
            </div>
          </div>

          {/* Analyzed Comment */}
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 border border-gray-200">
            <h4 className="font-bold text-gray-700 mb-3 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-600" />
              Analyzed Comment:
            </h4>
            <p className="text-gray-800 italic text-lg font-medium leading-relaxed">
              "{comment}"
            </p>
          </div>

          {/* AI Reasoning */}
          {reasoning && (
            <div className="mt-6 bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-200 rounded-2xl p-6">
              <h4 className="font-bold text-purple-900 mb-4 flex items-center gap-2 text-lg">
                <Brain className="w-6 h-6" /> 
                AI Model Reasoning
              </h4>
              <div className="space-y-3">
                <p className="text-gray-700">
                  <strong className="text-purple-700">Model Type:</strong> {reasoning.model_type}
                </p>
                <div>
                  <p className="font-bold text-purple-700 mb-2">Key Decision Factors:</p>
                  <ul className="space-y-2">
                    {reasoning.key_factors.map((factor, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-gray-700">
                        <span className="text-purple-500 font-bold">•</span>
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

      {/* Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Semantic Similarity Comparison */}
        {semantic_analysis && (
          <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-6 border border-white/50">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl">
                <Eye className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-800">
                Semantic Similarity Analysis
              </h3>
            </div>
            
            <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-4 mb-4">
              <div className="flex items-start gap-2">
                <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-blue-900 font-medium">{semantic_analysis.explanation}</p>
              </div>
            </div>

            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={semanticComparison}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="name" stroke="#6b7280" style={{ fontSize: '14px', fontWeight: '600' }} />
                <YAxis domain={[0, 100]} label={{ value: 'Similarity %', angle: -90, position: 'insideLeft' }} stroke="#6b7280" />
                <Tooltip 
                  formatter={(value) => `${value}%`}
                  contentStyle={{ borderRadius: '12px', border: '2px solid #e5e7eb' }}
                />
                <Bar 
                  dataKey="similarity" 
                  radius={[12, 12, 0, 0]}
                  label={{ position: 'top', formatter: (val) => `${val}%`, fontWeight: 'bold' }}
                >
                  {semanticComparison.map((entry, index) => (
                    <Bar 
                      key={`cell-${index}`} 
                      dataKey="similarity" 
                      fill={entry.name.includes('Fair') ? '#10b981' : '#f59e0b'} 
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>

            <div className="grid grid-cols-2 gap-3 mt-4">
              <div className="bg-emerald-50 border-2 border-emerald-300 rounded-xl p-3">
                <div className="text-emerald-700 text-xs font-bold mb-1">Fair Language</div>
                <div className="text-2xl font-black text-emerald-600">
                  {(semantic_analysis.similarity_to_positive * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-amber-50 border-2 border-amber-300 rounded-xl p-3">
                <div className="text-amber-700 text-xs font-bold mb-1">Toxic Language</div>
                <div className="text-2xl font-black text-amber-600">
                  {(semantic_analysis.similarity_to_toxic * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Confidence Breakdown */}
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-6 border border-white/50">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-800">
              Prediction Confidence
            </h3>
          </div>

          <div className="bg-purple-50 border-l-4 border-purple-500 rounded-lg p-4 mb-4">
            <div className="flex items-start gap-2">
              <Info className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-purple-900 font-medium">
                How certain the model is about this prediction (0-100%)
              </p>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={confidenceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#6b7280" style={{ fontSize: '14px', fontWeight: '600' }} />
              <YAxis domain={[0, 100]} stroke="#6b7280" />
              <Tooltip 
                formatter={(value) => `${value}%`}
                contentStyle={{ borderRadius: '12px', border: '2px solid #e5e7eb' }}
              />
              <Bar dataKey="value" fill="url(#colorGradient)" radius={[12, 12, 0, 0]}>
                <defs>
                  <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#8b5cf6" stopOpacity={1}/>
                    <stop offset="100%" stopColor="#ec4899" stopOpacity={1}/>
                  </linearGradient>
                </defs>
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          <div className="mt-4 space-y-2">
            <p className="font-bold text-gray-700">
              Confidence Level: <span className={`${confidenceLevelColor} text-lg`}>{confidenceLevel.toUpperCase()}</span>
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 text-emerald-700 font-medium">
                <div className="w-3 h-3 bg-emerald-500 rounded-full"></div>
                <strong>High (70-100%):</strong> Very confident
              </div>
              <div className="flex items-center gap-2 text-amber-700 font-medium">
                <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
                <strong>Medium (50-70%):</strong> Moderately confident
              </div>
              <div className="flex items-center gap-2 text-red-700 font-medium">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <strong>Low (0-50%):</strong> Uncertain
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Embedding Statistics - Full Width */}
      {embeddingRadarData.length > 0 && (
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl">
              <Hash className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-800">
              Sentence Embedding Vector Analysis (384 Dimensions)
            </h3>
          </div>

          <div className="bg-indigo-50 border-l-4 border-indigo-500 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-2">
              <Info className="w-5 h-5 text-indigo-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-indigo-900 font-medium">
                Your comment is converted into a 384-dimensional mathematical vector. These statistics describe the shape and distribution of that vector.
              </p>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={350}>
            <RadarChart data={embeddingRadarData}>
              <PolarGrid stroke="#d1d5db" />
              <PolarAngleAxis dataKey="metric" style={{ fontSize: '14px', fontWeight: '600' }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} />
              <Radar 
                name="Statistics" 
                dataKey="value" 
                stroke="#8b5cf6" 
                fill="#8b5cf6" 
                fillOpacity={0.6}
                strokeWidth={3}
              />
              <Tooltip formatter={(value) => value.toFixed(2)} />
            </RadarChart>
          </ResponsiveContainer>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-6">
            <div className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-300 rounded-xl p-4 text-center">
              <div className="text-purple-700 text-xs font-bold mb-1">Dimension</div>
              <div className="text-2xl font-black text-purple-600">{embedding_stats.dimension}</div>
            </div>
            <div className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-300 rounded-xl p-4 text-center">
              <div className="text-purple-700 text-xs font-bold mb-1">L2 Norm</div>
              <div className="text-2xl font-black text-purple-600">{embedding_stats.norm.toFixed(2)}</div>
            </div>
            <div className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-300 rounded-xl p-4 text-center">
              <div className="text-purple-700 text-xs font-bold mb-1">Mean</div>
              <div className="text-2xl font-black text-purple-600">{embedding_stats.mean.toFixed(3)}</div>
            </div>
            <div className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-300 rounded-xl p-4 text-center">
              <div className="text-purple-700 text-xs font-bold mb-1">Std Dev</div>
              <div className="text-2xl font-black text-purple-600">{embedding_stats.std.toFixed(3)}</div>
            </div>
            <div className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-300 rounded-xl p-4 text-center">
              <div className="text-purple-700 text-xs font-bold mb-1">Range</div>
              <div className="text-lg font-black text-purple-600">
                {embedding_stats.min.toFixed(2)} to {embedding_stats.max.toFixed(2)}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Model Limitations Warning */}
      <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-300 rounded-3xl shadow-2xl p-8">
        <div className="flex items-start gap-3 mb-6">
          <div className="p-2 bg-amber-500 rounded-xl">
            <Info className="w-6 h-6 text-white" />
          </div>
          <h3 className="text-xl font-bold text-amber-900">Important Model Limitations</h3>
        </div>
        
        <div className="space-y-4 text-gray-800">
          <div className="bg-white/70 rounded-xl p-4 border border-amber-200">
            <p className="font-bold text-amber-900 mb-2">📊 Model Accuracy: 80.08% on test data</p>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-emerald-50 border-2 border-emerald-300 rounded-xl p-4">
              <p className="font-bold text-emerald-900 mb-3">✓ What the model detects:</p>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-600 font-bold">•</span>
                  <span>Direct discriminatory language about social groups</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-600 font-bold">•</span>
                  <span>Toxic and hateful language patterns</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-600 font-bold">•</span>
                  <span>Stereotypes and unfair generalizations</span>
                </li>
              </ul>
            </div>

            <div className="bg-red-50 border-2 border-red-300 rounded-xl p-4">
              <p className="font-bold text-red-900 mb-3">✗ What the model may miss:</p>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-red-600 font-bold">•</span>
                  <span>Subtle or context-dependent bias</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-600 font-bold">•</span>
                  <span>Bias in non-human subjects</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-600 font-bold">•</span>
                  <span>Academic discussions about bias</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-600 font-bold">•</span>
                  <span>Sarcasm and irony</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-4">
            <p className="text-sm text-blue-900">
              <strong>Note:</strong> This model was trained on the AiFairness dataset which focuses on social fairness and toxicity. It reflects that dataset's specific definition of "bias" and may not capture all forms of unfairness.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
