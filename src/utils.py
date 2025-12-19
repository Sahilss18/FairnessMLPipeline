"""
Utility functions for the Fairness and Bias Detection System.
"""
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve


def ensure_dir_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_model(model, filepath):
    """Save a trained model to disk."""
    ensure_dir_exists(os.path.dirname(filepath))
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to: {filepath}")


def load_model(filepath):
    """Load a trained model from disk."""
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded from: {filepath}")
    return model


def save_embeddings(embeddings, filepath):
    """Save embeddings as numpy array."""
    ensure_dir_exists(os.path.dirname(filepath))
    np.save(filepath, embeddings)
    print(f"Embeddings saved to: {filepath}")


def load_embeddings(filepath):
    """Load embeddings from numpy file."""
    embeddings = np.load(filepath)
    print(f"Embeddings loaded from: {filepath}")
    return embeddings


def plot_confusion_matrix(y_true, y_pred, title='Confusion Matrix', save_path=None):
    """Plot confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(title)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    
    if save_path:
        ensure_dir_exists(os.path.dirname(save_path))
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Plot saved to: {save_path}")
    
    plt.show()


def plot_roc_curve(y_true, y_proba, title='ROC Curve', save_path=None):
    """Plot ROC curve."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.grid(True)
    
    if save_path:
        ensure_dir_exists(os.path.dirname(save_path))
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Plot saved to: {save_path}")
    plt.close()
    return roc_auc


def plot_precision_recall_curve(y_true, y_proba, title='Precision-Recall Curve', save_path=None):
    """Plot precision-recall curve."""
    precision, recall, _ = precision_recall_curve(y_true, y_proba)
    
    plt.figure(figsize=(7, 6))
    plt.plot(recall, precision, color='green', lw=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(title)
    plt.grid(True)
    
    if save_path:
        ensure_dir_exists(os.path.dirname(save_path))
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Plot saved to: {save_path}")
    plt.close()


def plot_train_vs_test_auc(estimators_list, train_auc_scores, test_auc_scores, 
                           title='Train vs Test AUC', save_path=None):
    """Plot training vs testing AUC across different model configurations."""
    plt.figure(figsize=(7, 5))
    plt.plot(estimators_list, train_auc_scores, marker='o', label='Train AUC', color='blue')
    plt.plot(estimators_list, test_auc_scores, marker='o', label='Test AUC', color='green')
    plt.xlabel('Number of Trees (n_estimators)')
    plt.ylabel('AUC Score')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    
    if save_path:
        ensure_dir_exists(os.path.dirname(save_path))
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Plot saved to: {save_path}")
    plt.close()


def print_model_comparison(baseline_metrics, embedding_metrics):
    """Print a formatted comparison between baseline and embedding models."""
    print("\n" + "="*70)
    print("MODEL COMPARISON SUMMARY")
    print("="*70)
    
    print(f"\nBaseline Model (Numeric Features):")
    print(f"  Accuracy:  {baseline_metrics['accuracy']:.4f}")
    print(f"  ROC-AUC:   {baseline_metrics['roc_auc']:.4f}")
    
    print(f"\nEmbedding Model (Sentence-BERT):")
    print(f"  Accuracy:  {embedding_metrics['accuracy']:.4f}")
    print(f"  ROC-AUC:   {embedding_metrics['roc_auc']:.4f}")
    
    acc_improvement = ((embedding_metrics['accuracy'] - baseline_metrics['accuracy']) 
                       / baseline_metrics['accuracy'] * 100)
    auc_improvement = ((embedding_metrics['roc_auc'] - baseline_metrics['roc_auc']) 
                       / baseline_metrics['roc_auc'] * 100)
    
    print(f"\nImprovement:")
    print(f"  Accuracy: {acc_improvement:+.2f}%")
    print(f"  ROC-AUC:  {auc_improvement:+.2f}%")
    print("="*70 + "\n")
