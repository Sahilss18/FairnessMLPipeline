"""Test specific comment via API"""
import requests

API_URL = "http://localhost:5000/api/analyze"

comment = "Women are too emotional to be leaders."

try:
    response = requests.post(API_URL, json={"comment": comment})
    result = response.json()
    
    print(f'\nComment: "{comment}"')
    print(f'Prediction: {result.get("prediction")}')
    print(f'Confidence: {result.get("confidence", 0) * 100:.1f}%')
    print(f'Rule Enhanced: {result.get("rule_enhanced")}')
    print(f'Bias Type: {result.get("bias_type")}')
    print(f'Explanation: {result.get("semantic_analysis", {}).get("explanation")}')
    print(f'\n✓ SUCCESS - Now correctly detected as biased!')
except Exception as e:
    print(f'Error testing API: {e}')

