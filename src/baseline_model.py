"""
Phase 1: Baseline Model Training
Trains a Random Forest classifier on numeric features to establish baseline performance.
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import numpy as np

from config import BASELINE_CONFIG, BASELINE_MODEL_PATH, OUTPUTS_DIR
from utils import save_model, plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from preprocessing import load_and_clean_data, prepare_baseline_data
import os


def train_baseline_model(X_train, y_train):
    """
    Train a Random Forest classifier on numeric features.
    
    Args:
        X_train: Training features
        y_train: Training labels
        
    Returns:
        Trained model
    """
    print("\n" + "="*70)
    print("PHASE 1: TRAINING BASELINE MODEL")
    print("="*70)
    
    rf = RandomForestClassifier(**BASELINE_CONFIG)
    print(f"\nTraining Random Forest with {BASELINE_CONFIG['n_estimators']} estimators...")
    rf.fit(X_train, y_train)
    print("Training complete.")
    
    return rf


def evaluate_baseline_model(model, X_test, y_test, save_plots=True):
    """
    Evaluate the baseline model and generate visualizations.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        save_plots: Whether to save plots to disk
        
    Returns:
        dict: Dictionary containing evaluation metrics
    """
    print("\nEvaluating baseline model...")
    
    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    
    print(f"\nBaseline Model Performance:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  ROC-AUC:  {roc_auc:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Visualizations
    if save_plots:
        cm_path = os.path.join(OUTPUTS_DIR, 'baseline_confusion_matrix.png')
        roc_path = os.path.join(OUTPUTS_DIR, 'baseline_roc_curve.png')
        pr_path = os.path.join(OUTPUTS_DIR, 'baseline_precision_recall.png')
        
        plot_confusion_matrix(y_test, y_pred, 
                            title='Confusion Matrix - Baseline Model',
                            save_path=cm_path)
        plot_roc_curve(y_test, y_proba, 
                      title='ROC Curve - Baseline Model',
                      save_path=roc_path)
        plot_precision_recall_curve(y_test, y_proba,
                                   title='Precision-Recall Curve - Baseline Model',
                                   save_path=pr_path)
    
    return {
        'accuracy': accuracy,
        'roc_auc': roc_auc,
        'y_pred': y_pred,
        'y_proba': y_proba
    }


def train_and_compare_model_sizes(X_train, X_test, y_train, y_test):
    """
    Train models with different numbers of estimators to compare performance.
    
    Args:
        X_train, X_test, y_train, y_test: Training and testing data
    """
    print("\n" + "="*70)
    print("COMPARING MODEL SIZES")
    print("="*70)
    
    estimators = [10, 50, 100, 200]
    train_auc = []
    test_auc = []
    
    for n in estimators:
        print(f"\nTraining model with {n} estimators...")
        rf_model = RandomForestClassifier(n_estimators=n, random_state=42, n_jobs=-1)
        rf_model.fit(X_train, y_train)
        
        # Predict probabilities
        y_train_pred = rf_model.predict_proba(X_train)[:, 1]
        y_test_pred = rf_model.predict_proba(X_test)[:, 1]
        
        # Calculate AUC scores
        train_auc_score = roc_auc_score(y_train, y_train_pred)
        test_auc_score = roc_auc_score(y_test, y_test_pred)
        
        train_auc.append(train_auc_score)
        test_auc.append(test_auc_score)
        
        print(f"  Train AUC: {train_auc_score:.4f}, Test AUC: {test_auc_score:.4f}")
    
    # Plot comparison
    from utils import plot_train_vs_test_auc
    save_path = os.path.join(OUTPUTS_DIR, 'baseline_model_size_comparison.png')
    plot_train_vs_test_auc(estimators, train_auc, test_auc, 
                          title='Train vs Test AUC - Baseline Model',
                          save_path=save_path)


def run_baseline_phase(save_model_flag=True, compare_sizes=False):
    """
    Execute the complete baseline model pipeline.
    
    Args:
        save_model_flag: Whether to save the trained model
        compare_sizes: Whether to compare different model sizes
        
    Returns:
        dict: Results including model and metrics
    """
    # Load and prepare data
    df = load_and_clean_data()
    X_train, X_test, y_train, y_test = prepare_baseline_data(df)
    
    # Train model
    model = train_baseline_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_baseline_model(model, X_test, y_test, save_plots=True)
    
    # Optional: Compare model sizes
    if compare_sizes:
        train_and_compare_model_sizes(X_train, X_test, y_train, y_test)
    
    # Save model
    if save_model_flag:
        save_model(model, BASELINE_MODEL_PATH)
    
    print("\n" + "="*70)
    print("PHASE 1 COMPLETE")
    print("="*70 + "\n")
    
    return {
        'model': model,
        'metrics': metrics,
        'test_data': (X_test, y_test)
    }


if __name__ == "__main__":
    results = run_baseline_phase(save_model_flag=True, compare_sizes=True)
    print("Baseline model training and evaluation completed successfully.")
