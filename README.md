# Fairness and Bias Detection System for Autonomous Agents

## Project Overview

This project implements a multi-phase machine learning system to identify and mitigate problems in autonomous agents, specifically focusing on bias, fairness, and accountability. The system analyzes text content to detect potentially biased or toxic language, providing both classification predictions and interpretable explanations.

**🌐 Now with Interactive Web Interface!** Submit text comments and visualize bias detection results in real-time through a modern React frontend powered by Flask API.

## Problem Statement

Autonomous agents and AI systems can perpetuate harmful biases present in training data, leading to unfair treatment of individuals or groups. Key problems addressed:

- **Bias Detection**: Identifying prejudiced or discriminatory language in text
- **Fairness Assessment**: Evaluating whether content treats all groups equitably
- **Accountability**: Providing transparent explanations for AI decisions

While autonomous agents should ideally reason independently and make ethical decisions, current AI systems require human oversight and structured evaluation frameworks. This project builds toward that goal by creating tools that support autonomous agents in making fairer decisions.

## What Has Been Completed

### Phase 1: Baseline Model (Numeric Features)

The first phase establishes baseline performance using traditional machine learning on numeric features from a fairness dataset.

**Implementation:**
- Data loading and preprocessing from `fairness_dataset.csv`
- Handling missing values in text, numeric, and categorical fields
- Feature extraction using only numeric columns
- Training a Random Forest classifier with 100 estimators
- Binary classification: Fair (0) vs Toxic/Biased (1)

**Evaluation Metrics:**
- Accuracy
- Precision, Recall, F1-Score
- ROC-AUC score
- Confusion Matrix
- Precision-Recall Curve

**Results:**
The baseline model provides a performance benchmark using simple numerical features. However, it cannot capture semantic meaning or contextual nuances in language, limiting its effectiveness for fairness detection.

### Phase 2: Embedding-Based Model (Sentence-BERT)

The second phase introduces semantic understanding through sentence embeddings, significantly improving the system's ability to detect bias.

**Why Embeddings Were Introduced:**
- Numeric features alone cannot capture the meaning of text
- Sentence-BERT (all-MiniLM-L6-v2) converts text into 384-dimensional vectors
- Similar meanings cluster together in embedding space
- Embeddings preserve semantic relationships (e.g., "hate" and "dislike" are close)

**Implementation:**
- Generate sentence embeddings for all comments using Sentence-BERT
- Train Random Forest classifier (150 estimators) on embeddings
- Compare performance against baseline model
- Semantic similarity analysis using cosine distance

**Evaluation:**
- Same metrics as Phase 1 for direct comparison
- Additional semantic similarity to reference sentences
- Visual comparison of embedding space clustering

**Improvement Over Baseline:**
The embedding model shows measurable improvements in accuracy and ROC-AUC because it understands language meaning rather than just numeric patterns. This enables better discrimination between genuinely fair statements and subtly biased language.

### User Input Analysis

A practical inference system allows users to input comments and receive:
- Binary prediction: Fair or Toxic/Biased
- Confidence score (probability)
- Embedding vector preview (first 10 dimensions)
- Semantic similarity to positive and toxic reference texts
- Natural language explanation of the classification

**Example Analysis:**
```
Comment: "Everyone deserves respect regardless of their religion."
Prediction: Fair / Non-Toxic
Model Confidence: 0.12
Similarity to Positive Reference: 0.78
Similarity to Toxic Reference: 0.23
Explanation: Meaning is closer to positive or fair expressions.
```

## Why This Is Not Yet an Autonomous Agent

The current system is a **tool for supporting autonomous agents**, not an autonomous agent itself. Here is why:

**Current System:**
- Predicts labels based on learned patterns
- Requires pre-labeled training data
- Cannot reason about new ethical scenarios
- Does not explain its reasoning in human language
- Cannot adapt to new fairness definitions

**True Autonomous Agent Requirements:**
- Self-directed goal setting
- Contextual reasoning over complex situations
- Natural language explanation generation
- Learning from feedback without retraining
- Ethical decision-making under uncertainty

The current implementation focuses on accurate classification and basic interpretability, which are necessary but insufficient for full autonomy. Phase 3 will address this gap.

## Future Work: Phase 3 and Beyond

### Phase 3: Autoregressive Reasoning and Accountability (Planned)

The third phase will integrate an autoregressive language model to enable chain-of-thought reasoning and human-interpretable explanations.

**Why Autoregressive Models:**
- Generate text token-by-token, allowing step-by-step reasoning
- Can explain "why" a decision was made, not just "what" the decision is
- Enable contextual fairness verification by comparing to reference examples
- Support dynamic reasoning over novel inputs

**Architecture:**
The autoregressive model will act as an explanation layer on top of the existing classifier:
1. Classifier predicts Fair/Toxic label (as in Phase 2)
2. Autoregressive model receives: embedding, prediction, confidence
3. Model generates structured explanation describing intent, tone, and bias
4. System compares semantic meaning to reference examples
5. If inconsistencies detected, flag for review or generate warning

**Example Output:**
```
Input: "People from that community are usually lazy."
Classification: Toxic/Biased (confidence: 0.89)
Explanation: "This statement generalizes negative traits to an entire group,
which constitutes stereotyping and bias. The language assigns inherent
characteristics based on group membership rather than individual behavior."
Fairness Verification: Contradicts principle of individual assessment.
```

**Benefits:**
- Moves system closer to autonomous agent behavior
- Provides transparency and trust through explanations
- Enables human review of edge cases
- Supports accountability in high-stakes decisions

### Phase 4: Explicit Fairness Metrics (Planned)

Future phases will implement quantitative fairness measures:

**Demographic Parity Difference (DPD):**
- Measures whether positive predictions are equally distributed across groups
- Formula: P(Y=1|A=0) - P(Y=1|A=1)
- Ideal value: 0 (no disparity)

**Disparate Impact (DI):**
- Ratio of positive prediction rates between groups
- Formula: P(Y=1|A=0) / P(Y=1|A=1)
- Ideal value: 1 (equal impact)

These metrics will enable systematic evaluation of fairness across demographic groups and support regulatory compliance.

### Phase 5: Toward Full Autonomy (Long-term Vision)

The ultimate goal is an autonomous agent that:
- Monitors its own fairness metrics continuously
- Detects distribution shift and concept drift
- Requests human guidance only when uncertain
- Updates internal reasoning through self-reflection
- Generates accountability reports automatically

## Project Structure

```
ProblemsInRes/
│
├── data/
│   └── AiFairness.csv               # Input dataset (90,902 samples)
│
├── models/
│   ├── baseline_rf_model.pkl        # Trained baseline model
│   └── embedding_rf_model.pkl       # Trained embedding model
│
├── embeddings/
│   ├── train_embeddings.npy         # Training set embeddings
│   └── test_embeddings.npy          # Test set embeddings
│
├── outputs/
│   ├── baseline_confusion_matrix.png
│   ├── baseline_roc_curve.png
│   ├── embedding_confusion_matrix.png
│   ├── embedding_roc_curve.png
│   └── evaluation_report.txt        # Summary report
│
├── src/
│   ├── config.py                    # Configuration and paths
│   ├── utils.py                     # Utility functions
│   ├── preprocessing.py             # Data loading and cleaning
│   ├── baseline_model.py            # Phase 1 implementation
│   ├── embedding_model.py           # Phase 2 implementation
│   ├── evaluate.py                  # Model comparison
│   └── inference.py                 # User input analysis
│
├── api/
│   ├── app.py                       # Flask REST API server
│   └── requirements.txt             # API dependencies
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── AnalysisResults.js   # Visualization of analysis
│   │   │   ├── ExampleComments.js   # Sample comments
│   │   │   └── Statistics.js        # Model performance stats
│   │   ├── App.js                   # Main React app
│   │   ├── App.css                  # Styling
│   │   └── index.js                 # React entry point
│   └── package.json                 # Node.js dependencies
│
├── main.py                          # Main execution script
├── start_web_ui.ps1                 # Startup script for web interface
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── FRONTEND_GUIDE.md                # Web UI documentation
└── [8 other documentation files]
```

## Installation and Setup

### Prerequisites
- Python 3.12+ 
- Node.js 14+ and npm (for web interface)
- Virtual environment (recommended)

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```powershell
   cd c:\Users\sahil\OneDrive\Desktop\ProblemsInRes
   ```

2. **Create a virtual environment:**
   ```powershell
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Dataset is already configured:**
   - Dataset: `AiFairness.csv` (90,902 samples)
   - Path configured in `src/config.py`

6. **For web interface, install Node.js dependencies:**
   ```powershell
   cd frontend
   npm install
   cd ..
   ```
   - Copy `fairness_dataset.csv` into the `data/` folder
   - Ensure it has columns: `comment_text`, `target`, and numeric features

## Usage

### Option 1: Web Interface (Recommended)

**Quick Start:**
```powershell
.\start_web_ui.ps1
```

This script will:
- Start Flask API backend on `http://localhost:5000`
- Start React frontend on `http://localhost:3000`
- Open your browser automatically

**Manual Start:**

Terminal 1 - Flask API:
```powershell
.\.venv\Scripts\Activate.ps1
python api/app.py
```

Terminal 2 - React Frontend:
```powershell
cd frontend
npm start
```

**Web Interface Features:**
- 📝 Submit text comments for real-time analysis
- 📊 Interactive visualizations (confidence scores, semantic similarity)
- 📈 Model performance statistics
- 🔍 Browse example comments (fair vs biased)
- 🎯 Embedding vector analysis with radar charts

See `FRONTEND_GUIDE.md` for detailed documentation.

---

### Option 2: Command Line - Run Complete Pipeline

Train both models and compare results:

```powershell
python main.py --mode all
```

### Option 3: Run Individual Phases

**Phase 1 only (Baseline Model):**
```powershell
python main.py --mode baseline
```

**Phase 2 only (Embedding Model):**
```powershell
python main.py --mode embedding
```

### Option 4: Interactive Inference (CLI)

Analyze custom comments in terminal:

```powershell
python main.py --mode inference
```

Then enter comments when prompted. Type `quit` to exit.

### Option 5: Run Specific Modules

**Data preprocessing only:**
```powershell
python src/preprocessing.py
```

**Evaluation and comparison:**
```powershell
python src/evaluate.py
```

**Demo analysis with sample comments:**
```powershell
python src/inference.py
```

## Expected Output

After running the complete pipeline:
- Trained models saved in `models/`
- Embeddings saved in `embeddings/`
- Visualizations saved in `outputs/`
- Console output showing:
  - Data preprocessing summary
  - Training progress
  - Evaluation metrics for both models
  - Performance comparison

## Key Implementation Details

### Data Preprocessing
- Missing text values filled with empty strings
- Missing numeric values filled with zeros
- Missing categorical values filled with 'Unknown'
- Continuous target labels converted to binary (threshold: 0.5)

### Model Configuration
- Baseline: Random Forest with 100 estimators
- Embedding: Random Forest with 150 estimators
- Train/test split: 80/20
- Random state: 42 (reproducibility)

### Embedding Generation
- Model: all-MiniLM-L6-v2 (Sentence-BERT)
- Output dimension: 384
- Benefits: Fast inference, good semantic understanding

## Limitations and Considerations

### Current Limitations
1. **Static Classification**: Models require retraining for new patterns
2. **Limited Explainability**: No step-by-step reasoning (addressed in Phase 3)
3. **No Fairness Metrics**: DPD and DI not yet implemented
4. **Supervised Learning**: Requires labeled training data
5. **Context Insensitivity**: Cannot reason about speaker intent or situation

### Ethical Considerations
- This system is a decision-support tool, not a replacement for human judgment
- False positives may flag legitimate speech
- False negatives may miss harmful content
- Should be used with human oversight, especially in sensitive applications

## Research and Academic Context

This project is suitable for:
- Final year undergraduate or graduate research
- Machine learning course projects
- Fairness and ethics in AI studies
- Natural language processing applications

**Potential Extensions:**
- Cross-lingual bias detection
- Real-time moderation systems
- Fairness auditing for existing AI systems
- Integration with content management platforms

## Technical Requirements

**Minimum System Requirements:**
- CPU: Multi-core processor (4+ cores recommended)
- RAM: 8 GB minimum, 16 GB recommended
- Storage: 2 GB for models and embeddings
- Python 3.8+

**Dependencies:**
- NumPy, Pandas (data processing)
- Scikit-learn (machine learning)
- Sentence-Transformers (embeddings)
- Matplotlib, Seaborn (visualization)
- PyTorch (backend for transformers)

## References and Acknowledgments

**Key Technologies:**
- Sentence-BERT: Reimers & Gurevych (2019)
- Random Forest: Breiman (2001)
- Fairness in ML: Multiple research sources

**Dataset:**
User-provided fairness dataset with text comments and toxicity labels.

## Contact and Support

For questions, issues, or contributions:
- Review code documentation in each module
- Check console output for error messages
- Ensure dataset is properly formatted
- Verify all dependencies are installed

## License

This project is developed for educational and research purposes.

---

**Project Status**: Phases 1 and 2 complete. Phase 3 (autoregressive reasoning) in planning stage.

**Last Updated**: December 2025
