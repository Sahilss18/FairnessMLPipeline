# Dataset Information

## Required Dataset: fairness_dataset.csv

This project requires a fairness dataset with the following structure:

### Required Columns

1. **comment_text** (string)
   - Text content to analyze for bias
   - Can contain any natural language text
   - Missing values will be filled with empty strings

2. **target** (float)
   - Toxicity or bias score
   - Range: 0.0 (fair/non-toxic) to 1.0 (toxic/biased)
   - Values >= 0.5 are classified as toxic
   - Missing values will be filled with 0

3. **Numeric features** (optional)
   - Additional numeric columns for baseline model
   - Examples: severe_toxicity, obscene, threat, insult, identity_attack
   - Missing values will be filled with 0

4. **Categorical features** (optional)
   - Additional categorical columns
   - Missing values will be filled with 'Unknown'

### Example Dataset Structure

```csv
comment_text,target,severe_toxicity,obscene,threat,insult,identity_attack
"Everyone deserves respect.",0.05,0.0,0.0,0.0,0.0,0.0
"You are so stupid!",0.92,0.7,0.8,0.2,0.9,0.1
"People from that group are lazy.",0.88,0.6,0.3,0.1,0.7,0.9
"Great work! Thanks for sharing.",0.02,0.0,0.0,0.0,0.0,0.0
```

### Recommended Datasets

If you don't have a dataset, consider these public sources:

1. **Jigsaw Toxic Comment Classification**
   - Source: Kaggle
   - URL: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
   - Contains ~160k comments with toxicity labels

2. **Civil Comments Dataset**
   - Source: Kaggle / UCI
   - Contains comments with toxicity and demographic annotations

3. **Wikipedia Talk Corpus**
   - Source: Figshare
   - Contains discussions labeled for personal attacks

### Data Preparation

If your dataset has different column names:

1. Rename text column to `comment_text`
2. Rename target column to `target`
3. Ensure target is numeric (0-1 range preferred)
4. Save as CSV in `data/fairness_dataset.csv`

### Minimum Requirements

- At least 1000 samples recommended
- Balanced classes preferred (but not required)
- Text should be in English (model is English-trained)
- Target labels should be reliable

### Privacy and Ethics

- Ensure dataset usage complies with terms of service
- Do not include personally identifiable information
- Consider ethical implications of labeling decisions
- Respect original data licenses

## Placement

Place your prepared dataset at:
```
data/fairness_dataset.csv
```

The project will automatically load and preprocess it when you run:
```powershell
python main.py --mode all
```
