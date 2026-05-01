"""
Calculate Fairness Metrics for Bias Detection Models
Computes Demographic Parity Difference (DPD) and Disparate Impact (DI)
for Phase II (SBERT+RF) and Phase III (Ollama) models
"""

import pandas as pd
import numpy as np
import sys
import os
import pickle
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from inference import BiasDetector
from config import DATASET_PATH, TOXICITY_THRESHOLD

# Checkpoint directory
CHECKPOINT_DIR = Path('outputs/fairness_checkpoints')
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

def load_test_data():
    """Load test dataset with protected attributes"""
    print("Loading dataset...")
    # Handle encoding issues in the dataset
    df = pd.read_csv(DATASET_PATH, encoding='latin-1')
    
    # Convert continuous toxicity to binary
    df['binary_label'] = (df['target'] >= TOXICITY_THRESHOLD).astype(int)
    
    # Use 20% as test set (same as training split)
    test_size = int(len(df) * 0.2)
    test_df = df.tail(test_size).copy()
    
    print(f"Loaded {len(test_df)} test samples")
    return test_df

def define_protected_groups(df):
    """
    Define protected groups based on identity columns
    Returns samples belonging to each protected group (using integer positions)
    """
    protected_groups = {}
    
    # Gender-based groups (using 0.5 threshold for identity presence)
    protected_groups['female'] = np.where(df['female'].values > 0.5)[0]
    protected_groups['male'] = np.where(df['male'].values > 0.5)[0]
    
    # Race/ethnicity groups
    protected_groups['black'] = np.where(df['black'].values > 0.5)[0]
    protected_groups['white'] = np.where(df['white'].values > 0.5)[0]
    protected_groups['asian'] = np.where(df['asian'].values > 0.5)[0]
    protected_groups['latino'] = np.where(df['latino'].values > 0.5)[0]
    
    # Religion groups
    protected_groups['muslim'] = np.where(df['muslim'].values > 0.5)[0]
    protected_groups['christian'] = np.where(df['christian'].values > 0.5)[0]
    protected_groups['jewish'] = np.where(df['jewish'].values > 0.5)[0]
    
    # Sexual orientation
    protected_groups['homosexual'] = np.where(df['homosexual_gay_or_lesbian'].values > 0.5)[0]
    protected_groups['heterosexual'] = np.where(df['heterosexual'].values > 0.5)[0]
    
    # Remove empty groups
    protected_groups = {k: v for k, v in protected_groups.items() if len(v) > 0}
    
    print("\nProtected group sizes:")
    for group, indices in protected_groups.items():
        print(f"  {group}: {len(indices)} samples")
    
    return protected_groups

def calculate_demographic_parity_difference(predictions, protected_groups, group_a, group_b):
    """
    Calculate Demographic Parity Difference (DPD)
    
    DPD = P(Y_hat=1 | A=privileged) - P(Y_hat=1 | A=unprivileged)
    
    Fair if DPD ≈ 0 (ideally -0.1 to 0.1)
    """
    if group_a not in protected_groups or group_b not in protected_groups:
        return None
    
    idx_a = protected_groups[group_a]
    idx_b = protected_groups[group_b]
    
    if len(idx_a) == 0 or len(idx_b) == 0:
        return None
    
    # Convert indices to array positions
    idx_a = np.array(list(idx_a))
    idx_b = np.array(list(idx_b))
    
    # Positive prediction rate for each group
    rate_a = predictions[idx_a].mean()
    rate_b = predictions[idx_b].mean()
    
    dpd = rate_a - rate_b
    
    return dpd

def calculate_disparate_impact(predictions, protected_groups, group_a, group_b):
    """
    Calculate Disparate Impact (DI)
    
    DI = P(Y_hat=1 | A=unprivileged) / P(Y_hat=1 | A=privileged)
    
    Fair if 0.8 ≤ DI ≤ 1.25 (80% rule)
    """
    if group_a not in protected_groups or group_b not in protected_groups:
        return None
    
    idx_a = protected_groups[group_a]
    idx_b = protected_groups[group_b]
    
    if len(idx_a) == 0 or len(idx_b) == 0:
        return None
    
    # Convert indices to array positions
    idx_a = np.array(list(idx_a))
    idx_b = np.array(list(idx_b))
    
    rate_a = predictions[idx_a].mean()
    rate_b = predictions[idx_b].mean()
    
    # Avoid division by zero
    if rate_a == 0:
        return None
    
    di = rate_b / rate_a
    
    return di

def run_phase_ii_predictions(detector, test_df):
    """Run Phase II (SBERT + RF) predictions on test set"""
    checkpoint_file = CHECKPOINT_DIR / 'phase_ii_predictions.npy'
    
    # Check if checkpoint exists
    if checkpoint_file.exists():
        print("\n" + "="*70)
        print("Loading Phase II predictions from checkpoint...")
        print("="*70)
        predictions = np.load(checkpoint_file)
        print(f"✅ Loaded {len(predictions)} predictions from checkpoint")
        return predictions
    
    print("\n" + "="*70)
    print("Running Phase II (SBERT + Random Forest) Predictions...")
    print("="*70)
    
    predictions = []
    
    for idx, row in test_df.iterrows():
        comment = row['comment_text']
        try:
            result = detector.analyze_comment(comment, use_ollama=False)
            predictions.append(result['prediction'])
        except Exception as e:
            print(f"Error on index {idx}: {e}")
            predictions.append(0)  # Default to fair if error
        
        if (len(predictions) % 1000) == 0:
            print(f"Processed {len(predictions)} / {len(test_df)} samples...")
    
    predictions = np.array(predictions)
    
    # Save checkpoint
    np.save(checkpoint_file, predictions)
    print(f"\n✅ Saved Phase II predictions to {checkpoint_file}")
    
    return predictions

def run_phase_iii_predictions(detector, test_df, sample_size=500):
    """
    Run Phase III (Ollama) predictions on a sample
    (Full test set would take too long with Ollama)
    """
    checkpoint_file = CHECKPOINT_DIR / 'phase_iii_predictions.pkl'
    
    # Check if checkpoint exists
    if checkpoint_file.exists():
        print("\n" + "="*70)
        print("Loading Phase III predictions from checkpoint...")
        print("="*70)
        with open(checkpoint_file, 'rb') as f:
            checkpoint_data = pickle.load(f)
        predictions = checkpoint_data['predictions']
        sampled_positions = checkpoint_data['sampled_positions']
        print(f"✅ Loaded {len(sampled_positions)} Ollama predictions from checkpoint")
        return predictions, sampled_positions
    
    print("\n" + "="*70)
    print(f"Running Phase III (Ollama) Predictions on {sample_size} samples...")
    print("="*70)
    
    # Sample for Ollama (full test set would take hours)
    sampled_df = test_df.sample(n=min(sample_size, len(test_df)), random_state=42)
    
    predictions = []
    
    for idx, row in sampled_df.iterrows():
        comment = row['comment_text']
        try:
            result = detector.analyze_comment(comment, use_ollama=True)
            # Use Ollama's prediction if available, otherwise fall back to baseline
            if 'ollama_reasoning' in result and result['ollama_reasoning'].get('available'):
                pred = result['ollama_reasoning'].get('ollama_prediction', result['prediction'])
            else:
                pred = result['prediction']
            predictions.append(pred)
        except Exception as e:
            print(f"Error on index {idx}: {e}")
            predictions.append(0)
        
        if (len(predictions) % 50) == 0:
            print(f"Processed {len(predictions)} / {len(sampled_df)} samples...")
            # Save intermediate checkpoint every 50 samples
            intermediate_checkpoint = {
                'predictions': np.zeros(len(test_df)),
                'sampled_positions': np.array([]),
                'partial': True,
                'completed': len(predictions)
            }
            with open(checkpoint_file, 'wb') as f:
                pickle.dump(intermediate_checkpoint, f)
    
    # Create full-size array with predictions mapped back to original indices
    full_predictions = np.zeros(len(test_df))
    for i, orig_idx in enumerate(sampled_df.index):
        # Find position in test_df
        test_pos = test_df.index.get_loc(orig_idx)
        full_predictions[test_pos] = predictions[i]
    
    # Return positions (0-based) that were sampled
    sampled_positions = np.array([test_df.index.get_loc(idx) for idx in sampled_df.index])
    
    # Save final checkpoint
    checkpoint_data = {
        'predictions': full_predictions,
        'sampled_positions': sampled_positions,
        'partial': False,
        'completed': len(predictions)
    }
    with open(checkpoint_file, 'wb') as f:
        pickle.dump(checkpoint_data, f)
    print(f"\n✅ Saved Phase III predictions to {checkpoint_file}")
    
    return full_predictions, sampled_positions

def generate_fairness_report(test_df, phase_ii_preds, phase_iii_preds, phase_iii_indices):
    """Generate comprehensive fairness metrics report"""
    
    protected_groups = define_protected_groups(test_df)
    
    # Define comparison pairs (privileged vs unprivileged)
    comparisons = [
        ('male', 'female', 'Gender'),
        ('white', 'black', 'Race (White vs Black)'),
        ('white', 'asian', 'Race (White vs Asian)'),
        ('white', 'latino', 'Race (White vs Latino)'),
        ('christian', 'muslim', 'Religion (Christian vs Muslim)'),
        ('heterosexual', 'homosexual', 'Sexual Orientation'),
    ]
    
    print("\n" + "="*70)
    print("FAIRNESS METRICS COMPARISON")
    print("="*70)
    
    results = []
    
    for privileged, unprivileged, category in comparisons:
        if privileged not in protected_groups or unprivileged not in protected_groups:
            continue
        
        print(f"\n{category} ({privileged} vs {unprivileged}):")
        print("-" * 60)
        
        # Phase II metrics (full test set)
        dpd_ii = calculate_demographic_parity_difference(
            phase_ii_preds, protected_groups, privileged, unprivileged
        )
        di_ii = calculate_disparate_impact(
            phase_ii_preds, protected_groups, privileged, unprivileged
        )
        
        # Phase III metrics (sampled data only)
        # Map sampled indices to array positions
        sample_positions = {idx: i for i, idx in enumerate(test_df.index) if i in phase_iii_indices}
        phase_iii_protected = {}
        for k, v in protected_groups.items():
            # Only include positions that are in the sampled set
            sampled_v = np.array([pos for pos in v if pos in phase_iii_indices])
            if len(sampled_v) > 0:
                phase_iii_protected[k] = sampled_v
        
        dpd_iii = calculate_demographic_parity_difference(
            phase_iii_preds, phase_iii_protected, privileged, unprivileged
        )
        di_iii = calculate_disparate_impact(
            phase_iii_preds, phase_iii_protected, privileged, unprivileged
        )
        
        if dpd_ii is not None and di_ii is not None:
            print(f"  Phase II (SBERT + RF):")
            print(f"    DPD: {dpd_ii:+.4f}  {'✓ Fair' if abs(dpd_ii) < 0.1 else '✗ Unfair'}")
            print(f"    DI:  {di_ii:.4f}   {'✓ Fair' if 0.8 <= di_ii <= 1.25 else '✗ Unfair'}")
        
        if dpd_iii is not None and di_iii is not None:
            print(f"  Phase III (Ollama):")
            print(f"    DPD: {dpd_iii:+.4f}  {'✓ Fair' if abs(dpd_iii) < 0.1 else '✗ Unfair'}")
            print(f"    DI:  {di_iii:.4f}   {'✓ Fair' if 0.8 <= di_iii <= 1.25 else '✗ Unfair'}")
        
        results.append({
            'Category': category,
            'Privileged': privileged,
            'Unprivileged': unprivileged,
            'Phase_II_DPD': dpd_ii,
            'Phase_II_DI': di_ii,
            'Phase_III_DPD': dpd_iii,
            'Phase_III_DI': di_iii
        })
    
    # Generate summary table
    print("\n" + "="*70)
    print("TABLE 2: FAIRNESS METRICS COMPARISON")
    print("="*70)
    print("\nModel                    | Avg DPD  | Avg DI   | Fair Groups")
    print("-" * 70)
    
    df_results = pd.DataFrame(results)
    
    phase_ii_avg_dpd = df_results['Phase_II_DPD'].abs().mean()
    phase_ii_avg_di = df_results['Phase_II_DI'].mean()
    phase_ii_fair = ((df_results['Phase_II_DPD'].abs() < 0.1) & 
                     (df_results['Phase_II_DI'] >= 0.8) & 
                     (df_results['Phase_II_DI'] <= 1.25)).sum()
    
    phase_iii_avg_dpd = df_results['Phase_III_DPD'].abs().mean()
    phase_iii_avg_di = df_results['Phase_III_DI'].mean()
    phase_iii_fair = ((df_results['Phase_III_DPD'].abs() < 0.1) & 
                      (df_results['Phase_III_DI'] >= 0.8) & 
                      (df_results['Phase_III_DI'] <= 1.25)).sum()
    
    print(f"Phase II (SBERT + ML)    | {phase_ii_avg_dpd:+.4f}  | {phase_ii_avg_di:.4f}  | {phase_ii_fair}/{len(results)}")
    print(f"Phase III (Ollama)       | {phase_iii_avg_dpd:+.4f}  | {phase_iii_avg_di:.4f}  | {phase_iii_fair}/{len(results)}")
    
    print("\n" + "="*70)
    print("FAIRNESS INTERPRETATION")
    print("="*70)
    print("DPD (Demographic Parity Difference):")
    print("  • Fair if |DPD| < 0.1")
    print("  • Closer to 0 = more fair")
    print("  • Negative = unprivileged group gets more positive predictions")
    print("\nDI (Disparate Impact):")
    print("  • Fair if 0.8 ≤ DI ≤ 1.25 (80% rule)")
    print("  • 1.0 = perfect parity")
    print("  • <0.8 = discrimination against unprivileged")
    print("  • >1.25 = discrimination against privileged")
    
    # Save to CSV
    output_file = 'outputs/fairness_metrics_comparison.csv'
    df_results.to_csv(output_file, index=False)
    print(f"\n✅ Detailed results saved to: {output_file}")
    
    return df_results

def main():
    # Initialize detector
    print("Initializing Bias Detector...")
    from config import EMBEDDING_MODEL_PATH, SENTENCE_TRANSFORMER_MODEL
    detector = BiasDetector(
        model_path=EMBEDDING_MODEL_PATH,
        embedder_name=SENTENCE_TRANSFORMER_MODEL
    )
    
    # Load test data
    test_df = load_test_data()
    
    # Run Phase II predictions
    phase_ii_preds = run_phase_ii_predictions(detector, test_df)
    
    # Run Phase III predictions (sampled)
    phase_iii_preds, phase_iii_indices = run_phase_iii_predictions(detector, test_df, sample_size=500)
    
    # Generate fairness report
    results_df = generate_fairness_report(test_df, phase_ii_preds, phase_iii_preds, phase_iii_indices)
    
    print("\n✅ Fairness evaluation complete!")

if __name__ == "__main__":
    main()
