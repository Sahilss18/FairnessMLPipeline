# Getting Started Guide

## Welcome!

This guide will walk you through running your fairness and bias detection system from start to finish.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Windows with PowerShell
- ✅ Python 3.8 or higher installed
- ✅ At least 8 GB RAM
- ✅ 2 GB free disk space
- ✅ Your dataset (`fairness_dataset.csv`)

### Check Python Version
```powershell
python --version
```
Should show Python 3.8 or higher.

## Step-by-Step Setup

### Step 1: Navigate to Project Directory (1 minute)

```powershell
cd c:\Users\sahil\OneDrive\Desktop\ProblemsInRes
```

### Step 2: Create Virtual Environment (2 minutes)

```powershell
python -m venv venv
```

This creates an isolated Python environment for the project.

### Step 3: Activate Virtual Environment (30 seconds)

```powershell
.\venv\Scripts\Activate.ps1
```

Your prompt should now show `(venv)` at the beginning.

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies (5-10 minutes)

```powershell
pip install -r requirements.txt
```

This will install:
- NumPy and Pandas for data processing
- Scikit-learn for machine learning
- Sentence-Transformers for embeddings
- Matplotlib and Seaborn for visualization
- PyTorch as backend

**Note**: First-time installation may take several minutes as it downloads large packages.

### Step 5: Add Your Dataset (1 minute)

Place your `fairness_dataset.csv` file in the `data/` folder.

**Required format:**
```csv
comment_text,target,other_numeric_columns...
"Text comment here",0.85,0.5,0.3,...
```

See `data/README.md` for detailed format requirements.

### Step 6: Verify Setup (30 seconds)

```powershell
python --version
pip list | Select-String "sentence-transformers"
```

Should show version information confirming installation.

## Your First Run

### Option A: Complete Pipeline (Recommended First Time)

```powershell
python main.py --mode all
```

**What happens:**
1. Loads and cleans your dataset
2. Trains baseline model (2-5 min)
3. Generates embeddings (5-15 min)
4. Trains embedding model (2-5 min)
5. Creates visualizations
6. Generates comparison report

**Total time**: 10-25 minutes depending on dataset size

**Console output will show:**
```
================================================================================
FAIRNESS AND BIAS DETECTION SYSTEM FOR AUTONOMOUS AGENTS
================================================================================

Loading dataset from: data\fairness_dataset.csv
Dataset shape: (10000, 10)
...
[Progress updates as it runs]
...
================================================================================
PIPELINE COMPLETE
================================================================================
```

### Option B: Quick Demo (Fast Testing)

```powershell
python main.py --mode demo
```

**What happens:**
- Runs analysis on pre-defined sample comments
- Shows how the system works
- Takes 1-2 minutes

**Good for**: Understanding output format before full training

## Understanding the Output

### Console Output

You'll see:
1. **Data loading**: Dataset size and missing value handling
2. **Phase 1**: Baseline model training progress
3. **Metrics**: Accuracy, ROC-AUC, confusion matrix
4. **Phase 2**: Embedding generation progress
5. **Comparison**: Side-by-side performance

### Files Generated

Check these directories:

#### `models/`
- `baseline_rf_model.pkl` - Trained baseline model
- `embedding_rf_model.pkl` - Trained embedding model

#### `embeddings/`
- `train_embeddings.npy` - Training set embeddings
- `test_embeddings.npy` - Test set embeddings

#### `outputs/`
- Confusion matrices (PNG images)
- ROC curves (PNG images)
- Precision-recall curves (PNG images)
- `evaluation_report.txt` - Text summary

### Reviewing Results

1. **Open `outputs/evaluation_report.txt`**
   - Shows accuracy and ROC-AUC for both models
   - Displays improvement percentages

2. **View confusion matrices**
   - `baseline_confusion_matrix.png`
   - `embedding_confusion_matrix.png`
   - Compare true positives vs false positives

3. **Check ROC curves**
   - Higher AUC = better model
   - Compare baseline vs embedding

## Interactive Usage

### Try the Interactive Mode

```powershell
python main.py --mode inference
```

**What you can do:**
```
Enter comment: Everyone deserves equal treatment.
```

**System responds:**
```
================================================================================
Comment: Everyone deserves equal treatment.
Prediction: Fair / Non-Toxic
Model Confidence: 0.08

Embedding (first 10 of 384 dimensions):
[0.12, -0.34, 0.56, ...]

Semantic Similarity:
  To Positive Reference: 0.82
  To Toxic Reference:    0.15

Explanation: Meaning is closer to positive or fair expressions.
================================================================================
```

### Exit Interactive Mode
Type `quit` or `exit` or press `Ctrl+C`

## Common First-Time Issues

### Issue 1: "fairness_dataset.csv not found"

**Solution:**
```powershell
# Check if file exists
Test-Path data\fairness_dataset.csv
# Should return True
```

If False, add your dataset to the `data/` folder.

### Issue 2: "Cannot activate virtual environment"

**Solution:**
```powershell
# Run as administrator or adjust policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 3: Installation fails

**Solution:**
```powershell
# Upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue 4: Out of memory

**Solution:**
- Close other applications
- Use smaller dataset for testing
- Restart computer and try again

### Issue 5: Very slow embedding generation

**Solution:**
- Normal on CPU (5-15 minutes for 10k samples)
- Consider smaller dataset for initial testing
- GPU would speed this up 10x (optional)

## What to Expect: Performance Metrics

### Typical Results

**Baseline Model (Phase 1):**
- Accuracy: 70-80%
- ROC-AUC: 0.75-0.85

**Embedding Model (Phase 2):**
- Accuracy: 80-90%
- ROC-AUC: 0.85-0.95

**Improvement:**
- 5-15% accuracy gain
- 10-20% AUC improvement

### If Your Results Are Different

**Lower accuracy than expected:**
- Check dataset quality
- Ensure proper labels (0 = fair, 1 = toxic)
- Verify sufficient training data (1000+ samples)

**Very high accuracy (>95%):**
- May indicate data leakage
- Check for duplicate samples
- Verify train/test split

## Next Steps After First Run

### 1. Review Documentation

Read in this order:
1. `CONVERSION_SUMMARY.md` - What was created
2. `EXPLANATION.md` - Technical details
3. `PHASE3_DESIGN.md` - Future work

### 2. Experiment with Settings

Edit `src/config.py`:
```python
# Try different model sizes
BASELINE_CONFIG = {
    'n_estimators': 200,  # Increase trees
    'random_state': 42
}

# Try different embeddings
SENTENCE_TRANSFORMER_MODEL = 'all-mpnet-base-v2'  # Larger model
```

Then re-run:
```powershell
python main.py --mode all
```

### 3. Analyze Your Own Comments

```powershell
python main.py --mode inference
```

Try various comments to test the system:
- Clearly fair statements
- Obviously toxic text
- Subtle bias examples
- Edge cases

### 4. Examine the Code

Start with:
1. `src/preprocessing.py` - See how data is loaded
2. `src/baseline_model.py` - Understand Phase 1
3. `src/embedding_model.py` - Understand Phase 2
4. `src/inference.py` - See inference logic

### 5. Plan Phase 3

Review `PHASE3_DESIGN.md` to understand:
- Autoregressive reasoning
- Chain-of-thought explanations
- Fairness verification
- Path to autonomous agents

## Running Individual Phases

### Just Baseline (Phase 1)

```powershell
python main.py --mode baseline
```
Faster for testing baseline changes.

### Just Embeddings (Phase 2)

```powershell
python main.py --mode embedding
```
Run after tweaking embedding parameters.

### Just Evaluation

```powershell
python src\evaluate.py
```
Re-compare existing models without retraining.

### Just Demo

```powershell
python main.py --mode demo
```
Quick test with sample comments.

## Working with Results

### View Images

Navigate to `outputs/` folder and open PNG files:
- Double-click to view in default image viewer
- Compare baseline vs embedding visualizations

### Read Report

```powershell
notepad outputs\evaluation_report.txt
```

### Export Results

Copy outputs for your report:
```powershell
# Copy all outputs to desktop
Copy-Item outputs\* -Destination $env:USERPROFILE\Desktop\FairnessResults\
```

## Tips for Best Results

### 1. Dataset Quality
- At least 1000 samples
- Balanced classes if possible
- Clean, well-labeled data
- Diverse examples

### 2. First Run
- Use complete pipeline (`--mode all`)
- Review all outputs
- Understand baseline performance

### 3. Optimization
- Start with default settings
- Change one parameter at a time
- Document what works

### 4. Documentation
- Take screenshots of results
- Save console output
- Note any issues encountered

## Troubleshooting Commands

### Check Python environment
```powershell
python --version
pip list
```

### Verify dataset
```powershell
Get-Content data\fairness_dataset.csv -TotalCount 5
```

### Check file paths
```powershell
Test-Path data\fairness_dataset.csv
Test-Path src\config.py
```

### View logs
```powershell
python main.py --mode all 2>&1 | Tee-Object -FilePath run.log
```

### Clean and restart
```powershell
# Remove generated files
Remove-Item models\*.pkl -ErrorAction SilentlyContinue
Remove-Item embeddings\*.npy -ErrorAction SilentlyContinue
Remove-Item outputs\* -ErrorAction SilentlyContinue

# Re-run
python main.py --mode all
```

## Daily Workflow

### Starting a Session
```powershell
cd c:\Users\sahil\OneDrive\Desktop\ProblemsInRes
.\venv\Scripts\Activate.ps1
```

### Running Experiments
```powershell
# Edit config.py with new parameters
notepad src\config.py

# Run experiment
python main.py --mode all

# Review results
explorer outputs
```

### Ending a Session
```powershell
deactivate  # Deactivate virtual environment
```

## Getting Help

### Documentation Files
- **Quick questions**: `SETUP.md`
- **Technical details**: `EXPLANATION.md`
- **Architecture**: `PROJECT_STRUCTURE.md`
- **Future work**: `PHASE3_DESIGN.md`

### Code Comments
All Python files are well-commented. Read the docstrings:
```python
# At top of each function
def function_name():
    """
    Description of what function does.
    
    Args:
        param: Description
        
    Returns:
        Description of return value
    """
```

### Console Output
The system prints detailed progress:
- What it's doing
- File paths
- Metrics
- Warnings if issues detected

## Success Criteria

You know everything is working when:

✅ No errors during installation
✅ Pipeline completes without crashes
✅ Models saved in `models/` folder
✅ Visualizations in `outputs/` folder
✅ Evaluation report generated
✅ Interactive mode works
✅ Results make sense (accuracy > 60%)

## Ready to Start!

You're all set! Run your first experiment:

```powershell
# Make sure you're in the project directory
cd c:\Users\sahil\OneDrive\Desktop\ProblemsInRes

# Activate environment
.\venv\Scripts\Activate.ps1

# Run complete pipeline
python main.py --mode all
```

Grab a coffee, the first run takes 10-25 minutes. You'll see progress updates in the console.

After completion, explore the `outputs/` directory to see your results!

---

**Questions?** Check `EXPLANATION.md` for detailed explanations of every component.

**Issues?** Review the troubleshooting section above.

**Ready for more?** Read `PHASE3_DESIGN.md` to plan future development.

Good luck with your research! 🚀
