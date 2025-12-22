# 📡 Offline Mode Guide

## Running Without Internet

This application runs **100% offline** - no internet connection required!

### What Runs Locally:

✓ **Flask API** - Python backend (localhost:5000)  
✓ **React Frontend** - Web UI (localhost:3000)  
✓ **Ollama LLM** - AI reasoning (localhost:11434)  
✓ **ML Models** - Scikit-learn, SBERT (cached locally)  

---

## Quick Start (Offline)

### Windows PowerShell:
```powershell
.\start_offline.ps1
```

### Python (Cross-platform):
```bash
python start_offline.py
```

### Manual Start:
```powershell
# Terminal 1 - API
.\.venv\Scripts\python.exe api\app.py

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## First-Time Setup (Requires Internet Once)

### 1. Install Dependencies
```powershell
# Python packages
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Frontend packages
cd frontend
npm install
```

### 2. Download Ollama Model
```powershell
ollama pull qwen2.5:3b
```

### 3. Download SBERT Model (Auto-cached)
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # Downloads once
```

### 4. Train Models (if needed)
```powershell
python src/baseline_model.py
python src/embedding_model.py
```

---

## After Setup - Fully Offline

Once setup is complete, **disconnect from internet** and run:

```powershell
.\start_offline.ps1
```

### Offline Checklist:
- ✓ Models trained (`models/*.pkl`)
- ✓ SBERT cached (`~/.cache/torch/sentence_transformers/`)
- ✓ Ollama model downloaded (`ollama list`)
- ✓ Frontend built (`frontend/node_modules/`)
- ✓ Python packages installed (`.venv/`)

---

## Troubleshooting Offline Mode

### Issue: "Ollama not accessible"
**Solution:** Start Ollama service first:
```powershell
ollama serve
```

### Issue: "Models not found"
**Solution:** Train models with internet once:
```powershell
python src/baseline_model.py
python src/embedding_model.py
```

### Issue: "Frontend dependencies missing"
**Solution:** Install npm packages once (requires internet):
```powershell
cd frontend
npm install
```

### Issue: "SBERT downloading model"
**Solution:** First run downloads model to cache:
```python
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Ports Used (All Local)

| Service | Port | URL |
|---------|------|-----|
| React Frontend | 3000 | http://localhost:3000 |
| Flask API | 5000 | http://localhost:5000 |
| Ollama LLM | 11434 | http://localhost:11434 |

**No external connections** - all traffic stays on localhost!

---

## File Locations (Offline Assets)

```
ProblemsInRes/
├── models/                    # Trained ML models
│   ├── baseline_rf_model.pkl
│   └── embedding_rf_model.pkl
├── .venv/                     # Python packages (offline)
├── frontend/node_modules/     # React packages (offline)
└── ~/.cache/                  # SBERT models (offline)
    └── torch/sentence_transformers/
```

---

## Performance Benefits (Offline)

✓ **Faster** - No network latency  
✓ **Private** - Data never leaves your machine  
✓ **Reliable** - No internet outages  
✓ **Secure** - No external API keys needed  

---

## Ollama Offline Verification

Check if Ollama works offline:

```powershell
# List local models
ollama list

# Test without internet
ollama run qwen2.5:3b "Is this biased?"
```

If models are listed, Ollama works offline! ✓

---

## Complete Offline Workflow

1. **One-time setup** (with internet):
   ```powershell
   pip install -r requirements.txt
   cd frontend && npm install
   ollama pull qwen2.5:3b
   python src/baseline_model.py
   ```

2. **Every subsequent use** (no internet):
   ```powershell
   .\start_offline.ps1
   ```

3. **Open browser**: http://localhost:3000

4. **Analyze comments** with three modes:
   - Baseline Model (sklearn)
   - Ollama Reasoning (Qwen2.5)
   - Compare Both

All processing happens locally! 🚀

---

## Offline API Examples

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Analyze Comment (Baseline)
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"comment": "This is a test comment"}'
```

### Analyze with Ollama
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"comment": "Test", "use_gpt2": true}'
```

---

## Why This Works Offline

1. **Python Backend**: Pure Python, no external APIs
2. **React Frontend**: Bundled JS, no CDN dependencies
3. **Ollama**: Local LLM server, no cloud inference
4. **ML Models**: Cached `.pkl` files, no downloads
5. **SBERT**: Pre-downloaded to `~/.cache/`

**Zero external dependencies at runtime!** 🎯
