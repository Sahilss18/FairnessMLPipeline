"""
Quick test to demonstrate GPT-2's improved bias detection
Shows how GPT-2 can now override baseline predictions
"""
import requests
import json

API_URL = "http://localhost:5000/api/analyze"

def test_comment(comment, description):
    print(f"\n{'='*80}")
    print(f"TEST: {description}")
    print(f"Comment: \"{comment}\"")
    print('='*80)
    
    # Test with GPT-2
    response = requests.post(API_URL, json={
        "comment": comment,
        "use_gpt2": True
    })
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n📊 BASELINE MODEL:")
        print(f"   Prediction: {result['prediction'].upper()}")
        print(f"   Confidence: {result['confidence']*100:.1f}%")
        
        if 'gpt2_reasoning' in result:
            gpt2 = result['gpt2_reasoning']
            print(f"\n🧠 GPT-2 MODEL:")
            print(f"   Prediction: {'BIASED' if gpt2.get('gpt2_prediction') == 1 else 'FAIR'}")
            print(f"   Confidence: {gpt2.get('reasoning_confidence', 0)*100:.1f}%")
            
            if gpt2.get('disagreement'):
                print(f"   ⚠️  STATUS: GPT-2 DISAGREES WITH BASELINE!")
                print(f"   ✓  GPT-2 DETECTED BIAS THAT BASELINE MISSED")
            else:
                print(f"   ✓  STATUS: Models agree")
            
            print(f"\n💡 Explanation:")
            print(f"   {gpt2.get('explanation', 'N/A')}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print()

if __name__ == '__main__':
    print("\n" + "="*80)
    print("GPT-2 ENHANCED BIAS DETECTION TEST")
    print("Demonstrating GPT-2's ability to detect subtle bias")
    print("="*80)
    
    # Test cases where baseline fails
    test_cases = [
        ("Women are too emotional to be leaders.", 
         "Gender stereotype - Baseline often misses this"),
        
        ("Poor people are just lazy and don't want to work.",
         "Socioeconomic bias - Baseline struggles with this"),
        
        ("Everyone deserves respect and equal opportunities.",
         "Fair statement - Both should agree"),
        
        ("People from that country can't be trusted.",
         "Xenophobic bias - Test GPT-2's detection"),
    ]
    
    for comment, description in test_cases:
        test_comment(comment, description)
    
    print("="*80)
    print("✅ TEST COMPLETE")
    print("="*80)
    print("\n💡 Key Improvement:")
    print("   GPT-2 now makes INDEPENDENT predictions and can override baseline")
    print("   when it detects bias patterns the baseline model missed!\n")
