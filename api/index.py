from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
import os

# Download stopwords if not already downloaded
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize Porter Stemmer
port_stem = PorterStemmer()

# Load trained model and vectorizer
model = None
vectorizer = None
model_loaded = False

def load_model():
    """Load the model and vectorizer"""
    global model, vectorizer, model_loaded
    try:
        # Get the directory where this file is located
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'model', 'fake_news_model.pkl')
        vectorizer_path = os.path.join(base_dir, 'model', 'tfidf_vectorizer.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            print("✗ Model files not found!")
            return False
            
        model = pickle.load(open(model_path, 'rb'))
        vectorizer = pickle.load(open(vectorizer_path, 'rb'))
        model_loaded = True
        print("✓ Model and vectorizer loaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        model_loaded = False
        return False

# Try to load model on startup
load_model()

# Text preprocessing function
def preprocess_text(content):
    """
    Preprocess text by:
    1. Removing non-alphabetic characters
    2. Converting to lowercase
    3. Removing stopwords
    4. Applying stemming
    """
    try:
        # Remove non-alphabetic characters
        content = re.sub('[^a-zA-Z]', ' ', content)
        # Convert to lowercase
        content = content.lower()
        # Split into words
        content = content.split()
        # Remove stopwords and apply stemming
        content = [port_stem.stem(word) for word in content if word not in stopwords.words('english')]
        # Join back into string
        return ' '.join(content)
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return content

@app.route("/")
def home():
    return render_template("index.html", prediction=None, model_status=model_loaded)

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        try:
            # Check if model is loaded
            if not model_loaded:
                return render_template("index.html", 
                                     prediction="Error: Model not loaded. Please retrain the model.",
                                     model_status=False)
            
            # Get the news text from form
            news_text = request.form["news_text"]
            
            # Check if text is empty
            if not news_text or len(news_text.strip()) < 10:
                return render_template("index.html", 
                                     prediction="Error: Please enter a valid news article (at least 10 characters)",
                                     model_status=model_loaded)
            
            # Preprocess the text
            preprocessed_text = preprocess_text(news_text)
            
            # Transform using vectorizer
            transformed_text = vectorizer.transform([preprocessed_text])
            
            # Get prediction
            prediction = model.predict(transformed_text)[0]
            
            # Get prediction probability for confidence score
            try:
                prediction_proba = model.predict_proba(transformed_text)[0]
                confidence = max(prediction_proba) * 100
            except:
                confidence = 85  # Default confidence if predict_proba not available
            
            # Convert 0/1 prediction to meaningful text
            if prediction == 1:
                result_text = f"Real News"
            else:
                result_text = f"Fake News"
            
            print(f"Prediction: {result_text} (Confidence: {confidence:.1f}%)")
            return render_template("index.html", prediction=result_text, model_status=model_loaded)
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            import traceback
            traceback.print_exc()
            return render_template("index.html", 
                                 prediction=f"Error: Unable to process the article. {str(e)}",
                                 model_status=model_loaded)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """API endpoint for predictions"""
    try:
        if not model_loaded:
            return jsonify({
                "error": "Model not loaded. Please retrain the model."
            }), 503
            
        data = request.get_json()
        news_text = data.get("text", "")
        
        if not news_text or len(news_text.strip()) < 10:
            return jsonify({
                "error": "Please provide valid news article text (at least 10 characters)"
            }), 400
        
        # Preprocess the text
        preprocessed_text = preprocess_text(news_text)
        
        # Transform and predict
        transformed_text = vectorizer.transform([preprocessed_text])
        prediction = model.predict(transformed_text)[0]
        
        # Get confidence
        try:
            prediction_proba = model.predict_proba(transformed_text)[0]
            confidence = max(prediction_proba) * 100
        except:
            confidence = 85
        
        result = {
            "prediction": "Real News" if prediction == 1 else "Fake News",
            "confidence": round(confidence, 2),
            "label": int(prediction)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded
    })

# Vercel requires the app to be exposed
handler = app
