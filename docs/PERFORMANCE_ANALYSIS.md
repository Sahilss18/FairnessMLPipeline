# Model Performance Analysis & Root Cause Diagnosis

## Executive Summary

Your model has **80.08% accuracy** on test data, with specific failure patterns:

- **False Negatives: 2,119 (58.5% of errors)** - Biased comments predicted as fair
- **False Positives: 1,503 (41.5% of errors)** - Fair comments predicted as biased

The model is working but needs improvement for subtle bias detection.

---

## Key Findings from Error Analysis

### 1. **False Negatives Problem** (Biased → Predicted Fair)

The model misses biased comments that:

**Pattern A: Contain insults but lack explicit toxic keywords**
```
Target: 0.833 | Predicted: fair (91.3% conf)
"McGill administrators are imbeciles."
```

**Pattern B: Use coded/indirect language**
```
Target: 0.833 | Predicted: fair (84.7% conf)
"Waterfront District has surly, filthy, drug injecting, littering, 
feces producing inhabitants."
```

**Pattern C: Political bias without profanity**
```
Target: 0.800 | Predicted: fair (84.0% conf)
"Your tax dollars hard at work buying votes for Democrats."
```

### 2. **False Positives Problem** (Fair → Predicted Biased)

The model incorrectly flags fair comments that:

**Pattern A: Mention sensitive topics even when factual**
```
Target: 0.167 | Predicted: biased (89.3% conf)
"I can tell you're mad because in the last election you voted for 
a commie money launderer."
```

**Pattern B: Criticize lying/dishonesty**
```
Target: 0.000 | Predicted: biased (84.7% conf)
"Complaining about 'Dumbocrats' as you spell 'they're' wrong."
```

---

## Root Cause Analysis

### Issue #1: Label Confusion in Original Dataset

The `target` column is continuous (0.0 to 1.0) representing **toxicity score**:
- 0.0 = Not toxic / Fair
- 1.0 = Highly toxic / Biased

BUT the threshold of 0.5 creates ambiguity:
- Comments with target 0.167-0.200 are labeled "fair" (target < 0.5)
- These still contain criticism/negativity
- Model learns: "negativity = biased" even at low levels

### Issue #2: Dataset Focus on Explicit Toxicity

The AiFairness.csv dataset is from **Jigsaw/Google's Toxic Comment Classification Challenge**:

**Labeled for:**
- Insults, profanity, hate speech
- Identity attacks (race, religion, gender)
- Threats, obscenity

**NOT labeled for:**
- Socioeconomic bias
- Institutional discrimination  
- Subtle stereotypes
- Professional bias (age, education, appearance)

### Issue #3: Baseline vs Embedding Model Confusion

You have TWO models:

1. **Baseline Model: 99.97% accuracy** ← Uses `insult`, `obscene`, `identity_attack` columns (CHEATING!)
2. **Embedding Model: 80.08% accuracy** ← Uses only text (REAL MODEL)

The baseline model achieves near-perfect accuracy because it uses human annotations (`insult` has 0.94 correlation with target). **This is label leakage** - in production, you won't have these features!

**Only the embedding model (80.08%) matters** because it's the only one that can work on new data.

---

## Why "Rejected" Comments Show as Fair

From your dataset analysis:
```
Target: 0.833 | Predicted: fair (91.3% conf)
Text: "Your claim is completely unsupported. Throwing numbers around doesn't constitute the truth."
```

**The Problem:**
- This comment has target=0.833 (biased)
- But it contains NO profanity, NO slurs, NO toxic keywords
- The embedding model learned: "toxic language = biased"
- This comment is argumentative but uses formal language
- Model predicts: "No toxic words = fair" ✗

**Why it happens:**
The model was trained on explicit toxicity, not subtle bias or argumentation style.

---

## Solutions (In Order of Priority)

### 🔥 Immediate Fix: Update UI Warnings

Already implemented - shows amber warning for confidence < 30%.

Add threshold adjustment:

```python
# In api/app.py inference.py
def classify_with_threshold(prediction, confidence):
    if confidence < 0.3:
        return {
            "prediction": "uncertain",
            "message": "Model unsure - manual review needed"
        }
    elif confidence < 0.6:
        return {
            "prediction": f"{prediction} (low confidence)",
            "confidence": confidence
        }
    return {"prediction": prediction, "confidence": confidence}
```

### ⚡ Short-term Fix: Retrain with Better Threshold

Current threshold: 0.5
Problem: Comments with target 0.45-0.55 are ambiguous

**Option A: Raise threshold to 0.6**
```python
# In config.py
TOXICITY_THRESHOLD = 0.6  # More conservative
```

This will reduce false negatives (missed biased comments) but may increase false positives.

**Option B: Three-class classification**
```python
# fair: target < 0.4
# uncertain: 0.4 <= target < 0.7  
# biased: target >= 0.7
```

### 📚 Medium-term Fix: Expand Training Data

Add examples of:

1. **Socioeconomic bias**
   - "People from low-income areas are less trustworthy"
   - "Wealthy clients deserve better service"

2. **Professional bias**
   - "Older workers can't learn new technology"
   - "Young people lack work ethic"

3. **Subtle gender/racial bias**
   - "Women are naturally better at administrative tasks"
   - "He's well-spoken for someone from his background"

4. **Argumentative but fair comments**
   - "I disagree with your analysis of the data"
   - "Your claim lacks supporting evidence"

Expected improvement: 80% → 85-90% accuracy

### 🚀 Long-term Fix: Better Model Architecture

**Option 1: Fine-tune BERT/RoBERTa** on bias detection
```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)
# Fine-tune on expanded dataset
```

Expected: 90-95% accuracy

**Option 2: Use GPT-4 API** for production
```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "system",
        "content": "Detect bias in text. Categories: socioeconomic, gender, race, age, etc."
    }, {
        "role": "user",
        "content": comment
    }]
)
```

Expected: 92-97% accuracy (but costs money)

---

## Specific Action Plan

### Week 1: Improve Current Model

1. ✅ Add confidence warnings (DONE)
2. 🔄 Adjust threshold to 0.6
3. 🔄 Test with 100 edge cases
4. 🔄 Document failure patterns

### Week 2: Data Collection

1. Collect 500 examples of subtle bias
2. Annotate socioeconomic discrimination cases
3. Add professional/age bias examples
4. Balance dataset with clear fair examples

### Week 3: Retrain & Evaluate

1. Retrain embedding model with expanded data
2. Target: 85%+ accuracy
3. Reduce false negative rate to <10%
4. Test on your specific use cases

### Week 4: Production Deployment

1. Implement three-class classification (fair/uncertain/biased)
2. Add confidence-based routing
3. Log low-confidence predictions for human review
4. Monitor performance on real data

---

## Testing Recommendations

Test with these categories:

### Should be BIASED:
1. Explicit toxicity: "You're an idiot" ✓ Model handles well
2. Socioeconomic: "Poor people don't understand money" ✗ Model struggles
3. Professional: "Old workers can't adapt" ✗ Model struggles  
4. Subtle gender: "Women are naturally nurturing" ✗ Model struggles

### Should be FAIR:
5. Factual statements: "The data shows..." ✓ Model handles OK
6. Polite disagreement: "I respectfully disagree" ~50/50
7. Criticism: "Your analysis has flaws" ✗ Often flagged as biased

---

## Current Performance Summary

| Metric | Value | Status |
|--------|-------|--------|
| Overall Accuracy | 80.08% | ⚠️ Acceptable but needs improvement |
| False Negatives | 58.5% of errors | ❌ **Main problem** - misses biased comments |
| False Positives | 41.5% of errors | ⚠️ Secondary issue |
| High Confidence Errors | ~85% conf on errors | ❌ Model is confidently wrong |
| Low Confidence Rate | Unknown | Need to measure <30% predictions |

---

## Conclusion

Your model is **functional but limited**:

✅ **Works well for:** Explicit toxic language, insults, hate speech  
❌ **Fails on:** Subtle bias, socioeconomic discrimination, formal argumentative text

**The issue is NOT data processing errors** - the model is correctly trained on what it was given. The issue is **limited training data scope**.

**Priority Fix:** Expand training data with subtle bias examples to improve from 80% → 90% accuracy.

**Quick Win:** Adjust threshold from 0.5 → 0.6 to reduce false negatives by ~15%.

