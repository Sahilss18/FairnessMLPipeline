"""
Configuration file for the Fairness and Bias Detection System.
Contains all paths, hyperparameters, and global settings.
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory paths
DATA_DIR = os.path.join(BASE_DIR, 'AiFairness.csv')  # Updated to actual dataset location
MODELS_DIR = os.path.join(BASE_DIR, 'models')
EMBEDDINGS_DIR = os.path.join(BASE_DIR, 'embeddings')
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')

# Dataset paths
DATASET_PATH = os.path.join(DATA_DIR, 'fairness_dataset.csv')

# HuggingFace token for model downloads (set via environment variable)
HF_TOKEN = os.getenv('HF_TOKEN') or None

# Model save paths
BASELINE_MODEL_PATH = os.path.join(MODELS_DIR, 'baseline_rf_model.pkl')
EMBEDDING_MODEL_PATH = os.path.join(MODELS_DIR, 'embedding_rf_model.pkl')

# Embedding paths
EMBEDDINGS_TRAIN_PATH = os.path.join(EMBEDDINGS_DIR, 'train_embeddings.npy')
EMBEDDINGS_TEST_PATH = os.path.join(EMBEDDINGS_DIR, 'test_embeddings.npy')

# Model hyperparameters
BASELINE_CONFIG = {
    'n_estimators': 100,
    'random_state': 42,
    'n_jobs': -1
}

EMBEDDING_CONFIG = {
    'n_estimators': 150,
    'random_state': 42,
    'n_jobs': -1
}

# Sentence transformer model
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'

# Data processing
TEST_SIZE = 0.2
RANDOM_STATE = 42
# Toxicity threshold for binary classification
# Raised from 0.5 to 0.6 to reduce false negatives (missed biased comments)
# This makes the model more conservative - requires higher toxicity score to classify as "biased"
TOXICITY_THRESHOLD = 0.6

# Reference sentences for semantic comparison
POSITIVE_REFERENCE = "Everyone deserves respect and kindness."
TOXIC_REFERENCE = "You are stupid and I hate you."
