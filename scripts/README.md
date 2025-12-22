# Utility Scripts

This directory contains utility scripts for report generation, data analysis, and system startup.

## 📊 Report Generation Scripts

### generate_comprehensive_report.py
Generates complete evaluation reports with visualizations:
- Ollama reasoning analysis
- Model comparison (Baseline vs Ollama)
- System reliability metrics
- 30-day performance trends

**Output Files:**
- `outputs/ollama_reasoning_analysis.png`
- `outputs/model_comparison.png`
- `outputs/system_reliability.png`
- `outputs/comprehensive_evaluation_report.txt`
- `outputs/evaluation_metrics.json`

**Usage:**
```powershell
python scripts/generate_comprehensive_report.py
```

### generate_ollama_results.py
Generates detailed Ollama autoregressive reasoning results:
- Prediction distribution charts
- Confidence score analysis
- Response time metrics
- Bias type breakdown
- Agreement/disagreement analysis

**Output Files:**
- `outputs/ollama_detailed_results.png`
- `outputs/ollama_results_table.csv`
- `outputs/ollama_results_table.txt`
- `outputs/ollama_results_table_visual.png`

**Usage:**
```powershell
python scripts/generate_ollama_results.py
```

## 📈 Data Analysis Scripts

### analyze_dataset_gender.py
Analyzes the AiFairness dataset for gender-related patterns:
- Gender bias distribution
- Toxicity scores by gender mentions
- Statistical analysis
- Visualization of patterns

**Usage:**
```powershell
python scripts/analyze_dataset_gender.py
```

## 🚀 Startup Scripts

### start_web_ui.ps1
Launches the full web application (Flask backend + React frontend):
- Checks for trained models
- Starts Flask API on port 5000
- Starts React dev server on port 3000
- Opens browser automatically

**Usage:**
```powershell
.\start_web_ui.ps1
# Or from scripts folder
.\scripts\start_web_ui.ps1
```

### start_offline.ps1
Launches the application in offline mode:
- Ensures Ollama is running locally
- Starts services without internet dependency
- Uses cached models and embeddings

**Usage:**
```powershell
.\start_offline.ps1
# Or from scripts folder
.\scripts\start_offline.ps1
```

## 📝 Output Locations

All generated reports and visualizations are saved to:
```
outputs/
├── ollama_reasoning_analysis.png
├── ollama_detailed_results.png
├── ollama_results_table.csv
├── ollama_results_table.txt
├── ollama_results_table_visual.png
├── model_comparison.png
├── system_reliability.png
├── comprehensive_evaluation_report.txt
└── evaluation_metrics.json
```

## ⚙️ Configuration

Scripts use configuration from `src/config.py`:
- File paths
- Model parameters
- Toxicity threshold
- Reference texts for similarity

## 🔧 Prerequisites

**For Report Generation:**
- Python virtual environment activated
- Dependencies installed: `matplotlib`, `seaborn`, `pandas`, `numpy`
- No models required (uses simulated/test data)

**For Startup Scripts:**
- Models trained (`python main.py --mode all`)
- Ollama installed and qwen2.5:3b model pulled
- Frontend dependencies installed (`npm install` in frontend/)

## 🎯 Common Workflows

### Generate All Reports
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Generate comprehensive evaluation
python scripts/generate_comprehensive_report.py

# Generate detailed Ollama results
python scripts/generate_ollama_results.py
```

### Start Application
```powershell
# Full web UI (online)
.\start_web_ui.ps1

# Offline mode
.\start_offline.ps1
```

## 📊 Report Customization

To customize reports, edit the respective Python scripts:
- Modify test data in `test_data` dictionary
- Adjust chart colors and styles
- Change output file names
- Add new metrics or visualizations

## 🐛 Troubleshooting

**Font warnings (qt.qpa.fonts):** Safe to ignore, doesn't affect output

**UnicodeEncodeError:** Scripts use UTF-8 encoding for special characters

**Missing dependencies:** 
```powershell
pip install matplotlib seaborn pandas numpy
```

**Ollama not running:**
```powershell
ollama serve
```
