"""
Flask API for Fairness and Bias Detection System
Provides REST endpoints for the React frontend
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from inference import BiasDetector
from config import EMBEDDING_MODEL_PATH, SENTENCE_TRANSFORMER_MODEL
from audit_logger import get_audit_logger
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize the detector once
print("Loading bias detection model...")
try:
    detector = BiasDetector(
        model_path=EMBEDDING_MODEL_PATH,
        embedder_name=SENTENCE_TRANSFORMER_MODEL
    )
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    detector = None

# Initialize audit logger
print("Initializing audit chain...")
try:
    audit_logger = get_audit_logger()
    print("Audit chain ready!")
except Exception as e:
    print(f"Warning: Audit logger initialization failed: {e}")
    audit_logger = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if the API is running and model is loaded"""
    audit_stats = audit_logger.get_stats() if audit_logger else {}
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector is not None,
        'audit_enabled': audit_logger is not None,
        'audit_stats': audit_stats
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_comment():
    """
    Analyze a single comment for bias and fairness
    
    Request body:
    {
        "comment": "text to analyze",
        "use_gpt2": false  // Optional: use Ollama reasoning (Phase III)
    }
    """
    if detector is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'comment' not in data:
            return jsonify({'error': 'No comment provided'}), 400
        
        comment = data['comment'].strip()
        use_gpt2 = data.get('use_gpt2', False)
        
        if not comment:
            return jsonify({'error': 'Empty comment'}), 400
        
        # Analyze the comment with optional GPT-2 reasoning
        base_result = detector.analyze_comment(comment, use_gpt2=use_gpt2)
        
        # Enhanced response format for frontend
        prediction_label = "biased" if base_result['prediction'] == 1 else "fair"
        
        response = {
            'comment': comment,
            'prediction': prediction_label,
            'confidence': float(base_result['confidence']),
            'semantic_analysis': {
                'similarity_to_positive': float(base_result['similarity_to_positive']),
                'similarity_to_toxic': float(base_result['similarity_to_toxic']),
                'explanation': base_result['explanation'],
                'avg_similarity': (float(base_result['similarity_to_positive']) + float(base_result['similarity_to_toxic'])) / 2,
                'similar_comments': [
                    {
                        'comment': 'Everyone deserves respect and kindness.',
                        'label': 'fair',
                        'similarity': float(base_result['similarity_to_positive'])
                    },
                    {
                        'comment': 'You are stupid and I hate you.',
                        'label': 'biased',
                        'similarity': float(base_result['similarity_to_toxic'])
                    }
                ]
            },
            'embedding_stats': {
                'dimension': 384,
                'mean': float(np.mean(base_result['embedding_preview'])),
                'std': float(np.std(base_result['embedding_preview'])),
                'min': float(np.min(base_result['embedding_preview'])),
                'max': float(np.max(base_result['embedding_preview'])),
                'norm': float(np.linalg.norm(base_result['embedding_preview'])),
                'preview': [float(x) for x in base_result['embedding_preview']]
            },
            'reasoning': {
                'model_type': 'Random Forest + Sentence-BERT',
                'confidence_level': 'high' if base_result['confidence'] > 0.7 else 'medium' if base_result['confidence'] > 0.5 else 'low',
                'key_factors': [
                    f"Semantic similarity to toxic reference: {base_result['similarity_to_toxic']:.2%}",
                    f"Semantic similarity to positive reference: {base_result['similarity_to_positive']:.2%}",
                    f"Model confidence: {base_result['confidence']:.2%}"
                ]
            }
        }
        
        # Add Ollama reasoning if requested (Phase III)
        if use_gpt2 and 'gpt2_reasoning' in base_result:
            ollama_data = base_result['gpt2_reasoning']
            # Convert numpy and boolean types to Python native types
            if 'ollama_prediction' in ollama_data:
                ollama_data['gpt2_prediction'] = int(ollama_data['ollama_prediction'])
                ollama_data['ollama_prediction'] = int(ollama_data['ollama_prediction'])
            if 'baseline_prediction' in ollama_data:
                ollama_data['baseline_prediction'] = int(ollama_data['baseline_prediction'])
            if 'disagreement' in ollama_data:
                ollama_data['disagreement'] = bool(ollama_data['disagreement'])
            if 'available' in ollama_data:
                ollama_data['available'] = bool(ollama_data['available'])
            response['gpt2_reasoning'] = ollama_data
            
        # Add model comparison if available
        if 'model_comparison' in base_result:
            comparison = base_result['model_comparison']
            # Convert boolean types
            if 'models_agree' in comparison:
                comparison['models_agree'] = bool(comparison['models_agree'])
            if 'comparison_metrics' in comparison:
                metrics = comparison['comparison_metrics']
                for key in metrics:
                    if isinstance(metrics[key], bool):
                        metrics[key] = bool(metrics[key])
            response['model_comparison'] = comparison
        
        # 🔐 LOG TO AUDIT CHAIN (Blockchain-style accountability)
        if audit_logger:
            try:
                model_used = 'compare' if 'model_comparison' in response else ('ollama' if use_gpt2 else 'baseline')
                audit_entry = audit_logger.log_prediction(
                    comment=comment,
                    baseline_prediction=prediction_label,
                    baseline_confidence=float(base_result['confidence']),
                    semantic_similarity_positive=float(base_result['similarity_to_positive']),
                    semantic_similarity_toxic=float(base_result['similarity_to_toxic']),
                    model_used=model_used,
                    ollama_prediction=response.get('gpt2_reasoning', {}).get('gpt2_prediction'),
                    ollama_confidence=response.get('gpt2_reasoning', {}).get('reasoning_confidence')
                )
                response['audit'] = {
                    'logged': True,
                    'audit_id': audit_entry['audit_id'],
                    'entry_hash': audit_entry['entry_hash'],
                    'timestamp': audit_entry['timestamp']
                }
                print(f"✅ Logged to audit chain: ID {audit_entry['audit_id']}, Hash: {audit_entry['entry_hash'][:16]}...")
            except Exception as e:
                print(f"⚠️ Audit logging failed: {e}")
                response['audit'] = {'logged': False, 'error': str(e)}
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in analyze_comment: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Analyze multiple comments
    
    Request body:
    {
        "comments": ["text1", "text2", ...]
    }
    
    Response:
    {
        "results": [result1, result2, ...]
    }
    """
    if detector is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'comments' not in data:
            return jsonify({'error': 'No comments provided'}), 400
        
        comments = data['comments']
        
        if not isinstance(comments, list):
            return jsonify({'error': 'Comments must be a list'}), 400
        
        results = []
        for comment in comments:
            if comment.strip():
                result = detector.analyze_comment(comment)
                # Convert numpy types
                result['prediction'] = int(result['prediction'])
                result['confidence'] = float(result['confidence'])
                result['similarity_to_positive'] = float(result['similarity_to_positive'])
                result['similarity_to_toxic'] = float(result['similarity_to_toxic'])
                result['embedding_preview'] = [float(x) for x in result['embedding_preview']]
                results.append(result)
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get model performance statistics
    """
    try:
        # Return hardcoded stats based on your training results
        stats = {
            'baseline_model': {
                'accuracy': 0.9997,  # 99.97% from your training
                'roc_auc': 1.0,
                'n_estimators': 100,
                'n_features': 42  # Baseline features
            },
            'embedding_model': {
                'accuracy': 0.8008,  # 80.08% from your training
                'roc_auc': 0.885,
                'n_estimators': 150,
                'n_features': 384  # Sentence-BERT dimensions
            },
            'dataset': {
                'total_samples': 90902,
                'train_size': 72721,
                'test_size': 18181
            }
        }
        
        return jsonify(stats)
    
    except Exception as e:
        print(f"Error in get_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """
    Get example comments for demonstration
    """
    examples = [
        {
            "comment": "I really appreciate the work of all people equally.",
            "label": "fair"
        },
        {
            "comment": "Everyone deserves respect regardless of their religion.",
            "label": "fair"
        },
        {
            "comment": "We should consider all perspectives before making decisions.",
            "label": "fair"
        },
        {
            "comment": "The research shows interesting patterns across demographics.",
            "label": "fair"
        },
        {
            "comment": "You are such an idiot, I hate people like you.",
            "label": "biased"
        },
        {
            "comment": "Muslims are always causing trouble.",
            "label": "biased"
        },
        {
            "comment": "People from that country can't be trusted.",
            "label": "biased"
        },
        {
            "comment": "Women are too emotional to be leaders.",
            "label": "biased"
        }
    ]
    
    return jsonify({'examples': examples})


@app.route('/api/audit/verify', methods=['GET'])
def verify_audit_chain():
    """
    Verify the integrity of the audit chain.
    Checks hash continuity and cryptographic signatures.
    
    Returns verification results with any errors found.
    """
    if not audit_logger:
        return jsonify({'error': 'Audit chain not available'}), 503
    
    try:
        verification = audit_logger.verify_chain()
        return jsonify({
            'verified': verification['chain_valid'],
            'total_entries': verification['total_entries'],
            'valid_entries': verification['valid_entries'],
            'errors': verification['errors'],
            'message': 'Audit chain is valid ✅' if verification['chain_valid'] 
                      else f"Found {len(verification['errors'])} integrity violations ❌"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/audit/export', methods=['GET'])
def export_audit_log():
    """
    Export recent audit entries.
    Query params:
        limit: Number of entries to export (default: 100, max: 1000)
    """
    if not audit_logger:
        return jsonify({'error': 'Audit chain not available'}), 503
    
    try:
        limit = min(int(request.args.get('limit', 100)), 1000)
        entries = audit_logger.export_audit_log(limit=limit)
        
        return jsonify({
            'entries': entries,
            'count': len(entries),
            'exported_at': datetime.utcnow().isoformat() + 'Z'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/audit/stats', methods=['GET'])
def get_audit_stats():
    """Get audit chain statistics."""
    if not audit_logger:
        return jsonify({'error': 'Audit chain not available'}), 503
    
    try:
        stats = audit_logger.get_stats()
        verification = audit_logger.verify_chain()
        
        return jsonify({
            **stats,
            'chain_verified': verification['chain_valid'],
            'last_verified_at': datetime.utcnow().isoformat() + 'Z'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("FAIRNESS DETECTION API SERVER")
    print("="*70)
    print("\nAPI Endpoints:")
    print("  GET  /api/health        - Health check")
    print("  POST /api/analyze       - Analyze single comment")
    print("  POST /api/batch-analyze - Analyze multiple comments")
    print("  GET  /api/stats         - Get model statistics")
    print("  GET  /api/examples      - Get example comments")
    print("\n🔐 Audit Chain Endpoints:")
    print("  GET  /api/audit/verify  - Verify chain integrity")
    print("  GET  /api/audit/export  - Export audit log")
    print("  GET  /api/audit/stats   - Get audit statistics")
    print("\nStarting server on http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
