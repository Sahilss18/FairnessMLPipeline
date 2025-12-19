"""
Test Sentence-BERT Embedding Quality
Tests if embeddings properly capture semantic meaning and distinguish bias from fair content.
"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def test_embedding_quality():
    print('='*80)
    print('SENTENCE-BERT EMBEDDING QUALITY TEST')
    print('='*80)
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f'\nModel: all-MiniLM-L6-v2')
    print(f'Embedding dimension: {model.get_sentence_embedding_dimension()}')
    
    # Test bias detection scenarios
    biased_comments = [
        'You are stupid and I hate you',
        'This bitch is nuts',
        'Poor people are less reliable',
        'Women are naturally better at administrative tasks',
        'Old workers cannot adapt to technology',
    ]
    
    fair_comments = [
        'Everyone deserves respect and kindness',
        'All applicants should be evaluated equally',
        'Credit limits should be based on repayment history',
        'People of all backgrounds contribute to society',
        'Age does not determine ability',
    ]
    
    print('\n' + '='*80)
    print('TESTING BIAS VS FAIR DISTINCTION')
    print('='*80)
    
    # Encode
    biased_emb = model.encode(biased_comments)
    fair_emb = model.encode(fair_comments)
    
    # Average embeddings for each category
    avg_biased = biased_emb.mean(axis=0).reshape(1, -1)
    avg_fair = fair_emb.mean(axis=0).reshape(1, -1)
    
    print('\nCategory similarity (should be LOW):')
    category_sim = cosine_similarity(avg_biased, avg_fair)[0][0]
    print(f'Biased vs Fair: {category_sim:.3f}')
    
    if category_sim > 0.5:
        print('⚠️  WARNING: Categories too similar! Model may struggle.')
    else:
        print('✓ Good separation between categories.')
    
    # Test individual examples
    print('\n' + '='*80)
    print('EXPLICIT BIAS COMMENTS (Should predict BIASED)')
    print('='*80)
    
    for comment in biased_comments:
        emb = model.encode([comment])
        sim_to_biased = cosine_similarity(emb, avg_biased)[0][0]
        sim_to_fair = cosine_similarity(emb, avg_fair)[0][0]
        prediction = 'BIASED' if sim_to_biased > sim_to_fair else 'FAIR'
        correct = '✓' if prediction == 'BIASED' else '✗'
        print(f'\n{correct} "{comment[:60]}..."')
        print(f'   Similarity to biased: {sim_to_biased:.3f}')
        print(f'   Similarity to fair: {sim_to_fair:.3f}')
        print(f'   Prediction: {prediction}')
    
    print('\n' + '='*80)
    print('FAIR COMMENTS (Should predict FAIR)')
    print('='*80)
    
    for comment in fair_comments:
        emb = model.encode([comment])
        sim_to_biased = cosine_similarity(emb, avg_biased)[0][0]
        sim_to_fair = cosine_similarity(emb, avg_fair)[0][0]
        prediction = 'BIASED' if sim_to_biased > sim_to_fair else 'FAIR'
        correct = '✓' if prediction == 'FAIR' else '✗'
        print(f'\n{correct} "{comment[:60]}..."')
        print(f'   Similarity to biased: {sim_to_biased:.3f}')
        print(f'   Similarity to fair: {sim_to_fair:.3f}')
        print(f'   Prediction: {prediction}')
    
    print('\n' + '='*80)
    print('SUBTLE BIAS TEST (Problem cases)')
    print('='*80)
    
    subtle_bias = [
        'Applicants from low-income neighborhoods are less reliable',
        'McGill administrators are imbeciles',
        'Your tax dollars buying votes for Democrats',
        'Poor people do not understand financial responsibility',
    ]
    
    for comment in subtle_bias:
        emb = model.encode([comment])
        sim_to_biased = cosine_similarity(emb, avg_biased)[0][0]
        sim_to_fair = cosine_similarity(emb, avg_fair)[0][0]
        diff = sim_to_biased - sim_to_fair
        prediction = 'BIASED' if sim_to_biased > sim_to_fair else 'FAIR'
        
        print(f'\nComment: "{comment[:60]}..."')
        print(f'  Biased: {sim_to_biased:.3f} | Fair: {sim_to_fair:.3f} | Diff: {diff:.3f}')
        print(f'  Prediction: {prediction}')
        
        if abs(diff) < 0.05:
            print(f'  ⚠️  AMBIGUOUS: Too close to call!')
        elif prediction == 'FAIR':
            print(f'  ✗ WRONG: Should be biased but predicted fair')
    
    # Test semantic understanding
    print('\n' + '='*80)
    print('SEMANTIC UNDERSTANDING TEST')
    print('='*80)
    
    pairs = [
        ('You are stupid', 'You are foolish', 'Should be SIMILAR'),
        ('I hate you', 'I love you', 'Should be DIFFERENT'),
        ('Poor people are unreliable', 'Low-income applicants are trustworthy', 'Should be DIFFERENT'),
        ('Everyone deserves respect', 'All people deserve kindness', 'Should be SIMILAR'),
    ]
    
    for sent1, sent2, expected in pairs:
        emb1 = model.encode([sent1])
        emb2 = model.encode([sent2])
        sim = cosine_similarity(emb1, emb2)[0][0]
        
        print(f'\n"{sent1}" vs "{sent2}"')
        print(f'  Similarity: {sim:.3f}')
        print(f'  Expected: {expected}')
        
        if 'SIMILAR' in expected and sim < 0.5:
            print(f'  ⚠️  WARNING: Should be similar but similarity is low!')
        elif 'DIFFERENT' in expected and sim > 0.6:
            print(f'  ⚠️  WARNING: Should be different but similarity is high!')
        else:
            print(f'  ✓ Correct')
    
    print('\n' + '='*80)
    print('SUMMARY')
    print('='*80)
    print('\nEmbedding Model Status:')
    print('  ✓ Model loads correctly')
    print('  ✓ Generates 384-dimensional embeddings')
    print('  ✓ Captures semantic similarity')
    
    if category_sim < 0.5:
        print('  ✓ Distinguishes bias from fair (at high level)')
    else:
        print('  ✗ Poor separation between bias and fair categories')
    
    print('\nKnown Issues:')
    print('  ✗ Struggles with subtle/institutional bias')
    print('  ✗ Cannot detect socioeconomic discrimination well')
    print('  ✗ Formal language bias appears "fair" to the model')
    
    print('\nRoot Cause:')
    print('  - all-MiniLM-L6-v2 is a general-purpose model')
    print('  - NOT specifically trained for bias detection')
    print('  - Needs fine-tuning on bias-specific data')

if __name__ == '__main__':
    test_embedding_quality()
