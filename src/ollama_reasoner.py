"""
Ollama Reasoning Module (Phase III)
Uses Ollama (Qwen2.5:3b) for bias detection and explanation generation
"""
import requests
import json


class OllamaReasoner:
    """
    Ollama-based reasoning for bias detection with independent analysis
    """
    
    def __init__(self, model_name="qwen2.5:3b", base_url="http://localhost:11434"):
        """
        Initialize Ollama reasoner
        
        Args:
            model_name: Ollama model to use
            base_url: Ollama API base URL
        """
        self.model_name = model_name
        self.base_url = base_url
        self.available = False
        
        try:
            # Check if Ollama is available
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_exists = any(m['name'] == model_name for m in models)
                
                if model_exists:
                    self.available = True
                    print(f"Ollama reasoner initialized with {model_name}")
                else:
                    print(f"Warning: Model {model_name} not found in Ollama")
            else:
                print("Warning: Ollama API not responding")
                
        except Exception as e:
            print(f"Warning: Could not connect to Ollama: {e}")
            self.available = False
    
    def generate_completion(self, prompt, max_tokens=150):
        """
        Generate text completion using Ollama
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            str: Generated text
        """
        if not self.available:
            return None
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.5,
                        "top_p": 0.9
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                print(f"Ollama API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error generating completion: {e}")
            return None
    
    def detect_bias_with_ollama(self, comment):
        """
        Use Ollama to independently detect bias in comment
        
        Args:
            comment: Input text to analyze
            
        Returns:
            dict: Ollama's bias detection result
        """
        if not self.available:
            return None
        
        try:
            # Let Ollama use its natural language understanding for bias detection
            prompt = f"""Analyze the following comment for bias, unfairness, or disrespect.

Consider:
- Does it contain stereotypes, prejudice, or discrimination?
- Is there disrespectful, insulting, or demeaning language toward any person or group?
- Does it show contempt, mockery, or lack of respect?
- Are there value judgments, personal attacks, or emotionally charged characterizations?

Comment: "{comment}"

Based on your understanding of language and fairness, is this comment biased or disrespectful?

Answer only "Yes" or "No" as the first word:"""
            
            output = self.generate_completion(prompt, max_tokens=150)
            
            if not output:
                return None
            
            # DEBUG: Print Ollama's response
            print(f"\n🔍 Ollama DEBUG for: '{comment[:80]}...'")
            print(f"   Raw response: {output[:300]}")
            
            # Analyze response - get first word
            output_clean = output.strip()
            first_word = output_clean.split()[0].lower() if output_clean else ''
            first_line = output_clean.split('\n')[0].lower() if output_clean else ''
            
            print(f"   First word: '{first_word}'")
            print(f"   First line: '{first_line[:100]}'")
            
            # Check for explicit Yes/No in first word or very beginning
            is_yes = first_word.startswith('yes')
            is_no = first_word.startswith('no')
            
            print(f"   Is Yes: {is_yes}, Is No: {is_no}")
            
            # Use Ollama's direct answer
            if is_yes:
                ollama_predicts_bias = True
                ollama_confidence = 0.75
            elif is_no:
                ollama_predicts_bias = False
                ollama_confidence = 0.75
            else:
                # If unclear, check for bias keywords in response
                bias_keywords = ['biased', 'discriminatory', 'stereotype', 'prejudice', 'unfair treatment']
                fair_keywords = ['not biased', 'fair', 'neutral', 'objective', 'factual']
                
                bias_count = sum(1 for kw in bias_keywords if kw in first_line)
                fair_count = sum(1 for kw in fair_keywords if kw in first_line)
                
                print(f"   Bias keywords: {bias_count}, Fair keywords: {fair_count}")
                
                if bias_count > fair_count:
                    ollama_predicts_bias = True
                    ollama_confidence = 0.60
                else:
                    ollama_predicts_bias = False
                    ollama_confidence = 0.60
            
            print(f"   Final prediction: {'BIASED' if ollama_predicts_bias else 'FAIR'} (confidence: {ollama_confidence:.2f})\n")
            
            return {
                'ollama_prediction': 1 if ollama_predicts_bias else 0,
                'ollama_confidence': ollama_confidence,
                'ollama_raw_output': output,
                'first_word': first_word
            }
            
        except Exception as e:
            print(f"Error in Ollama bias detection: {e}")
            return None
    
    def generate_reasoning(self, comment, prediction, confidence, 
                          similarity_positive, similarity_toxic):
        """
        Generate explanation for bias detection with Ollama's own analysis
        
        Args:
            comment: Input text
            prediction: Baseline model prediction (0=fair, 1=biased)
            confidence: Baseline prediction confidence (0-1)
            similarity_positive: Cosine similarity to positive reference
            similarity_toxic: Cosine similarity to toxic reference
            
        Returns:
            dict: Generated explanation and metadata with Ollama's analysis
        """
        if not self.available:
            return {
                'explanation': 'Ollama reasoning not available',
                'model': 'Ollama (unavailable)',
                'reasoning_confidence': 0.0,
                'available': False
            }
        
        try:
            # Get Ollama's independent bias detection
            ollama_analysis = self.detect_bias_with_ollama(comment)
            
            # Determine which prediction to use
            if ollama_analysis and ollama_analysis['ollama_prediction'] != prediction:
                # Ollama disagrees with baseline
                final_prediction = ollama_analysis['ollama_prediction']
                final_confidence = ollama_analysis['ollama_confidence']
                label = 'Toxic/Biased' if final_prediction == 1 else 'Fair/Non-toxic'
                disagreement = True
            else:
                # Ollama agrees or unavailable
                final_prediction = prediction
                final_confidence = confidence
                label = 'Toxic/Biased' if prediction == 1 else 'Fair/Non-toxic'
                disagreement = False
            
            # Generate detailed explanation
            prompt = f"""Explain why this comment is classified as {label}.

Comment: "{comment}"
Classification: {label}

Provide a brief 2-sentence explanation focusing on the language patterns and potential bias indicators.

Explanation:"""
            
            explanation = self.generate_completion(prompt, max_tokens=80)
            
            if not explanation:
                explanation = "Unable to generate explanation."
            else:
                # Clean up explanation
                sentences = explanation.split('.')
                explanation = '. '.join(sentences[:2]).strip()
                if not explanation.endswith('.'):
                    explanation += '.'
                
                # Add disagreement notice
                if disagreement:
                    explanation = f"[Ollama Override] {explanation}"
            
            result = {
                'explanation': explanation,
                'model': 'Ollama (Qwen2.5:3b)',
                'reasoning_confidence': final_confidence,
                'ollama_prediction': final_prediction,
                'baseline_prediction': prediction,
                'disagreement': disagreement,
                'available': True,
                'semantic_factors': {
                    'positive_similarity': similarity_positive,
                    'toxic_similarity': similarity_toxic,
                    'dominant_factor': 'toxic' if similarity_toxic > similarity_positive else 'positive'
                }
            }
            
            # Add Ollama analysis details
            if ollama_analysis:
                result['ollama_details'] = {
                    'raw_analysis': ollama_analysis['ollama_raw_output'],
                    'first_word_detected': ollama_analysis.get('first_word', '')
                }
            
            return result
            
        except Exception as e:
            print(f"Error generating Ollama reasoning: {e}")
            return {
                'explanation': f'Error: {str(e)}',
                'model': 'Ollama (error)',
                'reasoning_confidence': 0.0,
                'available': False
            }
    
    def compare_with_baseline(self, comment, baseline_explanation, 
                            ollama_result, baseline_prediction):
        """
        Compare Ollama reasoning with baseline model
        
        Returns:
            dict: Comparison metrics
        """
        if not ollama_result.get('available'):
            return None
        
        ollama_pred = ollama_result.get('ollama_prediction', baseline_prediction)
        agreement = (ollama_pred == baseline_prediction)
        
        return {
            'models_agree': agreement,
            'baseline_label': 'Biased' if baseline_prediction == 1 else 'Fair',
            'ollama_label': 'Biased' if ollama_pred == 1 else 'Fair',
            'disagreement_reason': None if agreement else 'Models detected different patterns',
            'baseline_model': {
                'name': 'Random Forest',
                'type': 'ML Classifier',
                'explanation': baseline_explanation,
                'explanation_length': len(baseline_explanation.split())
            },
            'gpt2_model': {
                'name': 'Ollama (Qwen2.5:3b)',
                'type': 'LLM',
                'explanation': ollama_result.get('explanation', ''),
                'explanation_length': len(ollama_result.get('explanation', '').split())
            },
            'comparison_metrics': {
                'baseline_focused': 'Explicit toxic patterns',
                'ollama_focused': 'Contextual bias and stereotypes',
                'baseline_concise': len(baseline_explanation.split()) < 20,
                'gpt2_detailed': len(ollama_result.get('explanation', '').split()) > 20,
                'recommendation': (
                    'Both models agree on classification' if agreement 
                    else 'Ollama detected patterns that baseline missed - consider reviewing manually'
                )
            }
        }


# Global reasoner instance
_ollama_reasoner = None


def get_ollama_reasoner():
    """
    Get or create global Ollama reasoner instance
    
    Returns:
        OllamaReasoner: Global reasoner
    """
    global _ollama_reasoner
    
    if _ollama_reasoner is None:
        print("Loading Ollama model for reasoning...")
        _ollama_reasoner = OllamaReasoner()
        
        if _ollama_reasoner.available:
            print("Ollama model loaded successfully!")
        else:
            print("Warning: Ollama model not available")
    
    return _ollama_reasoner
