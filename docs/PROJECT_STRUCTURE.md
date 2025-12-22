# Project Structure Overview

## Directory Layout

```
ProblemsInRes/
│
├── data/                           # Dataset directory
│   ├── README.md                   # Dataset requirements and info
│   └── fairness_dataset.csv        # [USER MUST PROVIDE]
│
├── models/                         # Saved trained models
│   ├── baseline_rf_model.pkl       # [Generated during training]
│   └── embedding_rf_model.pkl      # [Generated during training]
│
├── embeddings/                     # Cached embeddings
│   ├── train_embeddings.npy        # [Generated during training]
│   └── test_embeddings.npy         # [Generated during training]
│
├── outputs/                        # Results and visualizations
│   ├── baseline_confusion_matrix.png
│   ├── baseline_roc_curve.png
│   ├── baseline_precision_recall.png
│   ├── baseline_model_size_comparison.png
│   ├── embedding_confusion_matrix.png
│   ├── embedding_roc_curve.png
│   └── evaluation_report.txt
│
├── src/                            # Source code modules
│   ├── __init__.py                 # Package initialization
│   ├── config.py                   # Configuration and paths
│   ├── utils.py                    # Utility functions
│   ├── preprocessing.py            # Data loading and cleaning
│   ├── baseline_model.py           # Phase 1: Baseline model
│   ├── embedding_model.py          # Phase 2: Embedding model
│   ├── evaluate.py                 # Model comparison
│   └── inference.py                # User input analysis
│
├── venv/                           # Python virtual environment
│
├── main.py                         # Main execution script
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # Main documentation
├── SETUP.md                        # Quick setup guide
├── EXPLANATION.md                  # Detailed project explanation
└── PROJECT_STRUCTURE.md            # This file
```

## File Descriptions

### Root Level

- **main.py**: Entry point for all operations. Supports multiple modes.
- **requirements.txt**: All Python package dependencies with versions.
- **.gitignore**: Prevents committing large files and cache.

### Documentation Files

- **README.md**: Complete project documentation including:
  - Problem statement and context
  - Implementation details for all phases
  - Installation and usage instructions
  - Future work roadmap
  
- **SETUP.md**: Quick start guide for immediate setup
  
- **EXPLANATION.md**: In-depth explanation covering:
  - Why embeddings improve performance
  - Current limitations
  - Path toward autonomous agents
  - Technical concepts explained

### Source Code (`src/`)

1. **config.py**
   - All configuration parameters
   - File paths
   - Model hyperparameters
   - Reference texts for comparison

2. **utils.py**
   - File I/O functions (save/load models and embeddings)
   - Plotting functions for visualizations
   - Metric comparison utilities

3. **preprocessing.py**
   - Data loading from CSV
   - Missing value handling
   - Train/test splitting
   - Feature extraction

4. **baseline_model.py**
   - Phase 1 implementation
   - Random Forest on numeric features
   - Baseline evaluation and visualization

5. **embedding_model.py**
   - Phase 2 implementation
   - Sentence-BERT embedding generation
   - Random Forest on embeddings
   - Improved evaluation

6. **evaluate.py**
   - Runs both phases in sequence
   - Generates comparison report
   - Saves comprehensive results

7. **inference.py**
   - BiasDetector class for real-time analysis
   - Interactive mode for user input
   - Demo mode with sample comments
   - Semantic similarity explanations

## Execution Flows

### Complete Pipeline (main.py --mode all)

```
1. Load and clean dataset
2. Prepare numeric features
3. Train baseline Random Forest
4. Evaluate baseline model
5. Save baseline model
6. Generate sentence embeddings
7. Train embedding Random Forest
8. Evaluate embedding model
9. Save embedding model
10. Compare both models
11. Generate report
```

### Baseline Only (main.py --mode baseline)

```
1. Load dataset
2. Prepare numeric features
3. Train Random Forest
4. Evaluate and visualize
5. Save model
```

### Embedding Only (main.py --mode embedding)

```
1. Load dataset
2. Generate embeddings
3. Train Random Forest on embeddings
4. Evaluate and visualize
5. Save model and embeddings
```

### Inference (main.py --mode inference)

```
1. Load trained embedding model
2. Load Sentence-BERT embedder
3. Enter interactive loop:
   - User inputs comment
   - Generate embedding
   - Predict label
   - Calculate similarities
   - Display analysis
```

## Data Flow

```
fairness_dataset.csv
        ↓
[preprocessing.py]
        ↓
    ┌───────┴───────┐
    ↓               ↓
Numeric Features   Text Data
    ↓               ↓
[baseline_model]  [Sentence-BERT]
    ↓               ↓
RandomForest    384-dim vectors
    ↓               ↓
Predictions   [embedding_model]
    ↓               ↓
Metrics      RandomForest
    ↓               ↓
baseline.pkl  embedding.pkl
    ↓               ↓
    └───────┬───────┘
            ↓
      [evaluate.py]
            ↓
    Comparison Report
```

## Key Dependencies

### Core ML Libraries
- **scikit-learn**: Random Forest, metrics, data splitting
- **numpy**: Array operations
- **pandas**: Data manipulation

### Deep Learning
- **sentence-transformers**: Sentence-BERT embeddings
- **torch**: Backend for transformers

### Visualization
- **matplotlib**: Plotting
- **seaborn**: Statistical visualizations

## Model Persistence

### Saved Artifacts

1. **baseline_rf_model.pkl** (~10-50 MB)
   - Trained Random Forest on numeric features
   - Includes all decision trees and parameters

2. **embedding_rf_model.pkl** (~10-50 MB)
   - Trained Random Forest on embeddings
   - Includes all decision trees and parameters

3. **train_embeddings.npy** (~50-200 MB)
   - Cached training set embeddings
   - Shape: (n_train_samples, 384)

4. **test_embeddings.npy** (~10-50 MB)
   - Cached test set embeddings
   - Shape: (n_test_samples, 384)

### Loading Models

```python
from utils import load_model
model = load_model('models/embedding_rf_model.pkl')
```

## Extension Points

### Adding New Models

1. Create new file in `src/` (e.g., `xgboost_model.py`)
2. Follow pattern from `baseline_model.py`
3. Add import to `main.py`
4. Add command-line option

### Adding New Metrics

1. Add metric function to `utils.py`
2. Call in evaluation functions
3. Update report generation

### Custom Embeddings

1. Modify `SENTENCE_TRANSFORMER_MODEL` in `config.py`
2. Re-run Phase 2
3. Compare results

### Phase 3 Integration

1. Create `src/reasoning_model.py`
2. Load autoregressive model (GPT, LLaMA)
3. Generate explanations from predictions
4. Add to `main.py` as `--mode reasoning`

## Common Workflows

### First Time Setup
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Add dataset to data/
python main.py --mode all
```

### Quick Testing
```powershell
python main.py --mode demo
```

### Experimentation
```python
# Modify config.py parameters
# Re-run specific phase
python main.py --mode embedding
```

### Production Inference
```python
from src.inference import BiasDetector
detector = BiasDetector()
result = detector.analyze_comment("Your text here")
print(result['sentiment'])
```

## Performance Considerations

### Memory Usage
- Dataset loading: ~1-2 GB (depends on size)
- Embedding generation: ~2-4 GB
- Model training: ~1-2 GB
- **Total recommended RAM**: 8 GB minimum, 16 GB preferred

### Processing Time
- Data preprocessing: <1 minute
- Baseline training: 2-5 minutes
- Embedding generation: 5-15 minutes (CPU)
- Embedding training: 2-5 minutes
- **Total pipeline**: 10-25 minutes

### Optimization Tips
- Use GPU for embedding generation (if available)
- Reduce dataset size for testing
- Adjust n_estimators for faster training
- Cache embeddings to avoid regeneration

## Troubleshooting Guide

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Dataset Errors
- Check `data/fairness_dataset.csv` exists
- Verify column names match requirements
- Ensure CSV is properly formatted

### Memory Errors
- Reduce dataset size
- Close other applications
- Use smaller embedding model

### Model Loading Errors
- Ensure models were trained and saved
- Check file paths in `config.py`
- Verify pickle files are not corrupted

## Next Steps

1. **Initial Setup**: Follow SETUP.md
2. **Run Pipeline**: `python main.py --mode all`
3. **Review Results**: Check `outputs/` directory
4. **Try Inference**: `python main.py --mode inference`
5. **Read Details**: Review EXPLANATION.md
6. **Customize**: Modify `config.py` and re-run
7. **Extend**: Add Phase 3 reasoning components

## Support

For issues:
1. Check error messages carefully
2. Review relevant documentation file
3. Verify dataset format
4. Ensure dependencies are installed
5. Check Python version (3.8+ required)
