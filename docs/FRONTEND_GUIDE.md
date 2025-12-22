# Fairness & Bias Detection System - Web UI

## Quick Start

### 1. Start the Flask API Backend

```powershell
# Navigate to project root
cd c:\Users\sahil\OneDrive\Desktop\ProblemsInRes

# Activate virtual environment (if not already active)
.venv\Scripts\Activate.ps1

# Install API dependencies
pip install -r api/requirements.txt

# Start Flask server
python api/app.py
```

The API will run on `http://localhost:5000`

**Available Endpoints:**
- `GET /api/health` - Health check
- `POST /api/analyze` - Analyze single comment
- `POST /api/batch-analyze` - Analyze multiple comments
- `GET /api/stats` - Get model statistics
- `GET /api/examples` - Get example comments

---

### 2. Start the React Frontend

Open a **new PowerShell terminal** (keep the API running):

```powershell
# Navigate to frontend directory
cd c:\Users\sahil\OneDrive\Desktop\ProblemsInRes\frontend

# Install Node.js dependencies (first time only)
npm install

# Start React development server
npm start
```

The frontend will automatically open at `http://localhost:3000`

---

## System Requirements

- **Python 3.12.7** (with virtual environment configured)
- **Node.js 14+** and npm
- **Trained Models:** `baseline_rf_model.pkl`, `embedding_rf_model.pkl` in `models/`
- **Embeddings Cache:** `train_embeddings.npy`, `test_embeddings.npy` in `embeddings/`

---

## Frontend Features

### 1. **Analyze Tab**
- Submit any text comment for bias detection
- View confidence scores and predictions
- See semantic similarity to training examples
- Visualize embedding vector statistics
- Interactive charts using Recharts library

### 2. **Examples Tab**
- Browse pre-classified fair and biased comments
- Click to analyze any example
- Copy examples to modify and test

### 3. **Model Stats Tab**
- Phase 1 vs Phase 2 performance comparison
- Dataset distribution visualization
- Model architecture details
- ROC-AUC and accuracy metrics

---

## Architecture

```
Frontend (React)          Backend (Flask)           ML Models
─────────────────         ───────────────           ─────────
│                         │                         │
│  User Input             │  BiasDetector           │  Random Forest
│  ↓                      │  ↓                      │  (Phase 1: Baseline)
│  axios POST             │  Load Models            │
│  /api/analyze       ────┼→ Generate Embedding  ───┼→ Sentence-BERT
│                         │  ↓                      │  (Phase 2: Semantic)
│  ← JSON Response        │  ← Predictions          │
│  ↓                      │  ← Confidence           │
│  Visualizations         │  ← Similarity           │
└─────────────────        └───────────────          └─────────
```

---

## API Request/Response Examples

### Analyze Single Comment

**Request:**
```json
POST http://localhost:5000/api/analyze
Content-Type: application/json

{
  "comment": "People from that country are always causing problems."
}
```

**Response:**
```json
{
  "comment": "People from that country are always causing problems.",
  "prediction": "biased",
  "confidence": 0.8534,
  "semantic_analysis": {
    "avg_similarity": 0.7623,
    "similar_comments": [
      {
        "comment": "That group is never trustworthy.",
        "label": "biased",
        "similarity": 0.8912
      }
    ]
  },
  "embedding_stats": {
    "dimension": 384,
    "mean": 0.0234,
    "std": 0.1567,
    "min": -0.4523,
    "max": 0.5678,
    "norm": 2.3456
  }
}
```

---

## Troubleshooting

### API Not Starting
- Ensure virtual environment is activated: `.venv\Scripts\Activate.ps1`
- Check models exist in `models/` directory
- Verify embeddings cache in `embeddings/` directory
- Run `python main.py --mode all` to regenerate if needed

### Frontend Not Loading
- Check Node.js version: `node --version` (should be 14+)
- Delete `node_modules/` and run `npm install` again
- Ensure API is running on port 5000
- Check browser console for errors

### CORS Errors
- Verify `flask-cors` is installed: `pip list | Select-String flask-cors`
- API should allow `http://localhost:3000` origin
- Check browser network tab for failed requests

### Models Not Found
- Run training pipeline: `python main.py --mode all`
- Verify files:
  - `models/baseline_rf_model.pkl`
  - `models/embedding_rf_model.pkl`
  - `embeddings/train_embeddings.npy`
  - `embeddings/test_embeddings.npy`

---

## Development

### Hot Reload
- **Backend:** Flask auto-reloads on code changes (debug mode enabled)
- **Frontend:** React dev server auto-reloads on save

### Environment Variables

Create `frontend/.env` for custom API URL:
```
REACT_APP_API_URL=http://localhost:5000
```

---

## Production Deployment

### Build Frontend
```powershell
cd frontend
npm run build
```

Outputs optimized static files to `frontend/build/`

### Serve with Flask
Modify `api/app.py` to serve static files:
```python
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend/build', 'index.html')
```

---

## Technology Stack

**Frontend:**
- React 18.2.0
- Recharts (data visualization)
- Axios (HTTP client)
- Lucide React (icons)

**Backend:**
- Flask 3.0.0
- Flask-CORS 4.0.0

**ML Pipeline:**
- Sentence-Transformers (all-MiniLM-L6-v2)
- Scikit-learn (Random Forest)
- NumPy, Pandas

---

## License & Credits

Multi-Phase ML System for Fairness & Bias Detection in Autonomous Agents
- Phase 1: Baseline toxicity features
- Phase 2: Semantic embeddings
- Phase 3: Autoregressive reasoning (planned)
