# Why Baseline Model Has 99.97% Accuracy (Label Leakage Explained)

## The Problem: Data Leakage

Your baseline model achieves **99.97% accuracy** NOT because it's a good model, but because it's **cheating** by using features that are essentially the same as the target variable.

---

## What the Baseline Model Uses

The baseline model uses **42 numeric features** from the dataset, including:

```python
Baseline Features:
├── severe_toxicity    (Correlation: 0.45)
├── obscene           (Correlation: 0.48)
├── identity_attack   (Correlation: 0.31)
├── insult            (Correlation: 0.94) ⚠️ NEARLY PERFECT!
├── threat            (Correlation: 0.21)
├── asian             (mentions of Asian identity)
├── black             (mentions of Black identity)
├── female            (mentions of female identity)
└── ... 34 more numeric columns
```

---

## The Smoking Gun: `insult` Column

**Correlation with target: 0.9434** (94.34%!)

This means:
- If `insult` score is high → target is high → model predicts "biased" ✓
- If `insult` score is low → target is low → model predicts "fair" ✓

### Why This Is Cheating:

```
Target Variable (what we predict):
  - "target" = Overall toxicity score (0.0 to 1.0)
  - Rated by human annotators
  - Represents: Is this comment toxic/biased?

Baseline Features (what model uses):
  - "insult" = Insult level score (0.0 to 1.0)
  - Rated by SAME human annotators
  - Represents: Does this comment contain insults?
```

**This is like:**
- Predicting someone's height by looking at their height measurement
- Predicting test scores by looking at the answer key
- Predicting if it's raining by checking if the ground is wet

---

## Real-World Example

### Training Data:
```
Comment: "You're an idiot and I hate you"
Features:
  - insult: 0.97 ⚠️
  - obscene: 0.10
  - severe_toxicity: 0.09
Target: 0.90 (biased)
```

### Baseline Model Logic:
```python
if insult > 0.5:
    predict "biased"  # ✓ Correct! (but cheating)
else:
    predict "fair"
```

### The Problem in Production:

When you deploy this model, you **won't have** these features!

```
New Comment: "Poor people don't understand finance"
Features available:
  - insult: ??? ← You don't know this!
  - obscene: ??? ← You don't know this!
  - severe_toxicity: ??? ← You don't know this!
```

You only have the **text**. That's why only the **embedding model matters**.

---

## Visual Comparison

### Baseline Model (99.97% accuracy):
```
[Comment Text] 
       ↓
[Human says: insult=0.94, obscene=0.48, ...]
       ↓
[Random Forest: "If insult > 0.5 → biased"]
       ↓
[Prediction] ← Uses annotations as features (CHEATING!)
```

**In production:** ❌ You don't have human annotations!

### Embedding Model (80.33% accuracy):
```
[Comment Text]
       ↓
[Sentence-BERT: Convert to 384-dim vector]
       ↓
[Random Forest: Learns patterns from embeddings]
       ↓
[Prediction] ← Only uses text (REAL MODEL!)
```

**In production:** ✓ Works with just text!

---

## Statistical Proof

Let's analyze a sample:

```python
Sample from dataset:
Comment: "haha you guys are a bunch of losers."
Target: 0.8936 (biased)

Features:
  insult: 0.8723  ← Almost identical to target!
  obscene: 0.0
  identity_attack: 0.0212
  severe_toxicity: 0.0213
```

**Baseline Model Prediction:**
- Sees `insult = 0.8723`
- Predicts: "biased" (confidence: 99%+) ✓

**Embedding Model Prediction:**
- Converts text to 384-dim vector
- Analyzes: "losers" (negative), "haha" (mocking tone)
- Predicts: "biased" (confidence: 88.7%) ✓

**On new data without annotations:**
- Baseline: ❌ Cannot work (needs insult score)
- Embedding: ✓ Still works (uses text)

---

## Why We Keep Baseline Model

Even though it's "cheating," it serves a purpose:

1. **Sanity Check**: If baseline gets 99.97%, dataset is internally consistent
2. **Feature Analysis**: Shows which annotations matter most
3. **Upper Bound**: Represents "best possible" if we had perfect annotations
4. **Comparison**: Shows embedding model (80%) is doing well considering it only uses text

---

## The Real Performance

| Model | Test Accuracy | What It Uses | Production Ready? |
|-------|---------------|--------------|-------------------|
| Baseline | 99.97% | Human annotations (insult, obscene, etc.) | ❌ NO - Data leakage |
| Embedding | 80.33% | Only text (Sentence-BERT) | ✅ YES - Real model |

**The 80.33% is your ACTUAL performance.**

---

## How to Verify Label Leakage

Run this test:

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv('fairness_dataset.csv')

# Test 1: Baseline with all features (current)
X = df.select_dtypes(include=['number']).drop('target', axis=1)
y = (df['target'] >= 0.5).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(f"With insult column: {model.score(X_test, y_test):.4f}")  # 99.97%

# Test 2: Remove leakage features
X_clean = X.drop(['insult', 'obscene', 'severe_toxicity', 'identity_attack', 'threat'], axis=1, errors='ignore')
X_train_clean, X_test_clean, _, _ = train_test_split(X_clean, y, test_size=0.2, random_state=42)

model_clean = RandomForestClassifier(n_estimators=100, random_state=42)
model_clean.fit(X_train_clean, y_train)
print(f"Without leakage: {model_clean.score(X_test_clean, y_test):.4f}")  # Much lower!
```

---

## Conclusion

**Q: How can baseline accuracy be so high?**

**A: Label leakage.** The baseline model uses the `insult` column which has 0.94 correlation with the target. It's like predicting if someone is tall by measuring their height.

**The embedding model (80.33%) is your REAL performance** because it's the only one that works with just text in production.

**The gap (99.97% → 80.33%)** represents the difficulty of predicting toxicity from text alone vs. using human annotations.

---

## Recommendations

1. ✅ **Use embedding model for production** (already implemented in API)
2. ✅ **Report 80.33% as actual accuracy** (not 99.97%)
3. 🔄 **Remove baseline model from evaluation report** (it's misleading)
4. 🔄 **Focus on improving embedding model** to 85-90% accuracy
5. 🔄 **Add more diverse training data** (subtle bias examples)

The baseline model is useful for research/analysis but **never deploy it to production**.
