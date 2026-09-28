"""
Test Groq reasoning directly without Flask server
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from groq_reasoner import get_groq_reasoner

comment = "That candidate possesses all the required qualifications for this engineering leadership role."

print("=" * 80)
print(f"Testing comment: {comment}")
print("=" * 80)

# Get Groq reasoner
reasoner = get_groq_reasoner()

if not reasoner.available:
    print("ERROR: Groq reasoner is not available! Check GROQ_API_KEY.")
    sys.exit(1)

print(f"\nGroq is available: {reasoner.available}")
print(f"Model: {reasoner.model_name}")

# Test bias detection
result = reasoner.detect_bias_with_groq(comment)

if result:
    print("\n" + "=" * 80)
    print("RESULT:")
    print("=" * 80)
    print(f"Groq Prediction: {result['groq_prediction']} (1=Biased, 0=Fair)")
    print(f"Confidence: {result['groq_confidence'] * 100:.1f}%")
    print(f"First word detected: '{result.get('first_word', 'N/A')}'")
    print(f"\nFull Groq Response:\n{result['groq_raw_output']}")
else:
    print("ERROR: No result from Groq!")
