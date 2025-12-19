"""
Test multiple comments with Ollama reasoning
"""
import sys
sys.path.insert(0, 'src')

from ollama_reasoner import get_ollama_reasoner

# Test comments
test_comments = [
    "That man did not complete a primary goal of his position.",
    "Women are terrible at math and science.",
    "The candidate has strong qualifications for this role.",
    "People from that country can't be trusted."
]

# Get Ollama reasoner
reasoner = get_ollama_reasoner()

if not reasoner.available:
    print("ERROR: Ollama is not available!")
    sys.exit(1)

print(f"Testing {len(test_comments)} comments with Ollama\n")

for i, comment in enumerate(test_comments, 1):
    print(f"\n{'=' * 80}")
    print(f"Test {i}: {comment[:60]}...")
    print('=' * 80)
    
    result = reasoner.detect_bias_with_ollama(comment)
    
    if result:
        prediction = "BIASED" if result['ollama_prediction'] == 1 else "FAIR"
        print(f"Result: {prediction} ({result['ollama_confidence'] * 100:.1f}% confidence)")
    else:
        print("ERROR: No result!")
