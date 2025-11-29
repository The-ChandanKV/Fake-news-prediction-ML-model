"""
Quick test script to verify model loading and make predictions
"""
import sys

print("Testing model loading...")
print("-" * 50)

# Test imports
try:
    import numpy as np
    print(f"✓ NumPy version: {np.__version__}")
except Exception as e:
    print(f"✗ NumPy error: {e}")
    sys.exit(1)

try:
    import sklearn
    print(f"✓ Scikit-learn version: {sklearn.__version__}")
except Exception as e:
    print(f"✗ Scikit-learn error: {e}")
    sys.exit(1)

try:
    import pickle
    print("✓ Pickle module loaded")
except Exception as e:
    print(f"✗ Pickle error: {e}")
    sys.exit(1)

# Try loading the model
print("\nAttempting to load model...")
try:
    with open('model/fake_news_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ Model loaded successfully!")
    print(f"  Model type: {type(model).__name__}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    print("\nThe model needs to be retrained with the current environment.")
    print("Run: python train_improved_model.py")
    sys.exit(1)

# Try loading the vectorizer
print("\nAttempting to load vectorizer...")
try:
    with open('model/tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    print("✓ Vectorizer loaded successfully!")
    print(f"  Vectorizer type: {type(vectorizer).__name__}")
    print(f"  Features: {len(vectorizer.get_feature_names_out())}")
except Exception as e:
    print(f"✗ Error loading vectorizer: {e}")
    print("\nThe vectorizer needs to be retrained with the current environment.")
    print("Run: python train_improved_model.py")
    sys.exit(1)

# Test prediction
print("\nTesting prediction...")
test_text = "This is a test news article about politics and current events"

try:
    # Preprocess (simple version)
    import re
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    
    port_stem = PorterStemmer()
    processed = re.sub('[^a-zA-Z]', ' ', test_text)
    processed = processed.lower().split()
    processed = [port_stem.stem(word) for word in processed if word not in stopwords.words('english')]
    processed = ' '.join(processed)
    
    # Vectorize
    vectorized = vectorizer.transform([processed])
    
    # Predict
    prediction = model.predict(vectorized)[0]
    
    print(f"✓ Prediction successful!")
    print(f"  Result: {'Real News' if prediction == 1 else 'Fake News'}")
    
    # Try to get confidence
    try:
        proba = model.predict_proba(vectorized)[0]
        confidence = max(proba) * 100
        print(f"  Confidence: {confidence:.2f}%")
    except:
        print("  Confidence: Not available")
        
except Exception as e:
    print(f"✗ Prediction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("ALL TESTS PASSED! ✓")
print("=" * 50)
print("\nThe model is ready to use.")
print("You can now run: python app.py")
