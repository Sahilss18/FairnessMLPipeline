# Quick Setup Guide

## Installation

1. Open PowerShell in the project directory:
   ```powershell
   cd c:\Users\sahil\OneDrive\Desktop\ProblemsInRes
   ```

2. Create and activate virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Add your dataset:
   - Place `fairness_dataset.csv` in the `data/` folder

## Quick Start

Run the complete pipeline:
```powershell
python main.py --mode all
```

Run interactive inference:
```powershell
python main.py --mode inference
```

## Common Commands

```powershell
# Run baseline model only
python main.py --mode baseline

# Run embedding model only
python main.py --mode embedding

# Demo with sample comments
python main.py --mode demo

# Show help
python main.py --help
```

## Troubleshooting

**Issue: Dataset not found**
- Ensure `fairness_dataset.csv` is in `data/` directory
- Check file name spelling

**Issue: Module import errors**
- Verify virtual environment is activated
- Run: `pip install -r requirements.txt`

**Issue: Memory errors**
- Reduce batch size in embedding generation
- Close other applications

## Project Structure

```
ProblemsInRes/
├── data/              # Place dataset here
├── models/            # Trained models saved here
├── embeddings/        # Embeddings saved here
├── outputs/           # Visualizations and reports
├── src/               # Source code modules
├── main.py            # Main execution script
└── requirements.txt   # Python dependencies
```

## Expected Runtime

- Baseline model: 2-5 minutes
- Embedding generation: 5-15 minutes (depends on dataset size)
- Complete pipeline: 10-20 minutes

## Next Steps After Setup

1. Run complete pipeline to generate models
2. Review outputs in `outputs/` directory
3. Try interactive inference with your own comments
4. Examine evaluation report for model comparison
