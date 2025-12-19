"""
Phase 2: Embedding-Based Model Training
Generates Sentence-BERT embeddings and trains a classifier for improved fairness detection.
"""
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import numpy as np
import os

from config import (
    SENTENCE_TRANSFORMER_MODEL, 
    EMBEDDING_CONFIG, 
    EMBEDDING_MODEL_PATH,
    EMBEDDINGS_TRAIN_PATH,
    EMBEDDINGS_TEST_PATH,
    OUTPUTS_DIR
)
from utils import (
    save_model, 
    save_embeddings, 
    load_embeddings,
    plot_confusion_matrix, 
    plot_roc_curve
)
from preprocessing import (
    load_and_clean_data, 
    prepare_text_data,
    split_data_for_embeddings
)


def generate_embeddings(text_data, model_name=SENTENCE_TRANSFORMER_MODEL):
    """
    Generate sentence embeddings using Sentence-BERT.
    
    Args:
        text_data: List or Series of text strings
        model_name: Name of the sentence transformer model
        
    Returns:
        np.array: Matrix of embeddings (n_samples, embedding_dim)
    """
    print("\n" + "="*70)
    print("GENERATING SENTENCE EMBEDDINGS")
    print("="*70)
    
    print(f"\nLoading Sentence-BERT model: {model_name}")
    embedder = SentenceTransformer(model_name)
    
    print(f"Encoding {len(text_data)} text samples...")
    print("This may take several minutes for large datasets...")
    embeddings = embedder.encode(
        text_data.tolist(), 
        show_progress_bar=True,
        batch_size=32,  # Smaller batch size for memory efficiency
        convert_to_numpy=True
    )
    
    print(f"Embeddings generated with shape: {embeddings.shape}")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    
    return embeddings, embedder


def train_embedding_model(X_train, y_train):
    """
    Train a Random Forest classifier on sentence embeddings.
    
    Args:
        X_train: Training embeddings
        y_train: Training labels
        
    Returns:
        Trained model
    """
    print("\n" + "="*70)
    print("PHASE 2: TRAINING EMBEDDING-BASED MODEL")
    print("="*70)
    
    rf = RandomForestClassifier(**EMBEDDING_CONFIG)
    print(f"\nTraining Random Forest with {EMBEDDING_CONFIG['n_estimators']} estimators on embeddings...")
    rf.fit(X_train, y_train)
    print("Training complete.")
    
    return rf


def evaluate_embedding_model(model, X_test, y_test, save_plots=True):
    """
    Evaluate the embedding-based model and generate visualizations.
    
    Args:
        model: Trained model
        X_test: Test embeddings
        y_test: Test labels
        save_plots: Whether to save plots to disk
        
    Returns:
        dict: Dictionary containing evaluation metrics
    """
    print("\nEvaluating embedding-based model...")
    
    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    
    print(f"\nEmbedding Model Performance:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  ROC-AUC:  {roc_auc:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Visualizations
    if save_plots:
        cm_path = os.path.join(OUTPUTS_DIR, 'embedding_confusion_matrix.png')
        roc_path = os.path.join(OUTPUTS_DIR, 'embedding_roc_curve.png')
        
        plot_confusion_matrix(y_test, y_pred,
                            title='Confusion Matrix - Embedding Model',
                            save_path=cm_path)
        plot_roc_curve(y_test, y_proba,
                      title='ROC Curve - Embedding Model',
                      save_path=roc_path)
    
    return {
        'accuracy': accuracy,
        'roc_auc': roc_auc,
        'y_pred': y_pred,
        'y_proba': y_proba
    }


def run_embedding_phase(save_model_flag=True, save_embeddings_flag=True, 
                       load_existing_embeddings=False):
    """
    Execute the complete embedding-based model pipeline.
    
    Args:
        save_model_flag: Whether to save the trained model
        save_embeddings_flag: Whether to save generated embeddings
        load_existing_embeddings: Whether to load pre-computed embeddings
        
    Returns:
        dict: Results including model, embedder, and metrics
    """
    # Load and prepare data
    df = load_and_clean_data()
    text_data, labels = prepare_text_data(df)
    
    # Generate or load embeddings
    if load_existing_embeddings and os.path.exists(EMBEDDINGS_TRAIN_PATH):
        print("\nLoading pre-computed embeddings...")
        # This would require saving train/test split indices
        # For simplicity, regenerating embeddings
        embeddings, embedder = generate_embeddings(text_data)
    else:
        embeddings, embedder = generate_embeddings(text_data)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data_for_embeddings(embeddings, labels)
    
    # Save embeddings if requested
    if save_embeddings_flag:
        save_embeddings(X_train, EMBEDDINGS_TRAIN_PATH)
        save_embeddings(X_test, EMBEDDINGS_TEST_PATH)
    
    # Train model
    model = train_embedding_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_embedding_model(model, X_test, y_test, save_plots=True)
    
    # Save model
    if save_model_flag:
        save_model(model, EMBEDDING_MODEL_PATH)
    
    print("\n" + "="*70)
    print("PHASE 2 COMPLETE")
    print("="*70 + "\n")
    
    return {
        'model': model,
        'embedder': embedder,
        'metrics': metrics,
        'test_data': (X_test, y_test)
    }


if __name__ == "__main__":
    results = run_embedding_phase(save_model_flag=True, save_embeddings_flag=True)
    print("Embedding-based model training and evaluation completed successfully.")
