"""
GPT-2 Reasoning Module for Phase III
Provides explanations for bias detection using autoregressive language model
"""
import os
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import pipeline
    import torch
    GPT2_AVAILABLE = True
except ImportError:
    GPT2_AVAILABLE = False
    print("Warning: transformers library not available. GPT-2 reasoning disabled.")


class GPT2Reasoner:
    """
    Autoregressive reasoning using GPT-2 for explainable bias detection
    """
    
    def __init__(self):
        """Initialize GPT-2 model for text generation"""
        if not GPT2_AVAILABLE:
            self.reasoner = None
            self.available = False
            return
            
        try:
            print("Loading GPT-2 model for reasoning...")
            # Use smaller max_length to reduce latency
            self.reasoner = pipeline(
                "text-generation",
                model="gpt2",
                max_new_tokens=60,
                device=-1  # CPU
            )
            self.available = True
            print("GPT-2 model loaded successfully!")
        except Exception as e:
            print(f"Error loading GPT-2: {e}")
            self.reasoner = None
            self.available = False
    
    def detect_bias_with_gpt2(self, comment):
        """
        Use GPT-2 to detect bias patterns directly (independent of baseline model)
        
        Args:
            comment: Input text to analyze
            
        Returns:
            dict: GPT-2's own bias detection result
        """
        if not self.available or self.reasoner is None:
            return None
        
        try:
            # Prompt GPT-2 to detect bias (zero-shot classification)
            prompt = (
                f"Analyze this comment for bias, discrimination, or stereotypes:\n\n"
                f"Comment: \"{comment}\"\n\n"
                f"Analysis:\n"
                f"1. Contains bias: (Yes/No)\n"
                f"2. Bias type:"
            )
            
            output = self.reasoner(
                prompt,
                max_new_tokens=80,
                do_sample=True,
                temperature=0.5,  # Lower for more deterministic
                top_p=0.9,
                num_return_sequences=1
            )[0]["generated_text"]
            
            # Extract only the generated response (after the prompt)
            response_text = output[len(prompt):].strip().lower()
            
            # DEBUG: Print what GPT-2 actually said
            print(f"\n🔍 GPT-2 DEBUG for: '{comment[:50]}...'")
            print(f"   Raw response: {response_text[:200]}")
            
            # Look for explicit "Yes" or "No" answer in the first line
            first_line = response_text.split('\n')[0] if response_text else ''
            print(f"   First line: '{first_line}'")
            
            # Check if GPT-2 explicitly said "Yes" for bias
            contains_yes = 'yes' in first_line and 'no' not in first_line[:10]
            print(f"   Contains 'yes': {contains_yes}")
            
            # Also check for bias indicators in the response
            bias_indicators = [
                'discriminat', 'stereotype', 'prejudice',
                'sexist', 'racist', 'unfair', 'offensive', 'toxic'
            ]
            
            # Count bias indicators in GPT-2's response (excluding the word 'bias' itself)
            bias_score = sum(1 for indicator in bias_indicators if indicator in response_text)
            print(f"   Bias indicators found: {bias_score}")
            
            # GPT-2's independent prediction - use explicit answer or high bias score
            gpt2_predicts_bias = contains_yes or bias_score >= 3
            print(f"   Final prediction: {'BIASED' if gpt2_predicts_bias else 'FAIR'}\n")
            
            # Calculate confidence based on explicit answer or bias indicators
            if contains_yes:
                gpt2_confidence = min(0.65 + (bias_score * 0.1), 0.90)
            else:
                gpt2_confidence = min(0.50 + (bias_score * 0.12), 0.85)
            
            return {
                'gpt2_prediction': 1 if gpt2_predicts_bias else 0,
                'gpt2_confidence': gpt2_confidence,
                'gpt2_raw_output': output,
                'bias_indicators_found': bias_score
            }
            
        except Exception as e:
            print(f"Error in GPT-2 bias detection: {e}")
            return None
    
    def generate_reasoning(self, comment, prediction, confidence, 
                          similarity_positive, similarity_toxic):
        """
        Generate explanation for bias detection decision WITH GPT-2's own analysis
        
        Args:
            comment: Input text
            prediction: Baseline model prediction (0=fair, 1=biased)
            confidence: Baseline prediction confidence (0-1)
            similarity_positive: Cosine similarity to positive reference
            similarity_toxic: Cosine similarity to toxic reference
            
        Returns:
            dict: Generated explanation and metadata with GPT-2's independent analysis
        """
        if not self.available or self.reasoner is None:
            return {
                'explanation': 'GPT-2 reasoning not available',
                'model': 'GPT-2 (unavailable)',
                'reasoning_confidence': 0.0,
                'available': False
            }
        
        try:
            # First, get GPT-2's own independent bias detection
            gpt2_analysis = self.detect_bias_with_gpt2(comment)
            
            # Determine which prediction to use
            if gpt2_analysis and gpt2_analysis['gpt2_prediction'] != prediction:
                # GPT-2 disagrees with baseline - use GPT-2's prediction
                final_prediction = gpt2_analysis['gpt2_prediction']
                final_confidence = gpt2_analysis['gpt2_confidence']
                label = 'Toxic/Biased' if final_prediction == 1 else 'Fair/Non-toxic'
                disagreement = True
            else:
                # GPT-2 agrees or unavailable - use baseline
                final_prediction = prediction
                final_confidence = confidence
                label = 'Toxic/Biased' if prediction == 1 else 'Fair/Non-toxic'
                disagreement = False
            
            # Generate detailed explanation
            prompt = (
                f"Analyze this comment for bias and discrimination:\n\n"
                f"Comment: \"{comment}\"\n\n"
                f"The comment is classified as {label}.\n\n"
                f"Explanation: This comment"
            )
            
            # Generate reasoning
            output = self.reasoner(
                prompt,
                max_new_tokens=70,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1
            )[0]["generated_text"]
            
            # Extract explanation
            explanation_start = "Explanation: "
            if explanation_start in output:
                explanation = output.split(explanation_start)[1].strip()
                sentences = explanation.split('.')
                explanation = '. '.join(sentences[:2]).strip() + '.'
                
                # Add disagreement notice if applicable
                if disagreement:
                    explanation = f"[GPT-2 Override] {explanation}"
            else:
                explanation = "Unable to generate explanation."
            
            result = {
                'explanation': explanation,
                'model': 'GPT-2',
                'reasoning_confidence': final_confidence,
                'gpt2_prediction': final_prediction,
                'baseline_prediction': prediction,
                'disagreement': disagreement,
                'available': True,
                'semantic_factors': {
                    'positive_similarity': similarity_positive,
                    'toxic_similarity': similarity_toxic,
                    'dominant_factor': 'toxic' if similarity_toxic > similarity_positive else 'positive'
                }
            }
            
            # Add GPT-2 analysis details if available
            if gpt2_analysis:
                result['gpt2_analysis'] = gpt2_analysis
            
            return result
            
        except Exception as e:
            print(f"Error generating reasoning: {e}")
            return {
                'explanation': f'Error generating explanation: {str(e)}',
                'model': 'GPT-2 (error)',
                'reasoning_confidence': 0.0,
                'available': False
            }
    
    def compare_with_baseline(self, comment, base_explanation, 
                             gpt2_explanation, prediction):
        """
        Compare baseline explanation vs GPT-2 reasoning
        
        Returns:
            dict: Comparison metrics and insights
        """
        comparison = {
            'baseline_model': {
                'name': 'Random Forest + Sentence-BERT',
                'explanation': base_explanation,
                'explanation_length': len(base_explanation.split()),
                'type': 'Rule-based semantic analysis'
            },
            'gpt2_model': {
                'name': 'GPT-2 Autoregressive',
                'explanation': gpt2_explanation.get('explanation', 'N/A'),
                'explanation_length': len(gpt2_explanation.get('explanation', '').split()),
                'type': 'Generated natural language'
            },
            'comparison_metrics': {
                'baseline_concise': len(base_explanation.split()) < 15,
                'gpt2_detailed': len(gpt2_explanation.get('explanation', '').split()) > 15,
                'both_agree': True,  # Both use same underlying prediction
                'recommendation': self._get_recommendation(base_explanation, gpt2_explanation)
            }
        }
        
        return comparison
    
    def _get_recommendation(self, base_exp, gpt2_exp):
        """Determine which explanation is better"""
        gpt2_text = gpt2_exp.get('explanation', '')
        
        if not gpt2_exp.get('available', False):
            return 'Use baseline model (GPT-2 unavailable)'
        
        # GPT-2 provides more detailed, human-like explanations
        if len(gpt2_text.split()) > 20:
            return 'GPT-2 provides more detailed explanation'
        elif len(base_exp.split()) < 10:
            return 'Baseline is more concise'
        else:
            return 'Both models provide useful insights'


# Global instance
_gpt2_reasoner = None

def get_gpt2_reasoner():
    """Get or create global GPT2Reasoner instance"""
    global _gpt2_reasoner
    if _gpt2_reasoner is None:
        _gpt2_reasoner = GPT2Reasoner()
    return _gpt2_reasoner
