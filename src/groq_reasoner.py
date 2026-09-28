"""
Groq Reasoning Module (Phase III)
Uses Groq's OpenAI-compatible API for bias detection and explanation generation.
"""

import os
import requests
from config import GROQ_API_KEY, GROQ_MODEL


class GroqReasoner:
    """Groq-based reasoning for bias detection with independent analysis."""

    def __init__(self, model_name=None, base_url="https://api.groq.com/openai/v1"):
        self.base_url = base_url
        self.api_key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
        self.model_name = model_name or os.getenv("GROQ_MODEL") or GROQ_MODEL or "qwen/qwen3.8-27b"
        self.available = False

        if not self.api_key:
            print("Warning: GROQ_API_KEY is not set.")
            return

        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
            )
            if response.status_code == 200:
                models_data = response.json().get("data", [])
                available_ids = [m.get("id") for m in models_data if isinstance(m, dict)]
                
                # If requested model is available, use it; otherwise fallback to best available
                if self.model_name in available_ids:
                    self.available = True
                else:
                    candidates = ["qwen/qwen3.8-27b", "groq/compound-mini", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
                    matched = next((c for c in candidates if c in available_ids), None)
                    if matched:
                        self.model_name = matched
                        self.available = True
                    elif available_ids:
                        self.model_name = available_ids[0]
                        self.available = True
                    else:
                        self.available = True

                print(f"Groq reasoner initialized with model: {self.model_name}")
            else:
                print(f"Warning: Groq API responded with {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Warning: Could not connect to Groq: {e}")

    def _chat(self, prompt, max_tokens=120):
        if not self.available:
            return None

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a careful fairness and bias analysis assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.1,
                    "max_tokens": max_tokens,
                },
                timeout=30,
            )

            if response.status_code != 200:
                print(f"Groq API error: {response.status_code} - {response.text}")
                return None

            payload = response.json()
            return payload["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Groq request exception: {e}")
            return None

    def detect_bias_with_groq(self, comment):
        if not self.available:
            return None

        prompt = f'''Analyze the following comment for bias, unfairness, stereotypes, or disrespect.

Comment: "{comment}"

Answer with exactly one word first: Yes or No.
Then provide a brief reason in one sentence.'''

        output = self._chat(prompt, max_tokens=90)
        if not output:
            return None

        output_clean = output.strip()
        first_word = output_clean.split()[0].lower().strip(".,:;!?") if output_clean else ""
        is_yes = first_word.startswith("yes")
        is_no = first_word.startswith("no")

        if is_yes:
            groq_predicts_bias = True
            groq_confidence = 0.85
        elif is_no:
            groq_predicts_bias = False
            groq_confidence = 0.85
        else:
            groq_predicts_bias = "bias" in output_clean.lower() or "toxic" in output_clean.lower() or "stereotype" in output_clean.lower()
            groq_confidence = 0.70

        return {
            'groq_prediction': 1 if groq_predicts_bias else 0,
            'groq_confidence': groq_confidence,
            'groq_raw_output': output,
            'first_word': first_word,
        }

    def generate_reasoning(self, comment, prediction, confidence, similarity_positive, similarity_toxic):
        if not self.available:
            return {
                'explanation': 'Groq reasoning not available',
                'model': 'Groq (unavailable)',
                'reasoning_confidence': 0.0,
                'available': False,
            }

        groq_analysis = self.detect_bias_with_groq(comment)
        if groq_analysis and groq_analysis['groq_prediction'] != prediction:
            final_prediction = groq_analysis['groq_prediction']
            final_confidence = groq_analysis['groq_confidence']
            label = 'Toxic/Biased' if final_prediction == 1 else 'Fair/Non-toxic'
            disagreement = True
        else:
            final_prediction = prediction
            final_confidence = confidence
            label = 'Toxic/Biased' if prediction == 1 else 'Fair/Non-toxic'
            disagreement = False

        prompt = f'''Explain why this comment is classified as {label}.

Comment: "{comment}"
Classification: {label}

Provide a brief 2-sentence explanation focusing on the language patterns and potential bias indicators.'''

        explanation = self._chat(prompt, max_tokens=100)
        if not explanation:
            explanation = groq_analysis['groq_raw_output'] if groq_analysis else 'Unable to generate explanation.'
        else:
            if disagreement:
                explanation = f"[Groq Override] {explanation}"

        result = {
            'explanation': explanation,
            'model': f'Groq ({self.model_name})',
            'reasoning_confidence': final_confidence,
            'groq_prediction': final_prediction,
            'baseline_prediction': prediction,
            'disagreement': disagreement,
            'available': True,
            'semantic_factors': {
                'positive_similarity': similarity_positive,
                'toxic_similarity': similarity_toxic,
                'dominant_factor': 'toxic' if similarity_toxic > similarity_positive else 'positive',
            },
        }

        if groq_analysis:
            result['groq_details'] = {
                'raw_analysis': groq_analysis['groq_raw_output'],
                'first_word_detected': groq_analysis.get('first_word', ''),
            }

        return result

    def compare_with_baseline(self, comment, baseline_explanation, groq_result, baseline_prediction):
        if not groq_result.get('available'):
            return None

        groq_pred = groq_result.get('groq_prediction', baseline_prediction)
        agreement = groq_pred == baseline_prediction

        return {
            'models_agree': agreement,
            'baseline_label': 'Biased' if baseline_prediction == 1 else 'Fair',
            'groq_label': 'Biased' if groq_pred == 1 else 'Fair',
            'disagreement_reason': None if agreement else 'Models detected different patterns',
            'baseline_model': {
                'name': 'Random Forest + SBERT',
                'type': 'ML Classifier',
                'explanation': baseline_explanation,
                'explanation_length': len(baseline_explanation.split()),
            },
            'groq_model': {
                'name': f'Groq ({self.model_name})',
                'type': 'LLM (Autoregressive)',
                'explanation': groq_result.get('explanation', ''),
                'explanation_length': len(groq_result.get('explanation', '').split()),
            },
            'comparison_metrics': {
                'baseline_focused': 'Explicit toxic patterns & semantic similarity',
                'groq_focused': 'Contextual bias, stereotypes & deep language understanding',
                'baseline_concise': len(baseline_explanation.split()) < 20,
                'groq_detailed': len(groq_result.get('explanation', '').split()) > 10,
                'recommendation': (
                    'Both models agree on classification' if agreement
                    else 'Groq detected nuance that baseline missed - consider reviewing manually'
                ),
            },
        }


_groq_reasoner = None


def get_groq_reasoner():
    global _groq_reasoner

    if _groq_reasoner is None:
        print('Loading Groq model for reasoning...')
        _groq_reasoner = GroqReasoner()
        if _groq_reasoner.available:
            print(f'Groq model ({_groq_reasoner.model_name}) loaded successfully!')
        else:
            print('Warning: Groq model not available')

    return _groq_reasoner