"""Analyze dataset for gender bias patterns"""
import pandas as pd
import re

# Read dataset with proper encoding
df = pd.read_csv('AiFairness.csv/fairness_dataset.csv', encoding='latin-1')

print(f"Total rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}\n")

# Look for gender-related terms
gender_keywords = ['women', 'woman', 'female', 'girl', 'emotional', 'leader', 'kitchen', 'men', 'male']
pattern = '|'.join(gender_keywords)

gender_df = df[df['comment_text'].str.contains(pattern, case=False, na=False)]
print(f"Comments with gender keywords: {len(gender_df)}\n")

# Sample toxic gender comments (using target column for toxicity)
toxic_gender = gender_df[gender_df['target'] > 0.6][['comment_text', 'target']].head(20)
print("=== TOXIC GENDER-RELATED COMMENTS ===")
for idx, row in toxic_gender.iterrows():
    print(f"[{row['target']:.2f}] {row['comment_text']}")

print("\n=== PATTERN ANALYSIS ===")
# Check specific patterns
emotional_pattern = gender_df[gender_df['comment_text'].str.contains(r'(women|woman|female).*(emotional|emotion)', case=False, na=False)]
print(f"\nComments with 'women/female + emotional': {len(emotional_pattern)}")
if len(emotional_pattern) > 0:
    print("Examples:")
    for idx, row in emotional_pattern[['comment_text', 'target']].head(10).iterrows():
        print(f"  [{row['target']:.2f}] {row['comment_text']}")

leader_pattern = gender_df[gender_df['comment_text'].str.contains(r'(women|woman|female).*(leader|leadership|boss)', case=False, na=False)]
print(f"\nComments with 'women/female + leader': {len(leader_pattern)}")
if len(leader_pattern) > 0:
    print("Examples:")
    for idx, row in leader_pattern[['comment_text', 'target']].head(10).iterrows():
        print(f"  [{row['target']:.2f}] {row['comment_text']}")

too_pattern = gender_df[gender_df['comment_text'].str.contains(r'(women|woman|female).*(too|not)', case=False, na=False)]
print(f"\nComments with 'women/female + too/not': {len(too_pattern)}")
if len(too_pattern) > 0:
    print("Examples:")
    for idx, row in too_pattern[['comment_text', 'target']].head(10).iterrows():
        print(f"  [{row['target']:.2f}] {row['comment_text']}")
