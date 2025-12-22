# Fairness & Bias Detection System - AI Agent Guide

## Project Overview
Multi-phase ML system for detecting bias/toxicity in text using Random Forest + Sentence-BERT embeddings, with optional GPT-2/Ollama reasoning models. Includes Flask API backend and React frontend for interactive analysis.

## Architecture

### Three-Tier Structure
- **Backend**: Flask API (`api/app.py`) serving 5 REST endpoints
- **ML Core**: Phase 1 (baseline RF on numeric features) → Phase 2 (RF on SBERT embeddings) → Phase 3 (GPT-2/Ollama reasoning)
- **Frontend**: React SPA with Recharts visualization, 3 tabs (Analyze/Examples/Statistics)

### Critical Data Flow
1. Comment text → Sentence-BERT (all-MiniLM-L6-v2) → 384-dim embedding
2. Embedding → Random Forest (150 estimators) → Binary prediction (0=Fair, 1=Biased)
3. Optional: Comment → GPT-2/Ollama → Natural language explanation
4. Compare semantic similarity to reference texts (`POSITIVE_REFERENCE`, `TOXIC_REFERENCE` in `src/config.py`)

### Key Files
- **`main.py`**: CLI entrypoint with modes: `all|baseline|embedding|inference|demo`
- **`src/inference.py`**: `BiasDetector` class - main analysis interface with `analyze_comment(text, use_gpt2=False)`
- **`src/config.py`**: All paths, hyperparameters, reference texts, toxicity threshold (0.6)
- **`api/app.py`**: Flask server exposing BiasDetector via REST
- **`frontend/src/App.js`**: React UI with model selection (Baseline/GPT-2/Compare)

## Critical Workflows

### Development Setup (Windows PowerShell)
```powershell
# Virtual environment in .venv (not venv)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Train models (required before running API)
python main.py --mode all  # Generates models/*.pkl, embeddings/*.npy
```

### Running Web UI
```powershell
.\start_web_ui.ps1  # Auto-trains if models missing, starts Flask + React
```
- Flask: `http://localhost:5000`
- React: `http://localhost:3000`

### Testing
- **Direct inference**: `python main.py --mode inference` (interactive CLI)
- **API testing**: `python test_api.py` (requires Flask running)
- **Phase 3**: `python test_phase3.py` (GPT-2), `python test_ollama_direct.py` (Ollama)

## Project-Specific Conventions

### Model Path Management
- **Dataset**: Must be at `AiFairness.csv/fairness_dataset.csv` (not `data/`)
- **Models**: Saved to `models/baseline_rf_model.pkl` and `models/embedding_rf_model.pkl`
- **Embeddings**: Cached in `embeddings/train_embeddings.npy` and `embeddings/test_embeddings.npy`
- Always check `src/config.py` for canonical paths

### Toxicity Threshold
- Binary classification uses `TOXICITY_THRESHOLD = 0.6` (in `src/config.py`)
- Dataset has continuous labels (0.0-1.0), threshold converts to binary (0/1)
- **Important**: Threshold was raised from 0.5 to 0.6 to reduce false negatives (commented in config.py)

### Phase 3 Model Selection
- Frontend sends `{"comment": "...", "use_gpt2": true/false}` to `/api/analyze`
- **GPT-2**: Local transformers pipeline, ~2-3s latency, always available after `pip install transformers`
- **Ollama**: External service at `http://localhost:11434`, model=`qwen2.5:3b`, requires separate installation
- Both are optional enhancements to baseline SBERT+RF model

### Semantic Analysis Pattern
All models compute:
- `similarity_to_positive`: Cosine similarity to "Everyone deserves respect and kindness."
- `similarity_to_toxic`: Cosine similarity to "You are stupid and I hate you."
- Explanation logic: If `sim_positive > sim_toxic` → likely fair; else → likely biased

### Final Phase III (Audit Chain)
- Separate implementation in `final phase III/final phase III/`
- Uses SQLite audit chain with cryptographic signatures (`src/signer.py`)
- Hash-chained entries (each entry includes `prev_hash`)
- Explainer model trained on `train_with_explanations.csv`
- **Not integrated with main web UI** - standalone audit system

## Integration Points

### API Contract
```javascript
// Request
POST /api/analyze
{ "comment": "text", "use_gpt2": false }

// Response
{
  "prediction": "fair" | "biased",
  "confidence": 0.85,
  "semantic_analysis": {
    "similarity_to_positive": 0.72,
    "similarity_to_toxic": 0.23,
    "explanation": "..."
  },
  "gpt2_reasoning": { ... },  // Only if use_gpt2=true
  "model_comparison": { ... }  // Only if use_gpt2=true
}
```

### Frontend-Backend Communication
- React uses `axios` with `API_BASE_URL` from env var or defaults to `http://localhost:5000`
- CORS enabled in Flask - no auth required
- State management: `useState` for model selection (`useOllama`, `modelComparison`)

### External Dependencies
- **Sentence-BERT**: Downloads ~80MB model on first run (cached in `~/.cache/torch`)
- **GPT-2**: Downloads ~500MB on first transformers import
- **Ollama**: Optional, must be installed separately and running

## Common Pitfalls

1. **Dataset location**: Code expects `AiFairness.csv/fairness_dataset.csv`, not `data/fairness_dataset.csv`
2. **Virtual env naming**: Use `.venv` not `venv` (per `start_web_ui.ps1`)
3. **Model training required**: Web UI won't start without trained models - run `python main.py --mode all` first
4. **Embedding regeneration**: Deleting `embeddings/*.npy` forces recalculation (slow, ~5-10 min on full dataset)
5. **Phase 3 confusion**: `src/gpt2_reasoner.py` + `src/ollama_reasoner.py` are main implementation; `final phase III/` is separate audit prototype

## Testing Patterns
- Use `test_*.py` scripts in root for component testing
- `generate_comprehensive_report.py`: Generates performance analysis with Ollama results
- Frontend has `App_backup.js`, `App_old.js` - main is `App.js`

## Documentation Files
- **User guides**: `README.md`, `GETTING_STARTED.md`, `SETUP.md`
- **Technical**: `PROJECT_STRUCTURE.md`, `EXPLANATION.md`, `PHASE3_IMPLEMENTATION.md`
- **Summaries**: `PHASE3_SUMMARY.md`, `WEB_UI_SUMMARY.md`, `CONVERSION_SUMMARY.md`
- **Troubleshooting**: `MODEL_LIMITATIONS.md`, `OFFLINE_MODE.md`, `ENHANCED_DETECTION_FIX.md`

## Hugging Face Token
- Hardcoded in `src/config.py`: `HF_TOKEN = "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"`
- Used for downloading models that require authentication
