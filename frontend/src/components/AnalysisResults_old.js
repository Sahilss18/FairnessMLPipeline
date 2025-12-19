import React from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  Activity,
  Percent,
  Eye,
  Hash,
  Brain,
  Info
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
  Radar,
  LineChart,
  Line
} from 'recharts';
import './AnalysisResults.css';

const AnalysisResults = ({ result }) => {
  if (!result) return null;

  const { prediction, confidence, semantic_analysis, embedding_stats, comment, reasoning } = result;
  const isBiased = prediction === 'biased' || prediction === 1;

  // Prepare semantic comparison data
  const semanticComparison = semantic_analysis ? [
    { 
      name: 'Positive/Fair', 
      similarity: (semantic_analysis.similarity_to_positive * 100).toFixed(1),
      fill: '#10b981'
    },
    { 
      name: 'Toxic/Biased', 
      similarity: (semantic_analysis.similarity_to_toxic * 100).toFixed(1),
      fill: '#f59e0b'
    }
  ] : [];

  // Prepare confidence breakdown
  const confidenceData = [
    { name: 'Confidence', value: (confidence * 100).toFixed(1), fill: '#667eea' },
    { name: 'Uncertainty', value: ((1 - confidence) * 100).toFixed(1), fill: '#e2e8f0' }
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
  const confidenceLevelColor = confidenceLevel === 'high' ? '#10b981' : confidenceLevel === 'medium' ? '#f59e0b' : '#ef4444';

  return (
    <div className="results-container">
      {/* Main Prediction Card */}
      <div className={`prediction-card ${isBiased ? 'biased' : 'fair'}`}>
        <div className="prediction-header">
          {isBiased ? (
            <>
              <AlertTriangle size={48} />
              <div>
                <h2>Biased Content Detected</h2>
                <p>This comment may contain bias or unfairness</p>
              </div>
            </>
          ) : (
            <>
              <CheckCircle size={48} />
              <div>
                <h2>Fair Content</h2>
                <p>This comment appears to be fair and unbiased</p>
              </div>
            </>
          )}
        </div>

        <div className="confidence-meter">
          <div className="meter-label">
            <Percent size={18} />
            <span>Model Confidence Level: <strong style={{color: confidenceLevelColor}}>{confidenceLevel.toUpperCase()}</strong></span>
          </div>
          <div className="meter-bar">
            <div 
              className="meter-fill"
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
          <div className="meter-value">{(confidence * 100).toFixed(2)}%</div>
        </div>

        <div className="analyzed-comment">
          <h4>Analyzed Comment:</h4>
          <p>"{comment}"</p>
        </div>

        {/* AI Reasoning */}
        {reasoning && (
          <div className="ai-reasoning">
            <h4><Brain size={18} /> AI Model Reasoning</h4>
            <div className="reasoning-content">
              <p><strong>Model Type:</strong> {reasoning.model_type}</p>
              <p><strong>Key Decision Factors:</strong></p>
              <ul>
                {reasoning.key_factors.map((factor, idx) => (
                  <li key={idx}>{factor}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Visualizations Grid */}
      <div className="visualizations-grid">
        {/* Semantic Similarity Comparison */}
        {semantic_analysis && (
          <div className="viz-card">
            <h3>
              <Eye size={20} />
              Semantic Similarity Analysis
            </h3>
            <div className="explanation-box">
              <Info size={16} />
              <p>{semantic_analysis.explanation}</p>
            </div>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={semanticComparison}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} label={{ value: 'Similarity %', angle: -90, position: 'insideLeft' }} />
                <Tooltip formatter={(value) => `${value}%`} />
                <Bar 
                  dataKey="similarity" 
                  radius={[8, 8, 0, 0]}
                  label={{ position: 'top', formatter: (val) => `${val}%` }}
                >
                  {semanticComparison.map((entry, index) => (
                    <Bar key={`cell-${index}`} dataKey="similarity" fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
            <div className="similarity-explanation">
              <p>
                <strong>How it works:</strong> The model measures how similar your comment is to known "fair" vs "toxic" examples in the semantic embedding space (384 dimensions).
              </p>
              <div className="similarity-scores">
                <div className="score-item fair-score">
                  <span className="score-label">Similarity to Fair Language:</span>
                  <span className="score-value">{(semantic_analysis.similarity_to_positive * 100).toFixed(2)}%</span>
                </div>
                <div className="score-item biased-score">
                  <span className="score-label">Similarity to Toxic Language:</span>
                  <span className="score-value">{(semantic_analysis.similarity_to_toxic * 100).toFixed(2)}%</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Confidence Breakdown */}
        <div className="viz-card">
          <h3>
            <Activity size={20} />
            Prediction Confidence
          </h3>
          <div className="explanation-box">
            <Info size={16} />
            <p>How certain the model is about this prediction (0-100%)</p>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={confidenceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value) => `${value}%`} />
              <Bar dataKey="value" fill="#667eea" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="confidence-interpretation">
            <p><strong>Confidence Level: </strong>
              <span style={{color: confidenceLevelColor, fontWeight: 'bold'}}>
                {confidenceLevel.toUpperCase()}
              </span>
            </p>
            <ul>
              <li><strong>High (70-100%):</strong> Very confident in the prediction</li>
              <li><strong>Medium (50-70%):</strong> Moderately confident</li>
              <li><strong>Low (0-50%):</strong> Uncertain, treat with caution</li>
            </ul>
          </div>
        </div>

        {/* Embedding Statistics Radar */}
        {embeddingRadarData.length > 0 && (
          <div className="viz-card full-width">
            <h3>
              <Hash size={20} />
              Sentence Embedding Vector Analysis (384 Dimensions)
            </h3>
            <div className="explanation-box">
              <Info size={16} />
              <p>Your comment is converted into a 384-dimensional mathematical vector. These statistics describe the shape and distribution of that vector.</p>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={embeddingRadarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="metric" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar 
                  name="Statistics" 
                  dataKey="value" 
                  stroke="#667eea" 
                  fill="#667eea" 
                  fillOpacity={0.6} 
                />
                <Tooltip formatter={(value) => value.toFixed(2)} />
              </RadarChart>
            </ResponsiveContainer>
            <div className="embedding-stats">
              <div className="stat-item">
                <span className="stat-label">Vector Dimension:</span>
                <span className="stat-value">{embedding_stats.dimension}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">L2 Norm (magnitude):</span>
                <span className="stat-value">{embedding_stats.norm.toFixed(4)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Mean Value:</span>
                <span className="stat-value">{embedding_stats.mean.toFixed(4)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Std Deviation:</span>
                <span className="stat-value">{embedding_stats.std.toFixed(4)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Min Value:</span>
                <span className="stat-value">{embedding_stats.min.toFixed(4)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Max Value:</span>
                <span className="stat-value">{embedding_stats.max.toFixed(4)}</span>
              </div>
            </div>
            <div className="embedding-explanation">
              <p><strong>What this means:</strong></p>
              <p>Sentence-BERT converts your text into a mathematical representation that captures semantic meaning. Comments with similar meanings have similar vectors, allowing the model to detect patterns of bias even in rephrased statements.</p>
            </div>
          </div>
        )}
      </div>

      {/* Model Limitations Warning */}
      <div className="limitations-card">
        <h3><Info size={20} /> Important Model Limitations</h3>
        <div className="limitations-content">
          <p><strong>Model Accuracy:</strong> 80.08% on test data (Phase 2)</p>
          <p><strong>What the model detects:</strong></p>
          <ul>
            <li>✓ Direct discriminatory language about social groups (race, gender, nationality, etc.)</li>
            <li>✓ Toxic and hateful language patterns</li>
            <li>✓ Stereotypes and unfair generalizations about people</li>
          </ul>
          <p><strong>What the model may miss:</strong></p>
          <ul>
            <li>✗ Subtle or context-dependent bias</li>
            <li>✗ Bias in non-human subjects (pets, objects)</li>
            <li>✗ Academic discussions <em>about</em> bias (vs. exhibiting bias)</li>
            <li>✗ Sarcasm and irony</li>
          </ul>
          <p className="note"><strong>Note:</strong> This model was trained on the AiFairness dataset which focuses on social fairness and toxicity. It reflects that dataset's specific definition of "bias" and may not capture all forms of unfairness.</p>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
