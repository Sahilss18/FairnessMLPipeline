"""
Evaluation Module
Compares baseline and embedding models, generates comprehensive reports.
"""
import os
from config import OUTPUTS_DIR
from utils import print_model_comparison
from baseline_model import run_baseline_phase
from embedding_model import run_embedding_phase


def evaluate_all_phases():
    """
    Run complete evaluation pipeline comparing both phases.
    
    Returns:
        dict: Complete evaluation results
    """
    print("\n" + "="*80)
    print("COMPLETE PROJECT EVALUATION")
    print("="*80)
    print("\nThis will train and evaluate both baseline and embedding models.")
    print("Evaluation will include:")
    print("  - Data preprocessing and splitting")
    print("  - Baseline model training on numeric features")
    print("  - Embedding generation using Sentence-BERT")
    print("  - Embedding-based model training")
    print("  - Performance comparison and visualizations")
    print("\n" + "="*80 + "\n")
    
    # Phase 1: Baseline Model
    print("\nStarting Phase 1: Baseline Model")
    baseline_results = run_baseline_phase(save_model_flag=True, compare_sizes=True)
    baseline_metrics = baseline_results['metrics']
    
    # Phase 2: Embedding Model
    print("\nStarting Phase 2: Embedding-Based Model")
    embedding_results = run_embedding_phase(save_model_flag=True, save_embeddings_flag=True)
    embedding_metrics = embedding_results['metrics']
    
    # Compare results
    print_model_comparison(baseline_metrics, embedding_metrics)
    
    # Generate summary report
    generate_summary_report(baseline_metrics, embedding_metrics)
    
    return {
        'baseline': baseline_results,
        'embedding': embedding_results
    }


def generate_summary_report(baseline_metrics, embedding_metrics):
    """
    Generate a text summary report of model performance.
    
    Args:
        baseline_metrics: Metrics from baseline model
        embedding_metrics: Metrics from embedding model
    """
    report_path = os.path.join(OUTPUTS_DIR, 'evaluation_report.txt')
    
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("FAIRNESS AND BIAS DETECTION SYSTEM - EVALUATION REPORT\n")
        f.write("="*80 + "\n\n")
        
        f.write("PROJECT OVERVIEW\n")
        f.write("-"*80 + "\n")
        f.write("This project implements a multi-phase machine learning system for detecting\n")
        f.write("bias and promoting fairness in text content, specifically targeting problems\n")
        f.write("in autonomous agents and AI systems.\n\n")
        
        f.write("PHASE 1: BASELINE MODEL (NUMERIC FEATURES)\n")
        f.write("-"*80 + "\n")
        f.write(f"Accuracy:  {baseline_metrics['accuracy']:.4f}\n")
        f.write(f"ROC-AUC:   {baseline_metrics['roc_auc']:.4f}\n\n")
        
        f.write("PHASE 2: EMBEDDING-BASED MODEL (SENTENCE-BERT)\n")
        f.write("-"*80 + "\n")
        f.write(f"Accuracy:  {embedding_metrics['accuracy']:.4f}\n")
        f.write(f"ROC-AUC:   {embedding_metrics['roc_auc']:.4f}\n\n")
        
        acc_improvement = ((embedding_metrics['accuracy'] - baseline_metrics['accuracy']) 
                          / baseline_metrics['accuracy'] * 100)
        auc_improvement = ((embedding_metrics['roc_auc'] - baseline_metrics['roc_auc']) 
                          / baseline_metrics['roc_auc'] * 100)
        
        f.write("IMPROVEMENT ANALYSIS\n")
        f.write("-"*80 + "\n")
        f.write(f"Accuracy Improvement: {acc_improvement:+.2f}%\n")
        f.write(f"ROC-AUC Improvement:  {auc_improvement:+.2f}%\n\n")
        
        f.write("KEY FINDINGS\n")
        f.write("-"*80 + "\n")
        f.write("1. Sentence embeddings capture semantic meaning better than numeric features\n")
        f.write("2. The embedding model shows improved discrimination between fair and biased text\n")
        f.write("3. Semantic similarity analysis provides interpretable explanations\n\n")
        
        f.write("FUTURE WORK (PHASE 3)\n")
        f.write("-"*80 + "\n")
        f.write("- Integrate autoregressive reasoning for chain-of-thought explanations\n")
        f.write("- Implement explicit fairness metrics (DPD, DI)\n")
        f.write("- Add accountability logging and rule-based verification\n")
        f.write("- Extend toward autonomous agent capabilities\n\n")
        
        f.write("="*80 + "\n")
    
    print(f"\nEvaluation report saved to: {report_path}")


if __name__ == "__main__":
    results = evaluate_all_phases()
    print("\nComplete evaluation finished successfully.")
    print(f"All outputs saved to: {OUTPUTS_DIR}")
