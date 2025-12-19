"""
Error Analysis Script
Analyzes model predictions to identify failure patterns.
"""
import pandas as pd
import numpy as np
import joblib
from preprocessing import load_and_clean_data, split_data_for_embeddings
from config import EMBEDDING_MODEL_PATH, EMBEDDINGS_TEST_PATH, TOXICITY_THRESHOLD

def load_test_data():
    """Load test embeddings and labels"""
    # Load full embeddings
    train_embeddings = np.load('embeddings/train_embeddings.npy')
    test_embeddings = np.load('embeddings/test_embeddings.npy')
    
    # Load dataset to get text
    df = load_and_clean_data()
    text_data = df['comment_text'].fillna('')
    labels = df['target']
    
    # Split indices same way as training to align with saved embeddings
    from sklearn.model_selection import train_test_split
    from config import TEST_SIZE, RANDOM_STATE
    
    train_idx, test_idx = train_test_split(
        range(len(df)),
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )
    
    # Get test texts and labels
    test_texts = text_data.iloc[test_idx].values
    y_test_continuous = labels.iloc[test_idx].values
    y_test_binary = (y_test_continuous >= TOXICITY_THRESHOLD).astype(int)
    
    return test_embeddings, y_test_binary, test_texts, y_test_continuous

def analyze_errors():
    """Analyze model errors"""
    print("="*80)
    print("MODEL ERROR ANALYSIS")
    print("="*80)
    
    # Load model
    print("\nLoading model...")
    model = joblib.load(EMBEDDING_MODEL_PATH)
    
    # Load test data
    print("Loading test data...")
    X_test, y_test, test_texts, y_test_continuous = load_test_data()
    
    # Make predictions
    print("Making predictions...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # Find errors
    errors = y_pred != y_test
    n_errors = errors.sum()
    accuracy = (y_pred == y_test).mean()
    
    print(f"\n{'='*80}")
    print(f"OVERALL PERFORMANCE")
    print(f"{'='*80}")
    print(f"Total test samples: {len(y_test)}")
    print(f"Correct predictions: {(~errors).sum()} ({(~errors).mean()*100:.2f}%)")
    print(f"Wrong predictions: {n_errors} ({(errors).mean()*100:.2f}%)")
    print(f"Accuracy: {accuracy:.4f}")
    
    # Analyze false positives (predicted biased, actually fair)
    false_positives = (y_pred == 1) & (y_test == 0)
    n_fp = false_positives.sum()
    
    # Analyze false negatives (predicted fair, actually biased)
    false_negatives = (y_pred == 0) & (y_test == 1)
    n_fn = false_negatives.sum()
    
    print(f"\n{'='*80}")
    print(f"ERROR BREAKDOWN")
    print(f"{'='*80}")
    print(f"False Positives (predicted biased, actually fair): {n_fp} ({n_fp/n_errors*100:.1f}% of errors)")
    print(f"False Negatives (predicted fair, actually biased): {n_fn} ({n_fn/n_errors*100:.1f}% of errors)")
    
    # Show worst false negatives (biased comments predicted as fair)
    print(f"\n{'='*80}")
    print(f"WORST FALSE NEGATIVES (Biased predicted as Fair - High Confidence)")
    print(f"{'='*80}")
    fn_indices = np.where(false_negatives)[0]
    if len(fn_indices) > 0:
        fn_confidences = 1 - y_prob[fn_indices]  # Confidence in "fair" prediction
        top_fn = fn_indices[np.argsort(-fn_confidences)[:10]]
        
        for i, idx in enumerate(top_fn, 1):
            print(f"\n{i}. Target: {y_test_continuous[idx]:.3f} | Predicted: fair ({(1-y_prob[idx])*100:.1f}% conf)")
            print(f"   Text: {test_texts[idx][:200]}...")
    
    # Show worst false positives (fair comments predicted as biased)
    print(f"\n{'='*80}")
    print(f"WORST FALSE POSITIVES (Fair predicted as Biased - High Confidence)")
    print(f"{'='*80}")
    fp_indices = np.where(false_positives)[0]
    if len(fp_indices) > 0:
        fp_confidences = y_prob[fp_indices]  # Confidence in "biased" prediction
        top_fp = fp_indices[np.argsort(-fp_confidences)[:10]]
        
        for i, idx in enumerate(top_fp, 1):
            print(f"\n{i}. Target: {y_test_continuous[idx]:.3f} | Predicted: biased ({y_prob[idx]*100:.1f}% conf)")
            print(f"   Text: {test_texts[idx][:200]}...")
    
    # Analyze confidence distribution
    print(f"\n{'='*80}")
    print(f"CONFIDENCE ANALYSIS")
    print(f"{'='*80}")
    
    correct_conf = y_prob[~errors].mean()
    incorrect_conf = y_prob[errors].mean()
    
    print(f"Average confidence on correct predictions: {correct_conf:.3f}")
    print(f"Average confidence on incorrect predictions: {incorrect_conf:.3f}")
    
    # Low confidence predictions
    low_conf = (np.abs(y_prob - 0.5) < 0.2)  # Within 0.3-0.7 range
    print(f"\nLow confidence predictions (<0.3 or >0.7): {low_conf.sum()} ({low_conf.mean()*100:.1f}%)")
    print(f"Accuracy on low confidence: {(y_pred[low_conf] == y_test[low_conf]).mean():.3f}")
    print(f"Accuracy on high confidence: {(y_pred[~low_conf] == y_test[~low_conf]).mean():.3f}")
    
    print(f"\n{'='*80}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    analyze_errors()
