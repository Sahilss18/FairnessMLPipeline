"""
Inference Module
Provides real-time analysis of user-provided comments for bias and fairness.
"""
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util

from config import (
    SENTENCE_TRANSFORMER_MODEL,
    EMBEDDING_MODEL_PATH,
    POSITIVE_REFERENCE,
    TOXIC_REFERENCE
)
from utils import load_model


class BiasDetector:
    """
    A class for detecting bias in text using trained embedding model.
    """
    
    def __init__(self, model_path=EMBEDDING_MODEL_PATH, 
                 embedder_name=SENTENCE_TRANSFORMER_MODEL):
        """
        Initialize the bias detector.
        
        Args:
            model_path: Path to trained classifier
            embedder_name: Name of sentence transformer model
        """
        print("Initializing Bias Detector...")
        self.model = load_model(model_path)
        self.embedder = SentenceTransformer(embedder_name)
        
        # Pre-compute reference embeddings
        self.positive_ref = self.embedder.encode([POSITIVE_REFERENCE])
        self.toxic_ref = self.embedder.encode([TOXIC_REFERENCE])
        
        print("Bias Detector ready.\n")
    
    def analyze_comment(self, comment, use_gpt2=False):
        """
        Analyze a single comment for bias and fairness.
        
        Args:
            comment: Text string to analyze
            use_gpt2: Whether to use Ollama for reasoning (Phase III)
            
        Returns:
            dict: Analysis results
        """
        # Generate embedding
        embedding = self.embedder.encode([comment])
        
        # Get model prediction
        prediction = self.model.predict(embedding)[0]
        probability = self.model.predict_proba(embedding)[0][1]
        
        # Calculate semantic similarities
        cos_positive = util.cos_sim(embedding, self.positive_ref).item()
        cos_toxic = util.cos_sim(embedding, self.toxic_ref).item()
        
        # Determine sentiment
        sentiment = "Toxic / Biased" if prediction == 1 else "Fair / Non-Toxic"
        
        # Generate explanation based purely on semantic analysis
        if cos_toxic > cos_positive:
            base_explanation = "Meaning is closer to toxic language in semantic space."
        else:
            base_explanation = "Meaning is closer to positive or fair expressions."
        
        result = {
            'comment': comment,
            'prediction': prediction,
            'sentiment': sentiment,
            'confidence': probability,
            'embedding_preview': np.round(embedding[0][:10], 4).tolist(),
            'similarity_to_positive': cos_positive,
            'similarity_to_toxic': cos_toxic,
            'explanation': base_explanation
        }
        
        # Add Ollama reasoning if requested (Phase III)
        if use_gpt2:
            try:
                from ollama_reasoner import get_ollama_reasoner
                reasoner = get_ollama_reasoner()
                
                ollama_result = reasoner.generate_reasoning(
                    comment, prediction, probability,
                    cos_positive, cos_toxic
                )
                
                result['gpt2_reasoning'] = ollama_result
                
                # Add comparison between models
                comparison = reasoner.compare_with_baseline(
                    comment, base_explanation,
                    ollama_result, prediction
                )
                result['model_comparison'] = comparison
                
            except Exception as e:
                result['gpt2_reasoning'] = {
                    'explanation': f'Ollama reasoning unavailable: {str(e)}',
                    'model': 'Ollama (error)',
                    'available': False
                }
        
        return result

    
    def print_analysis(self, result):
        """
        Pretty print analysis result.
        
        Args:
            result: Dictionary from analyze_comment
        """
        print("="*80)
        print(f"Comment: {result['comment']}")
        print(f"\nPrediction: {result['sentiment']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"\nEmbedding Preview (first 10 dimensions):")
        print(result['embedding_preview'])
        print(f"\nSemantic Similarity:")
        print(f"  To Positive Reference: {result['similarity_to_positive']:.4f}")
        print(f"  To Toxic Reference:    {result['similarity_to_toxic']:.4f}")
        print(f"\nExplanation: {result['explanation']}")
        print("="*80)
    
    def analyze_batch(self, comments):
        """
        Analyze multiple comments.
        
        Args:
            comments: List of text strings
            
        Returns:
            list: List of analysis results
        """
        results = []
        for comment in comments:
            result = self.analyze_comment(comment)
            results.append(result)
            self.print_analysis(result)
        
        return results


def interactive_mode():
    """
    Run interactive bias detection where user can input comments.
    """
    print("\n" + "="*80)
    print("INTERACTIVE BIAS DETECTION")
    print("="*80)
    print("Enter comments to analyze for bias and fairness.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    detector = BiasDetector()
    
    while True:
        user_input = input("Enter comment: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Exiting interactive mode.")
            break
        
        if not user_input:
            print("Please enter a valid comment.\n")
            continue
        
        result = detector.analyze_comment(user_input)
        detector.print_analysis(result)


def demo_analysis():
    """
    Run demonstration analysis on predefined sample comments.
    """
    print("\n" + "="*80)
    print("DEMONSTRATION: ANALYZING SAMPLE COMMENTS")
    print("="*80)
    
    sample_comments = [
        "I really appreciate the work of all people equally.",
        "You are such an idiot, I hate people like you.",
        "Muslims are always causing trouble.",
        "Everyone deserves respect regardless of their religion.",
        "What a stupid post. You should just shut up."
    ]
    
    detector = BiasDetector()
    results = detector.analyze_batch(sample_comments)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    toxic_count = sum(1 for r in results if r['prediction'] == 1)
    fair_count = len(results) - toxic_count
    print(f"Total comments analyzed: {len(results)}")
    print(f"Classified as Fair: {fair_count}")
    print(f"Classified as Toxic: {toxic_count}")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Run demonstration
    demo_analysis()
    
    # Optionally start interactive mode
    # Uncomment the line below to enable interactive analysis
    # interactive_mode()
