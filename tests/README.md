# Test Suite for Fairness & Bias Detection System

This directory contains all unit tests, integration tests, and validation scripts for the project.

## 🧪 Test Files

### API Testing
- **test_api.py** - Flask API endpoint validation
  - Health check endpoint
  - Analyze endpoint (baseline & Groq reasoning)
  - Batch analyze endpoint
  - Cryptographic audit chain endpoints

### Model Testing
- **test_groq_direct.py** - Single comment Groq LLM reasoning
- **test_groq_reasoner.py** - Groq reasoner and baseline comparison suite
- **test_embeddings.py** - SBERT embedding generation
- **test_model_pipeline.py** - Full pipeline validation

### Legacy/Debug Tests
- **test_enhanced.py** - Enhanced detection testing
- **test_specific.py** - Specific edge case tests

## 🚀 Running Tests

### Run All Tests
```powershell
# From project root
Get-ChildItem -Path tests -Filter "test_*.py" | ForEach-Object { python $_.FullName }
```

### Run Individual Tests
```powershell
# Test Groq direct reasoning
python tests/test_groq_direct.py

# Test Groq reasoner and model comparison
python tests/test_groq_reasoner.py

# Test full model pipeline
python tests/test_model_pipeline.py

# Test API (requires running Flask server)
python tests/test_api.py
```

## ✅ Test Coverage

- ✅ API endpoints (health, analyze, batch, audit)
- ✅ Groq AI reasoning (single & batch)
- ✅ Embedding generation (SBERT)
- ✅ Model predictions (baseline & Groq reasoning)
- ✅ End-to-end pipeline

## 🔧 Prerequisites

- Virtual environment activated (`.venv`)
- Trained models present (`models/*.pkl`)
- Groq API configured via `.env` (`GROQ_API_KEY`)
- Flask API running (for API tests)
