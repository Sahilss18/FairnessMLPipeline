# Fairness & Bias Detection System

Multi-phase ML system for detecting bias and toxicity in text using Random Forest, Sentence-BERT embeddings, and Ollama Qwen2.5:3b reasoning model.

## 🚀 Quick Start

```powershell
# Start the web application (Flask + React)
.\start_web_ui.ps1

# Or run in offline mode
.\start_offline.ps1
```

Then open: http://localhost:3000

## 📁 Project Structure

```
ProblemsInRes/
├── 📄 main.py                    # Main CLI entry point
├── 📄 requirements.txt           # Python dependencies
├── 🚀 start_web_ui.ps1          # Web UI launcher
├── 🚀 start_offline.ps1         # Offline mode launcher
│
├── 📂 src/                       # Core ML pipeline
│   ├── config.py                # Configuration & paths
│   ├── preprocessing.py         # Data preprocessing
│   ├── baseline_model.py        # Phase I: Baseline RF
│   ├── embedding_model.py       # Phase II: SBERT embeddings
│   ├── ollama_reasoner.py       # Phase III: Ollama reasoning
│   └── inference.py             # BiasDetector interface
│
├── 📂 api/                       # Flask REST API backend
│   └── app.py                   # API endpoints
│
├── 📂 frontend/                  # React web interface
│   ├── src/
│   │   ├── App.js               # Main React app
│   │   └── components/          # UI components
│   └── package.json
│
├── 📂 tests/                     # Unit & integration tests
│   ├── test_api.py
│   ├── test_ollama_direct.py
│   └── test_*.py
│
├── 📂 scripts/                   # Utility scripts
│   ├── generate_comprehensive_report.py
│   ├── generate_ollama_results.py
│   ├── start_web_ui.ps1
│   └── start_offline.ps1
│
├── 📂 docs/                      # Documentation
│   ├── GETTING_STARTED.md
│   ├── SETUP.md
│   ├── PHASE3_IMPLEMENTATION.md
│   └── *.md
│
├── 📂 models/                    # Trained models (.pkl)
├── 📂 embeddings/                # Cached SBERT embeddings (.npy)
├── 📂 outputs/                   # Reports & visualizations
├── 📂 data/                      # Dataset storage
└── 📂 AiFairness.csv/           # Main dataset
```

## 🛠️ Setup

### Prerequisites
- Python 3.12.7
- Node.js 18+ (for frontend)
- Ollama 0.13.4 (for Phase III reasoning)

### Installation

1. **Clone & Setup Python Environment**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Install Ollama**
```powershell
# Download from https://ollama.ai
ollama pull qwen2.5:3b
```

3. **Train Models**
```powershell
python main.py --mode all
```

4. **Install Frontend Dependencies**
```powershell
cd frontend
npm install
cd ..
```

## 🎯 Features

### Three Analysis Modes

**1. Baseline Model**
- Random Forest + SBERT embeddings
- 80.33% accuracy
- ~50ms inference time

**2. Ollama Reasoning**
- Qwen2.5:3b autoregressive model
- Natural language explanations
- ~2.2s inference time
- 85% accuracy (estimated)

**3. Compare Both**
- Side-by-side validation
- Disagreement detection
- Multi-model consensus

### Web Interface
- Real-time bias detection
- Interactive examples
- Performance statistics
- Model comparison visualization

## 📊 Performance Metrics

| Metric | Baseline | Ollama | 
|--------|----------|--------|
| Accuracy | 80.33% | ~85% |
| Inference Time | 50ms | 2.2s |
| Model Size | 90MB | 1.9GB |
| Explainability | Scores | Natural Language |
| Offline | ✅ Yes | ✅ Yes |

## 🧪 Testing

```powershell
# Test API endpoints
python tests/test_api.py

# Test Ollama integration
python tests/test_ollama_direct.py

# Test full pipeline
python tests/test_model_pipeline.py
```

## 📖 Documentation

- [Getting Started](docs/GETTING_STARTED.md) - First-time setup guide
- [Setup Guide](docs/SETUP.md) - Detailed installation
- [Phase III Implementation](docs/PHASE3_IMPLEMENTATION.md) - Ollama integration details
- [Offline Mode](docs/OFFLINE_MODE.md) - Running without internet
- [Frontend Guide](docs/FRONTEND_GUIDE.md) - UI customization

## 🔬 Dataset

- **Source**: AiFairness.csv (90,902 comments)
- **Labels**: Binary (0=Fair, 1=Biased)
- **Threshold**: Toxicity ≥ 0.6 = Biased
- **Protected Attributes**: Gender, Race, Age, Religion, Disability, LGBTQ+

## 🤝 Contributing

1. All tests in `tests/` folder
2. Utility scripts in `scripts/` folder  
3. Documentation in `docs/` folder
4. Follow existing code style

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Sentence-BERT (all-MiniLM-L6-v2)
- Ollama (Qwen2.5:3b)
- AiFairness Dataset

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Built with**: Python 3.12.7 • React 18.2.0 • Flask 3.0.0 • Ollama 0.13.4
