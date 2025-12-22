"""Test enhanced bias detection with rule-based patterns"""
import sys
sys.path.insert(0, 'src')
from inference import BiasDetector

detector = BiasDetector()

test_comments = [
    'You are stupid and I hate you',
    'Poor people are less reliable',
    'Women belong in the kitchen',
    'Everyone deserves equal treatment',
    'This bitch is crazy'
]

print('\n===== ENHANCED BIAS DETECTION TEST =====\n')
for comment in test_comments:
    result = detector.analyze_comment(comment)
    
    # Determine expected result
    is_biased_comment = any(word in comment.lower() for word in ['stupid', 'hate', 'poor', 'women belong', 'bitch'])
    expected_biased = is_biased_comment and 'equal' not in comment.lower()
    actual_biased = result['prediction'] == 1
    status = '✓' if expected_biased == actual_biased else '✗'
    
    rule_flag = ' [RULE-ENHANCED]' if result['rule_enhanced'] else ''
    print(f'{status} "{comment}"')
    print(f'   → {result["sentiment"]} ({result["confidence"]:.1%}){rule_flag}')
    if result['rule_enhanced']:
        print(f'   → Bias type: {result["bias_type"]}')
        print(f'   → Original confidence: {result["original_confidence"]:.1%}')
    print()
