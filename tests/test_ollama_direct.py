"""
Test Ollama reasoning directly without Flask server
"""
import sys
sys.path.insert(0, 'src')

from ollama_reasoner import get_ollama_reasoner

# Test comment
comment = "That man did not complete a primary goal of his position."

print("=" * 80)
print(f"Testing comment: {comment}")
print("=" * 80)

# Get Ollama reasoner
reasoner = get_ollama_reasoner()

if not reasoner.available:
    print("ERROR: Ollama is not available!")
    sys.exit(1)

print(f"\nOllama is available: {reasoner.available}")
print(f"Model: {reasoner.model_name}")

# Test bias detection
result = reasoner.detect_bias_with_ollama(comment)

if result:
    print("\n" + "=" * 80)
    print("RESULT:")
    print("=" * 80)
    print(f"Ollama Prediction: {result['ollama_prediction']} (1=Biased, 0=Fair)")
    print(f"Confidence: {result['ollama_confidence'] * 100:.1f}%")
    print(f"\nFirst word from response: '{result.get('first_word', 'N/A')}'")
    print(f"\nFull Ollama Response:\n{result['ollama_raw_output']}")
else:
    print("ERROR: No result from Ollama!")
