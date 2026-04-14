import pickle
import pandas as pd
import numpy as np

try:
    with open('model/fake_news_model.pkl', 'rb') as f: model = pickle.load(f)
    with open('model/tfidf_vectorizer.pkl', 'rb') as f: vectorizer = pickle.load(f)
    
    print('\n=======================================')
    print('          DATA BALANCE CHECK')
    print('=======================================')
    
    # Check the actual training data from train.csv
    try:
        df = pd.read_csv('train.csv')
        counts = df['label'].value_counts()
        total = len(df)
        print(f'Total original articles trained on: {total}')
        print(f'Fake News count (Label 1): {counts.get(1, 0)} ({(counts.get(1, 0)/total)*100:.1f}%)')
        print(f'Real News count (Label 0): {counts.get(0, 0)} ({(counts.get(0, 0)/total)*100:.1f}%)')
        
        if abs((counts.get(1, 0)/total) - (counts.get(0, 0)/total)) < 0.1:
            print('\n--> CONCLUSION: Data is well balanced! No risk of overtraining on one side from data sizing.')
        else:
            print('\n--> WARNING: Data is imbalanced. Model might be biased towards majority class.')
            
    except Exception as e:
        print(f'Could not load train.csv: {e}')
        
    print('\n=======================================')
    print('         MODEL COEFFICIENT BIAS')
    print('=======================================')
    coef = model.coef_[0]
    fake_bias_count = (coef > 0).sum()
    real_bias_count = (coef < 0).sum()
    
    print(f'Total learned vocabulary words: {len(coef)}')
    print(f'Words that point to Fake: {fake_bias_count} ({(fake_bias_count/len(coef))*100:.1f}%)')
    print(f'Words that point to Real: {real_bias_count} ({(real_bias_count/len(coef))*100:.1f}%)')
    
    max_fake_weight = np.max(coef)
    max_real_weight = abs(np.min(coef))
    
    print(f'\nHighest weight pulling to Fake: {max_fake_weight:.4f}')
    print(f'Highest weight pulling to Real: {max_real_weight:.4f}')
    
    if abs(max_fake_weight - max_real_weight) > 2.0:
        print('--> WARNING: The model weights are slightly unbalanced in magnitude.')
    else:
        print('--> CONCLUSION: Coefficient magnitudes are balanced. The model is not overly penalizing or favoring one side unfairly.')

except Exception as e:
    print(f'Error: {e}')
