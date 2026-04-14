"""
Improved Fake News Detection Model Training Script
This script trains an improved model with better preprocessing and hyperparameters
"""

import pandas as pd
import numpy as np
import re
import sys
import os
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import nltk

# Fix Unicode output on Windows terminals
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Download required NLTK data
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

print("=" * 60)
print("IMPROVED FAKE NEWS DETECTION MODEL TRAINING")
print("=" * 60)

# Load datasets
print("\n[1/7] Loading datasets...")
try:
    # Load original dataset
    news_dataset = pd.read_csv('train.csv')
    print(f"✓ Original dataset loaded: {news_dataset.shape[0]} articles")
    
    # Load new uploaded dataset
    new_dataset = pd.read_csv('ML Dataset/news_articles.csv')
    print(f"✓ New custom dataset loaded: {new_dataset.shape[0]} articles")
    
    # Preprocess new dataset to match original format
    # Original format has: id, title, author, text, label
    # New dataset has: author, published, title, text, language, site_url, main_img_url, type, label, etc.
    new_dataset = new_dataset[['title', 'author', 'label']]
    new_dataset = new_dataset.dropna(subset=['label'])
    
    # Map 'Real' to 0 and 'Fake' to 1
    new_dataset['label'] = new_dataset['label'].map({'Real': 0, 'Fake': 1})
    new_dataset = new_dataset.dropna(subset=['label'])
    new_dataset['label'] = new_dataset['label'].astype(int)
    
    # Concatenate both datasets
    news_dataset = pd.concat([news_dataset, new_dataset], ignore_index=True)
    print(f"✓ Combined dataset size: {news_dataset.shape[0]} articles")
    
    # Shuffle the dataset
    news_dataset = news_dataset.sample(frac=1, random_state=42).reset_index(drop=True)
    
except Exception as e:
    print(f"✗ Error loading dataset: {e}")
    exit(1)

# Check for user feedback data
if os.path.exists('user_feedback.csv'):
    try:
        print("\n[✓] Found user feedback data! Incorporating into training...")
        feedback_dataset = pd.read_csv('user_feedback.csv')
        feedback_dataset = feedback_dataset[['title', 'author', 'label']]
        feedback_dataset = feedback_dataset.dropna(subset=['label'])
        feedback_dataset['label'] = feedback_dataset['label'].astype(int)
        
        # Concatenate feedback with the main dataset
        news_dataset = pd.concat([news_dataset, feedback_dataset], ignore_index=True)
        print(f"✓ Added {feedback_dataset.shape[0]} user feedback articles.")
        print(f"✓ New combined dataset size: {news_dataset.shape[0]} articles.")
    except Exception as e:
        print(f"✗ Error loading user feedback: {e}")

# Check for dynamically fetched real-world news
if os.path.exists('fetched_news.csv'):
    try:
        print("\n[✓] Found fetched real-world news! Incorporating into training...")
        fetched_dataset = pd.read_csv('fetched_news.csv')
        fetched_dataset = fetched_dataset[['title', 'author', 'label']]
        fetched_dataset = fetched_dataset.dropna(subset=['label'])
        fetched_dataset['label'] = fetched_dataset['label'].astype(int)
        
        news_dataset = pd.concat([news_dataset, fetched_dataset], ignore_index=True)
        print(f"✓ Added {fetched_dataset.shape[0]} real-world news articles.")
        print(f"✓ New combined dataset size: {news_dataset.shape[0]} articles.")
    except Exception as e:
        print(f"✗ Error loading fetched news: {e}")

# Check for Indian news data (for better India coverage)
if os.path.exists('indian_news.csv'):
    try:
        print("\n[✓] Found Indian news dataset! Incorporating for better regional coverage...")
        indian_dataset = pd.read_csv('indian_news.csv')
        indian_dataset = indian_dataset[['title', 'author', 'label']]
        indian_dataset = indian_dataset.dropna(subset=['label'])
        indian_dataset['label'] = indian_dataset['label'].astype(int)
        
        news_dataset = pd.concat([news_dataset, indian_dataset], ignore_index=True)
        print(f"✓ Added {indian_dataset.shape[0]} Indian news articles (labeled as Real).")
        print(f"✓ New combined dataset size: {news_dataset.shape[0]} articles.")
    except Exception as e:
        print(f"✗ Error loading Indian news: {e}")

# Handle missing values
print("\n[2/7] Preprocessing data...")
news_dataset = news_dataset.fillna('')

# Merge author and title for better context
news_dataset['content'] = news_dataset['author'].astype(str) + ' ' + news_dataset['title'].astype(str)

# Text preprocessing function
port_stem = PorterStemmer()

def stemming(content):
    """Enhanced text preprocessing with stemming"""
    # Remove non-alphabetic characters
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    # Convert to lowercase
    stemmed_content = stemmed_content.lower()
    # Split into words
    stemmed_content = stemmed_content.split()
    # Remove stopwords and apply stemming
    stemmed_content = [port_stem.stem(word) for word in stemmed_content 
                      if word not in stopwords.words('english')]
    # Join back
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

# Apply preprocessing
print("   Applying text preprocessing (this may take a few minutes)...")
news_dataset['content'] = news_dataset['content'].apply(stemming)
print("✓ Preprocessing complete")

# Separate features and labels
X = news_dataset['content'].values
Y = news_dataset['label'].values

print(f"   Features shape: {X.shape}")
print(f"   Labels shape: {Y.shape}")
print(f"   Class distribution: Fake={np.sum(Y==0)}, Real={np.sum(Y==1)}")

# TF-IDF Vectorization with improved parameters
print("\n[3/7] Creating TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=20000,  # Increased from default
    min_df=2,            # Minimum document frequency
    max_df=0.9,          # Maximum document frequency
    ngram_range=(1, 2),  # Use both unigrams and bigrams
    sublinear_tf=True    # Use sublinear tf scaling
)

X = vectorizer.fit_transform(X)
print(f"✓ TF-IDF vectorization complete: {X.shape[1]} features")

# Train-test split
print("\n[4/7] Splitting data...")
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, stratify=Y, random_state=42
)
print(f"✓ Training set: {X_train.shape[0]} samples")
print(f"✓ Test set: {X_test.shape[0]} samples")

# Train Logistic Regression with hyperparameter tuning
print("\n[5/7] Training Logistic Regression model...")
print("   Performing hyperparameter tuning...")

# Define parameter grid
param_grid = {
    'C': [0.1, 1, 10],
    'solver': ['lbfgs', 'liblinear'],
    'max_iter': [1000]
}

# Grid search
lr_model = LogisticRegression(random_state=42)
grid_search = GridSearchCV(
    lr_model, 
    param_grid, 
    cv=3, 
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, Y_train)
best_lr_model = grid_search.best_estimator_

print(f"✓ Best parameters: {grid_search.best_params_}")
print(f"✓ Best CV score: {grid_search.best_score_:.4f}")

# Evaluate on training data
Y_train_pred = best_lr_model.predict(X_train)
train_accuracy = accuracy_score(Y_train, Y_train_pred)
print(f"✓ Training accuracy: {train_accuracy:.4f}")

# Evaluate on test data
print("\n[6/7] Evaluating model...")
Y_test_pred = best_lr_model.predict(X_test)
test_accuracy = accuracy_score(Y_test, Y_test_pred)

print(f"✓ Test accuracy: {test_accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(Y_test, Y_test_pred, 
                          target_names=['Fake News', 'Real News']))

print("\nConfusion Matrix:")
cm = confusion_matrix(Y_test, Y_test_pred)
print(f"   True Negatives (Fake correctly identified): {cm[0][0]}")
print(f"   False Positives (Fake predicted as Real): {cm[0][1]}")
print(f"   False Negatives (Real predicted as Fake): {cm[1][0]}")
print(f"   True Positives (Real correctly identified): {cm[1][1]}")

# Save the improved model
print("\n[7/7] Saving model and vectorizer...")
try:
    with open('model/fake_news_model.pkl', 'wb') as f:
        pickle.dump(best_lr_model, f)
    print("✓ Model saved to: model/fake_news_model.pkl")
    
    with open('model/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    print("✓ Vectorizer saved to: model/tfidf_vectorizer.pkl")
    
except Exception as e:
    print(f"✗ Error saving model: {e}")

print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETE!")
print("=" * 60)
print(f"\nFinal Test Accuracy: {test_accuracy:.2%}")
print(f"Model is ready to use in the Flask application.")
print("\nTo run the application:")
print("  python app.py")
print("=" * 60)
