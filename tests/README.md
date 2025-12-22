# Test Suite for Fairness & Bias Detection System

This directory contains all unit tests, integration tests, and validation scripts for the project.

## 🧪 Test Files

### API Testing
- **test_api.py** - Flask API endpoint validation
  - Health check endpoint
  - Analyze endpoint
  - Error handling

### Model Testing
- **test_ollama_direct.py** - Single comment Ollama testing
- **test_ollama_multiple.py** - Batch Ollama testing  
- **test_embeddings.py** - SBERT embedding generation
- **test_model_pipeline.py** - Full pipeline validation
- **test_phase3.py** - Phase III reasoning tests

### Legacy/Debug Tests
- **test_enhanced.py** - Enhanced detection testing
- **test_gpt2_override.py** - Legacy GPT-2 tests (deprecated)
- **test_specific.py** - Specific edge case tests

## 🚀 Running Tests

### Run All Tests
```powershell
# From project root
Get-ChildItem -Path tests -Filter "test_*.py" | ForEach-Object { python $_.FullName }
```

### Run Individual Tests
```powershell
# Test API
python tests/test_api.py

# Test Ollama with single comment
python tests/test_ollama_direct.py

# Test full model pipeline
python tests/test_model_pipeline.py
```

## ✅ Test Coverage

- ✅ API endpoints (health, analyze, error handling)
- ✅ Ollama reasoning (single & batch)
- ✅ Embedding generation (SBERT)
- ✅ Model predictions (baseline & reasoning)
- ✅ End-to-end pipeline

## 📝 Writing New Tests

1. Create `test_<feature>.py` in this directory
2. Import required modules from `src/`
3. Use descriptive function names
4. Include expected vs actual output validation
5. Document edge cases

### Example Test Structure
```python
"""
Test <feature> functionality
"""
import sys
sys.path.append('..')
from src.inference import BiasDetector

def test_bias_detection():
    detector = BiasDetector()
    result = detector.analyze_comment("test comment")
    
    assert result['prediction'] in ['fair', 'biased']
    assert 'confidence' in result
    print("✅ Test passed")

if __name__ == "__main__":
    test_bias_detection()
```

## 🔧 Prerequisites

- Virtual environment activated
- Models trained (`python main.py --mode all`)
- Ollama running (for Phase III tests)
- Flask API running (for API tests)

## 📊 Test Results

Check test output for:
- ✅ Pass/fail status
- Prediction values
- Confidence scores
- Response times
- Error messages (if any)
