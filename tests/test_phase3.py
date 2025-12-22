"""
Test script for Phase III GPT-2 Integration
Tests baseline model, GPT-2 reasoning, and model comparison
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from inference import BiasDetector

def test_phase3():
    """Test all three modes: baseline, GPT-2, and comparison"""
    
    print("="*80)
    print("PHASE III: GPT-2 AUTOREGRESSIVE REASONING TEST")
    print("="*80)
    
    # Test comments
    test_comments = [
        "Women are too emotional to be leaders.",
        "Everyone deserves respect and equal opportunities.",
        "Poor people are just lazy and don't want to work."
    ]
    
    detector = BiasDetector()
    
    for i, comment in enumerate(test_comments, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {comment}")
        print('='*80)
        
        # Baseline mode
        print("\n🔹 MODE 1: BASELINE MODEL (Random Forest + SBERT)")
        print("-" * 80)
        result_baseline = detector.analyze_comment(comment, use_gpt2=False)
        print(f"Prediction: {result_baseline['sentiment']}")
        print(f"Confidence: {result_baseline['confidence']:.2%}")
        print(f"Explanation: {result_baseline['explanation']}")
        
        # GPT-2 mode
        print("\n🔹 MODE 2: GPT-2 REASONING (Autoregressive)")
        print("-" * 80)
        result_gpt2 = detector.analyze_comment(comment, use_gpt2=True)
        
        if 'gpt2_reasoning' in result_gpt2 and result_gpt2['gpt2_reasoning'].get('available'):
            gpt2_reason = result_gpt2['gpt2_reasoning']
            print(f"Model: {gpt2_reason['model']}")
            print(f"Explanation: {gpt2_reason['explanation']}")
            print(f"Dominant Factor: {gpt2_reason['semantic_factors']['dominant_factor']}")
        else:
            print("⚠️ GPT-2 reasoning not available")
            if 'gpt2_reasoning' in result_gpt2:
                print(f"Reason: {result_gpt2['gpt2_reasoning'].get('explanation', 'Unknown')}")
        
        # Model comparison
        if 'model_comparison' in result_gpt2:
            print("\n🔹 MODE 3: MODEL COMPARISON")
            print("-" * 80)
            comparison = result_gpt2['model_comparison']
            
            print(f"\nBaseline ({comparison['baseline_model']['name']}):")
            print(f"  - Type: {comparison['baseline_model']['type']}")
            print(f"  - Length: {comparison['baseline_model']['explanation_length']} words")
            print(f"  - Explanation: {comparison['baseline_model']['explanation']}")
            
            print(f"\nGPT-2 ({comparison['gpt2_model']['name']}):")
            print(f"  - Type: {comparison['gpt2_model']['type']}")
            print(f"  - Length: {comparison['gpt2_model']['explanation_length']} words")
            print(f"  - Explanation: {comparison['gpt2_model']['explanation']}")
            
            print(f"\n💡 Recommendation: {comparison['comparison_metrics']['recommendation']}")
    
    print("\n" + "="*80)
    print("✅ PHASE III TEST COMPLETE")
    print("="*80)


if __name__ == '__main__':
    try:
        test_phase3()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
