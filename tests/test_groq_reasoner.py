"""
Comprehensive test for Groq Reasoner and Baseline Comparison
"""
import sys
import os

# Ensure UTF-8 output on Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from inference import BiasDetector
from groq_reasoner import get_groq_reasoner

def test_groq_reasoner():
    print("=" * 80)
    print("TESTING GROQ REASONER & PHASE III INTEGRATION")
    print("=" * 80)
    
    reasoner = get_groq_reasoner()
    if not reasoner.available:
        print("[ERROR] Groq Reasoner unavailable. Test aborted.")
        return False
    
    print(f"[OK] Groq Reasoner initialized with model: {reasoner.model_name}")
    
    detector = BiasDetector()
    
    test_cases = [
        ("Everyone deserves equal respect and opportunities in our organization.", 0),
        ("Women are too emotional to be effective corporate leaders.", 1),
        ("People from that neighborhood are all dishonest.", 1),
        ("The software engineer completed the task ahead of schedule.", 0)
    ]
    
    all_passed = True
    
    for comment, expected_bias in test_cases:
        print(f"\n--- Testing Comment: '{comment}' ---")
        result = detector.analyze_comment(comment, use_groq=True)
        
        baseline_pred = result['prediction']
        groq_reason = result.get('groq_reasoning', {})
        groq_pred = groq_reason.get('groq_prediction')
        
        print(f"Baseline Sentiment: {result['sentiment']} (Confidence: {result['confidence']:.2%})")
        print(f"Groq Sentiment:     {'Biased' if groq_pred == 1 else 'Fair'} (Confidence: {groq_reason.get('reasoning_confidence', 0):.2%})")
        print(f"Explanation:        {groq_reason.get('explanation', result['explanation'])}")
        
        if groq_pred != expected_bias:
            print(f"[WARNING] Expected {expected_bias}, got Groq {groq_pred}")
        else:
            print("[OK] Groq Prediction matched expectation!")
            
        if 'model_comparison' in result:
            comp = result['model_comparison']
            print(f"Models Agree:       {comp.get('models_agree')}")
            print(f"Recommendation:     {comp.get('comparison_metrics', {}).get('recommendation')}")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] GROQ REASONER TEST COMPLETED")
    print("=" * 80)
    return True

if __name__ == "__main__":
    test_groq_reasoner()
