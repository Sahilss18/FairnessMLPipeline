"""Test the API endpoint with enhanced bias detection"""
import requests
import json

API_URL = "http://localhost:5000/api/analyze"

test_cases = [
    ("You are stupid and I hate you", "biased"),
    ("Poor people are less reliable", "biased"),
    ("Women belong in the kitchen", "biased"),
    ("Everyone deserves equal treatment", "fair"),
    ("This bitch is crazy", "biased")
]

print("\n===== API ENDPOINT TEST =====\n")

for comment, expected in test_cases:
    try:
        response = requests.post(API_URL, json={"comment": comment})
        result = response.json()
        
        prediction = result.get('prediction', 'unknown')
        confidence = result.get('confidence', 0) * 100
        rule_enhanced = result.get('rule_enhanced', False)
        bias_type = result.get('bias_type')
        
        status = "✓" if prediction == expected else "✗"
        rule_flag = " [RULE-ENHANCED]" if rule_enhanced else ""
        
        print(f'{status} "{comment}"')
        print(f'   → Prediction: {prediction} ({confidence:.1f}%){rule_flag}')
        if rule_enhanced and bias_type:
            print(f'   → Bias type: {bias_type}')
        print()
    except Exception as e:
        print(f'✗ "{comment}" - Error: {e}\n')

print("Test complete!")
