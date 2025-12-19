"""
Main Execution Script
Orchestrates the complete fairness and bias detection pipeline.
"""
import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from baseline_model import run_baseline_phase
from embedding_model import run_embedding_phase
from evaluate import evaluate_all_phases
from inference import interactive_mode, demo_analysis


def print_banner():
    """Print project banner."""
    print("\n" + "="*80)
    print("FAIRNESS AND BIAS DETECTION SYSTEM FOR AUTONOMOUS AGENTS")
    print("="*80)
    print("A multi-phase machine learning system for identifying bias and")
    print("promoting fairness in AI-generated and human-generated content.")
    print("="*80 + "\n")


def run_all():
    """Run complete pipeline: both phases with evaluation."""
    print_banner()
    print("Running complete pipeline (Phase 1 + Phase 2 + Evaluation)...\n")
    results = evaluate_all_phases()
    print("\n" + "="*80)
    print("PIPELINE COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("  1. Review outputs in the 'outputs/' directory")
    print("  2. Check trained models in 'models/' directory")
    print("  3. Run inference: python main.py --mode inference")
    print("="*80 + "\n")


def run_baseline():
    """Run Phase 1: Baseline model only."""
    print_banner()
    print("Running Phase 1: Baseline Model (Numeric Features)\n")
    results = run_baseline_phase(save_model_flag=True, compare_sizes=True)
    print("\nPhase 1 complete. Model saved.")
    print(f"Accuracy: {results['metrics']['accuracy']:.4f}")
    print(f"ROC-AUC:  {results['metrics']['roc_auc']:.4f}\n")


def run_embedding():
    """Run Phase 2: Embedding-based model only."""
    print_banner()
    print("Running Phase 2: Embedding-Based Model (Sentence-BERT)\n")
    results = run_embedding_phase(save_model_flag=True, save_embeddings_flag=True)
    print("\nPhase 2 complete. Model and embeddings saved.")
    print(f"Accuracy: {results['metrics']['accuracy']:.4f}")
    print(f"ROC-AUC:  {results['metrics']['roc_auc']:.4f}\n")


def run_inference():
    """Run inference mode for user input analysis."""
    print_banner()
    print("Starting Interactive Inference Mode\n")
    interactive_mode()


def run_demo():
    """Run demonstration with sample comments."""
    print_banner()
    demo_analysis()


def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Fairness and Bias Detection System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --mode all         # Run complete pipeline
  python main.py --mode baseline    # Run Phase 1 only
  python main.py --mode embedding   # Run Phase 2 only
  python main.py --mode inference   # Interactive comment analysis
  python main.py --mode demo        # Demo with sample comments
        """
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['all', 'baseline', 'embedding', 'inference', 'demo'],
        default='all',
        help='Execution mode (default: all)'
    )
    
    args = parser.parse_args()
    
    # Route to appropriate function
    try:
        if args.mode == 'all':
            run_all()
        elif args.mode == 'baseline':
            run_baseline()
        elif args.mode == 'embedding':
            run_embedding()
        elif args.mode == 'inference':
            run_inference()
        elif args.mode == 'demo':
            run_demo()
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease ensure 'fairness_dataset.csv' is in the 'data/' directory.")
        print("Run 'python main.py --help' for usage information.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check the error message above and try again.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
