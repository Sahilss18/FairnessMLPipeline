"""
Data Preprocessing Module
Handles loading, cleaning, and preparing the fairness dataset.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from config import DATASET_PATH, TEST_SIZE, RANDOM_STATE, TOXICITY_THRESHOLD


def load_and_clean_data(dataset_path=DATASET_PATH):
    """
    Load the fairness dataset and handle missing values.
    
    Returns:
        pd.DataFrame: Cleaned dataset
    """
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"Dataset shape: {df.shape}")
    
    # Check initial missing values
    initial_missing = df.isnull().sum().sum()
    print(f"Initial missing values: {initial_missing}")
    
    # Handle missing values in text column
    df['comment_text'] = df['comment_text'].fillna('')
    
    # Handle missing numeric values
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Handle missing categorical values
    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')
    
    # Verify all missing values are handled
    final_missing = df.isnull().sum().sum()
    print(f"Missing values after preprocessing: {final_missing}")
    
    return df


def prepare_baseline_data(df):
    """
    Prepare data for baseline model (numeric features only).
    
    Args:
        df: Input dataframe
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    # Separate features and target
    labels = df['target']
    features = df.drop('target', axis=1)
    
    # Keep only numeric columns
    numeric_features = features.select_dtypes(include=['number'])
    
    print(f"\nNumeric columns used for baseline model:")
    print(list(numeric_features.columns))
    
    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        numeric_features, labels, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_STATE
    )
    
    # Convert continuous labels to binary
    y_train = (y_train >= TOXICITY_THRESHOLD).astype(int)
    y_test = (y_test >= TOXICITY_THRESHOLD).astype(int)
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    print(f"Class distribution in training: {y_train.value_counts().to_dict()}")
    
    return X_train, X_test, y_train, y_test


def prepare_text_data(df):
    """
    Prepare text data for embedding-based model.
    
    Args:
        df: Input dataframe
        
    Returns:
        tuple: (text_data, labels)
    """
    text_data = df['comment_text'].fillna('')
    labels = df['target']
    
    print(f"\nTotal text samples: {len(text_data)}")
    print(f"Average comment length: {text_data.str.len().mean():.2f} characters")
    
    return text_data, labels


def split_data_for_embeddings(X_embeddings, y, test_size=TEST_SIZE, random_state=RANDOM_STATE):
    """
    Split embedding data into train and test sets.
    
    Args:
        X_embeddings: Embedding vectors
        y: Target labels
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X_embeddings, y,
        test_size=test_size,
        random_state=random_state
    )
    
    # Convert to binary labels
    y_train = (y_train >= TOXICITY_THRESHOLD).astype(int)
    y_test = (y_test >= TOXICITY_THRESHOLD).astype(int)
    
    print(f"\nEmbedding data split:")
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples: {X_test.shape[0]}")
    print(f"Embedding dimension: {X_train.shape[1]}")
    
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    # Test preprocessing
    df = load_and_clean_data()
    print("\nDataset info:")
    print(df.info())
    
    X_train, X_test, y_train, y_test = prepare_baseline_data(df)
    print(f"\nBaseline data prepared successfully.")
    
    text_data, labels = prepare_text_data(df)
    print(f"\nText data prepared successfully.")
