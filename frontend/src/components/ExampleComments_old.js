import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Copy, CheckCircle } from 'lucide-react';
import './ExampleComments.css';

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
      <div className="examples-loading">
        <div className="spinner-large"></div>
        <p>Loading examples...</p>
      </div>
    );
  }

  const biasedExamples = examples.filter(ex => ex.label === 'biased' || ex.label === 1);
  const fairExamples = examples.filter(ex => ex.label === 'fair' || ex.label === 0);

  return (
    <div className="examples-container">
      <div className="examples-header">
        <h2>Sample Comments</h2>
        <p>Click on any example to analyze it, or copy it to modify</p>
      </div>

      <div className="examples-grid">
        {/* Fair Examples */}
        <div className="examples-section">
          <h3 className="section-title fair-title">
            <CheckCircle size={20} />
            Fair Comments
          </h3>
          <div className="examples-list">
            {fairExamples.map((example, index) => (
              <div 
                key={`fair-${index}`}
                className="example-card fair-card"
              >
                <p className="example-text">{example.comment}</p>
                <div className="example-actions">
                  <button
                    className="action-btn analyze-btn-small"
                    onClick={() => onExampleClick(example.comment)}
                  >
                    Analyze
                  </button>
                  <button
                    className="action-btn copy-btn"
                    onClick={() => handleCopy(example.comment, `fair-${index}`)}
                  >
                    {copiedIndex === `fair-${index}` ? (
                      <>
                        <CheckCircle size={16} />
                        Copied
                      </>
                    ) : (
                      <>
                        <Copy size={16} />
                        Copy
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Biased Examples */}
        <div className="examples-section">
          <h3 className="section-title biased-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            Biased Comments
          </h3>
          <div className="examples-list">
            {biasedExamples.map((example, index) => (
              <div 
                key={`biased-${index}`}
                className="example-card biased-card"
              >
                <p className="example-text">{example.comment}</p>
                <div className="example-actions">
                  <button
                    className="action-btn analyze-btn-small"
                    onClick={() => onExampleClick(example.comment)}
                  >
                    Analyze
                  </button>
                  <button
                    className="action-btn copy-btn"
                    onClick={() => handleCopy(example.comment, `biased-${index}`)}
                  >
                    {copiedIndex === `biased-${index}` ? (
                      <>
                        <CheckCircle size={16} />
                        Copied
                      </>
                    ) : (
                      <>
                        <Copy size={16} />
                        Copy
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="examples-info">
        <h3>About These Examples</h3>
        <p>
          These sample comments are drawn from the training dataset and represent various types of content:
        </p>
        <ul>
          <li><strong>Fair Comments:</strong> Neutral, objective statements without bias or prejudice</li>
          <li><strong>Biased Comments:</strong> Statements containing stereotypes, unfair generalizations, or discriminatory language</li>
        </ul>
        <p className="info-note">
          The model analyzes semantic content, context, and linguistic patterns to determine fairness.
        </p>
      </div>
    </div>
  );
};

export default ExampleComments;
