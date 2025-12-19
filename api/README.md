# Fairness & Bias Detection API

Flask REST API backend for the Fairness & Bias Detection System.

## Endpoints

### Health Check
```
GET /api/health
```
Returns API status and model loading state.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

### Analyze Single Comment
```
POST /api/analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "comment": "Your text to analyze here"
}
```

**Response:**
```json
{
  "comment": "Your text to analyze here",
  "prediction": "biased" | "fair",
  "confidence": 0.8534,
  "semantic_analysis": {
    "avg_similarity": 0.7623,
    "similar_comments": [
      {
        "comment": "Similar comment from training data",
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

### Batch Analyze
```
POST /api/batch-analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "comments": [
    "First comment to analyze",
    "Second comment to analyze"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "comment": "First comment to analyze",
      "prediction": "fair",
      "confidence": 0.9234
    },
    {
      "comment": "Second comment to analyze",
      "prediction": "biased",
      "confidence": 0.7856
    }
  ]
}
```

---

### Model Statistics
```
GET /api/stats
```

Returns comprehensive model performance metrics.

**Response:**
```json
{
  "baseline_model": {
    "accuracy": 0.9997,
    "roc_auc": 1.0,
    "n_estimators": 100,
    "n_features": 42
  },
  "embedding_model": {
    "accuracy": 0.8008,
    "roc_auc": 0.885,
    "n_estimators": 150,
    "n_features": 384
  },
  "dataset": {
    "total_samples": 90902,
    "train_size": 72721,
    "test_size": 18181
  }
}
```

---

### Example Comments
```
GET /api/examples
```

Returns sample fair and biased comments from training data.

**Response:**
```json
{
  "examples": [
    {
      "comment": "This is a fair statement.",
      "label": "fair"
    },
    {
      "comment": "That group is always problematic.",
      "label": "biased"
    }
  ]
}
```

---

## Running the API

### Prerequisites
- Python 3.12+
- Trained models in `models/` directory
- Embeddings cache in `embeddings/` directory

### Start Server

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r api/requirements.txt

# Run Flask server
python api/app.py
```

The API will run on `http://localhost:5000`

---

## Dependencies

- **Flask 3.0.0**: Web framework
- **Flask-CORS 4.0.0**: Cross-origin resource sharing
- **scikit-learn**: ML models
- **sentence-transformers**: Embedding generation
- **numpy, pandas**: Data handling

---

## CORS Configuration

The API allows requests from:
- `http://localhost:3000` (React dev server)

To add more origins, modify `app.py`:

```python
CORS(app, origins=["http://localhost:3000", "http://your-domain.com"])
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing/invalid parameters)
- `500`: Server error (model loading failure, etc.)

**Error Response Format:**
```json
{
  "error": "Detailed error message"
}
```

---

## Architecture

```
Client Request
     ↓
Flask API (app.py)
     ↓
BiasDetector (inference.py)
     ↓
├── Load Models (baseline_rf, embedding_rf)
├── Generate Embeddings (Sentence-BERT)
├── Make Predictions
└── Calculate Similarities
     ↓
JSON Response
```

---

## Development

### Debug Mode
Flask runs in debug mode by default, enabling:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Logging
The API logs to console with timestamps and severity levels.

### Testing with curl

**Health Check:**
```powershell
curl http://localhost:5000/api/health
```

**Analyze Comment:**
```powershell
curl -X POST http://localhost:5000/api/analyze `
  -H "Content-Type: application/json" `
  -d '{\"comment\": \"Test comment here\"}'
```

---

## Production Considerations

For production deployment:

1. **Disable Debug Mode:**
   ```python
   app.run(host='0.0.0.0', port=5000, debug=False)
   ```

2. **Use Production WSGI Server:**
   ```powershell
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api.app:app
   ```

3. **Environment Variables:**
   - Set `FLASK_ENV=production`
   - Configure secret keys
   - Set allowed origins

4. **Model Loading:**
   - Models are loaded once at startup
   - Cached in memory for fast inference
   - ~1-2 second startup time

---

## API Performance

- **Single Analysis:** ~50-200ms
- **Batch Analysis:** ~100-500ms (5-10 comments)
- **Model Loading:** ~1-2 seconds (startup)
- **Memory Usage:** ~500MB-1GB (models + embeddings)

---

## Troubleshooting

**Models Not Found:**
- Ensure `baseline_rf_model.pkl` and `embedding_rf_model.pkl` exist in `models/`
- Run `python main.py --mode all` to train models

**Import Errors:**
- Check virtual environment is activated
- Verify all dependencies installed: `pip list`
- Reinstall: `pip install -r api/requirements.txt`

**Port Already in Use:**
- Change port in `app.py`: `app.run(port=5001)`
- Kill existing process: `Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process`

---

## License

Part of the Fairness & Bias Detection System for Autonomous Agents
