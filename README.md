# 🔍 Fake News Detection System

An advanced AI-powered fake news detection system using machine learning with a modern, interactive web interface featuring glassmorphism design and smooth scroll animations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-98%25+-success.svg)

## ✨ Features

### 🤖 Machine Learning
- **High Accuracy**: 98%+ accuracy on 20,800+ news articles
- **Advanced NLP**: TF-IDF vectorization with unigrams and bigrams
- **Text Preprocessing**: Stemming, stopword removal, and normalization
- **Confidence Scores**: Real-time prediction confidence metrics
- **Hyperparameter Tuning**: Optimized model parameters using GridSearchCV

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Beautiful frosted glass effects
- **Scroll Animations**: Smooth fade-in and slide-up animations
- **Particle Background**: Animated particle system
- **Interactive Elements**: Hover effects and micro-animations
- **Responsive Design**: Works perfectly on all devices
- **Real-time Feedback**: Character counter and loading animations
- **Gradient Animations**: Dynamic color transitions

### 🚀 Technical Features
- RESTful API endpoint for integrations
- Error handling and validation
- Confidence score visualization
- Clean, modular code structure
- Comprehensive documentation

## 📋 Requirements

```
Flask==2.3.0
scikit-learn==1.3.0
pandas==2.0.0
numpy==1.24.0
nltk==3.8.0
```

## 🛠️ Installation

1. **Clone the repository**
```bash
cd "e:\Project\Fake news prediction model"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data** (if not already downloaded)
```python
import nltk
nltk.download('stopwords')
```

## 🎯 Usage

### Training the Model (Optional - Model Already Included)

If you want to retrain the model with improved parameters:

```bash
python train_improved_model.py
```

This will:
- Load and preprocess the training data
- Apply TF-IDF vectorization with optimized parameters
- Perform hyperparameter tuning using GridSearchCV
- Train the model and save it to `model/fake_news_model.pkl`
- Display comprehensive evaluation metrics

### Running the Web Application

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### Using the API

**Endpoint**: `POST /api/predict`

**Request Body**:
```json
{
  "text": "Your news article text here..."
}
```

**Response**:
```json
{
  "prediction": "Real News",
  "confidence": 92.5,
  "label": 1
}
```

**Example using curl**:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news article text..."}'
```

**Example using Python**:
```python
import requests

response = requests.post(
    'http://localhost:5000/api/predict',
    json={'text': 'Your news article here...'}
)
print(response.json())
```

## 📊 Model Performance

### Current Model Statistics
- **Training Accuracy**: 98.6%
- **Test Accuracy**: 97.9%
- **Total Features**: 17,128 TF-IDF features
- **Training Samples**: 16,640
- **Test Samples**: 4,160

### Improved Model (After Retraining)
The improved model uses:
- **Enhanced TF-IDF**: 20,000 features with bigrams
- **Hyperparameter Tuning**: GridSearchCV optimization
- **Better Preprocessing**: Advanced text normalization
- **Expected Accuracy**: 98%+

## 🏗️ Project Structure

```
Fake news prediction model/
│
├── app.py                          # Flask application
├── train_improved_model.py         # Model training script
├── requirements.txt                # Python dependencies
├── train.csv                       # Training dataset
│
├── model/
│   ├── fake_news_model.pkl        # Trained model
│   ├── tfidf_vectorizer.pkl       # TF-IDF vectorizer
│   └── Fake news prediction.ipynb # Original notebook
│
├── templates/
│   └── index.html                 # Main web interface
│
└── static/
    ├── styles.css                 # Glassmorphism styles
    └── script.js                  # Interactive animations
```

## 🎨 Frontend Features

### Design Elements
- **Color Scheme**: Purple gradient theme with glassmorphism
- **Typography**: Inter & Space Grotesk fonts
- **Animations**: 
  - Particle background animation
  - Scroll-triggered fade-in effects
  - Counter animations for statistics
  - Loading spinner
  - Confidence bar animation
  - Button hover effects

### Interactive Components
- Character counter for input
- Real-time form validation
- Smooth scroll navigation
- Parallax effects
- Typing placeholder animation
- Result card with confidence visualization

## 🔧 Customization

### Changing Colors
Edit `static/styles.css` and modify the CSS variables:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent-color: #667eea;
    /* Add your custom colors */
}
```

### Adjusting Model Parameters
Edit `train_improved_model.py`:
```python
vectorizer = TfidfVectorizer(
    max_features=20000,  # Adjust feature count
    ngram_range=(1, 2),  # Change n-gram range
    # ... other parameters
)
```

## 📈 Improvements Made

### Model Accuracy
1. ✅ **Fixed Preprocessing Bug**: The original app.py wasn't preprocessing text before prediction
2. ✅ **Added Confidence Scores**: Now shows prediction confidence
3. ✅ **Improved TF-IDF**: Added bigrams and optimized parameters
4. ✅ **Hyperparameter Tuning**: GridSearchCV for optimal model parameters
5. ✅ **Better Error Handling**: Comprehensive error messages

### Frontend Enhancements
1. ✅ **Glassmorphism Design**: Modern frosted glass UI
2. ✅ **Scroll Animations**: Smooth fade-in and slide-up effects
3. ✅ **Particle Background**: Animated background particles
4. ✅ **Interactive Elements**: Hover effects and transitions
5. ✅ **Responsive Design**: Mobile-friendly layout
6. ✅ **Loading Animations**: Visual feedback during processing
7. ✅ **Confidence Visualization**: Animated progress bar
8. ✅ **Statistics Counter**: Animated number counters

## 🐛 Troubleshooting

### Model Not Loading
```bash
# Retrain the model
python train_improved_model.py
```

### NLTK Stopwords Error
```python
import nltk
nltk.download('stopwords')
```

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Contact

For questions or feedback, please open an issue in the repository.

---

**Built with ❤️ using Flask, Scikit-learn, and Modern Web Technologies**
