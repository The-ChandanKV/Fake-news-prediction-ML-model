from flask import Flask, render_template, request, jsonify, send_file
import pickle
import numpy as np
import re
import urllib.parse
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
import os
import sys
import json
from datetime import datetime

# Fix Unicode output on Windows terminals
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Download stopwords if not already downloaded
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

app = Flask(__name__)

# Initialize Porter Stemmer
port_stem = PorterStemmer()

# Load trained model and vectorizer
model = None
vectorizer = None
model_loaded = False

# Global analysis counter
STATS_FILE = 'analysis_stats.json'


def load_stats():
    """Load persistent analysis statistics."""
    if os.path.isfile(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"total_analyses": 0, "fake_detected": 0, "real_detected": 0, "languages_analyzed": []}


def save_stats(stats):
    """Save analysis statistics."""
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f)
    except Exception:
        pass


def load_model():
    """Load the model and vectorizer"""
    global model, vectorizer, model_loaded
    try:
        model_path = 'model/fake_news_model.pkl'
        vectorizer_path = 'model/tfidf_vectorizer.pkl'
        
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            print("✗ Model files not found!")
            print("  Please run: python train_improved_model.py")
            return False
            
        model = pickle.load(open(model_path, 'rb'))
        vectorizer = pickle.load(open(vectorizer_path, 'rb'))
        model_loaded = True
        print("✓ Model and vectorizer loaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print("  The model may need to be retrained with your current Python environment.")
        print("  Run: python train_improved_model.py")
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
                                     prediction="Error: Model not loaded. Please retrain the model by running: python train_improved_model.py",
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
            # Note: In the dataset, 0 = Real (Reliable), 1 = Fake (Unreliable)
            if prediction == 0:
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


# ============================================================
# ENHANCED API v2: Full Analysis Pipeline
# ============================================================

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Enhanced API endpoint with full analysis pipeline"""
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
        
        # Check if URL was pasted instead of text
        from url_analysis import is_url, analyze_url, scrape_article_text
        url_analysis_result = None
        
        if is_url(news_text.strip()):
            # User pasted a URL - scrape and analyze
            url_analysis_result = analyze_url(news_text.strip())
            scraped = scrape_article_text(news_text.strip())
            
            if scraped and scraped.get("text"):
                news_text = scraped["text"]
                url_analysis_result["scraped_title"] = scraped.get("title", "")
                url_analysis_result["scraped_word_count"] = scraped.get("word_count", 0)
            else:
                return jsonify({
                    "error": "Could not extract article text from this URL. Please paste the article text directly.",
                    "url_analysis": url_analysis_result
                }), 400
        
        # Check language and translate if necessary
        from advanced_features import detect_language, translate_text, get_language_name
        
        orig_lang = detect_language(news_text)
        if orig_lang != 'en':
            translated_text, _, _ = translate_text(news_text, source_lang=orig_lang)
            text_to_analyze = translated_text
            lang_info = {"detected": orig_lang, "name": get_language_name(orig_lang), "translated": True}
        else:
            text_to_analyze = news_text
            lang_info = {"detected": "en", "name": "English", "translated": False}
            
        # Get source credibility if URLs/domains are found
        from advanced_features import check_source_credibility
        sources = check_source_credibility(text_to_analyze)
        
        # Look for fact checks
        from advanced_features import fact_check_google
        fact_checks = fact_check_google(text_to_analyze[:200])
        
        # Preprocess the text
        preprocessed_text = preprocess_text(text_to_analyze)
        
        # Transform and predict
        transformed_text = vectorizer.transform([preprocessed_text])
        raw_prediction = model.predict(transformed_text)[0]
        
        # Get confidence (probability of predicted class)
        warning = None
        try:
            prediction_proba = model.predict_proba(transformed_text)[0]
            # proba[0] = probability of Real (class 0), proba[1] = probability of Fake (class 1)
            prob_real = prediction_proba[0] * 100
            prob_fake = prediction_proba[1] * 100
            confidence = max(prob_real, prob_fake)
        except:
            prob_real = 50
            prob_fake = 50
            confidence = 50
        
        # === CONFIDENCE THRESHOLD LOGIC ===
        # Instead of binary, use 3-tier system:
        #   - "Likely Real News"     if prob_real >= 75%
        #   - "Likely Fake News"     if prob_fake >= 75%  (i.e. prob_real <= 25%)
        #   - "Uncertain"            if confidence is between 25-75% for either class
        if prob_real >= 75:
            verdict = "Likely Real News"
            label = 0
        elif prob_fake >= 75:
            verdict = "Likely Fake News"
            label = 1
        else:
            verdict = "Uncertain — Could not determine reliably"
            label = 2  # Special label for uncertain
            warning = "Model confidence is low. This article may be outside the model's training domain."
            
        # Get explainability features
        from advanced_features import explain_prediction
        explanation = explain_prediction(text_to_analyze, vectorizer, model, preprocess_text)
        
        # NEW: Sentiment & manipulation analysis
        from sentiment_analysis import full_content_analysis
        content_analysis = full_content_analysis(text_to_analyze)
        
        # NEW: URL analysis (if URL detected in text)
        if not url_analysis_result:
            urls_in_text = re.findall(r'https?://[^\s]+', text_to_analyze)
            if urls_in_text:
                url_analysis_result = analyze_url(urls_in_text[0])
        
        # Update global stats
        stats = load_stats()
        stats["total_analyses"] = stats.get("total_analyses", 0) + 1
        if label == 0:
            stats["real_detected"] = stats.get("real_detected", 0) + 1
        elif label == 1:
            stats["fake_detected"] = stats.get("fake_detected", 0) + 1
        # label==2 (uncertain) doesn't count toward fake or real
        if lang_info["detected"] not in stats.get("languages_analyzed", []):
            stats.setdefault("languages_analyzed", []).append(lang_info["detected"])
        save_stats(stats)

        # Log to analytics engine
        try:
            from analytics import log_prediction
            domain = sources[0]["domain"] if sources else None
            log_prediction(
                verdict=verdict,
                confidence=confidence,
                domain=domain,
                lang=lang_info["detected"]
            )
        except Exception:
            pass
        
        # Calculate overall trust score (weighted combination)
        # For uncertain predictions, use the raw confidence as-is
        ml_trust = round(prob_real, 1)  # Higher = more trustworthy
        trust_components = {
            "ml_prediction": ml_trust,
            "content_analysis": round(content_analysis["content_credibility"], 1),
            "manipulation_inverse": round(100 - content_analysis["manipulation"]["score"], 1),
            "writing_quality": content_analysis["writing_quality"]["score"]
        }
        
        overall_trust = (
            trust_components["ml_prediction"] * 0.45 +
            trust_components["content_analysis"] * 0.20 +
            trust_components["manipulation_inverse"] * 0.20 +
            trust_components["writing_quality"] * 0.15
        )
        
        result = {
            "prediction": verdict,
            "confidence": round(confidence, 2),
            "label": label,
            "prob_real": round(prob_real, 2),
            "prob_fake": round(prob_fake, 2),
            "overall_trust_score": round(overall_trust, 1),
            "trust_components": trust_components,
            "language": lang_info,
            "sources": sources,
            "fact_checks": fact_checks,
            "explanation": explanation,
            "content_analysis": content_analysis,
            "url_analysis": url_analysis_result,
            "analyzed_at": datetime.now().isoformat(),
            "text_preview": text_to_analyze[:200] + "..." if len(text_to_analyze) > 200 else text_to_analyze
        }
        
        if warning:
            result["warning"] = warning
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/trending", methods=["GET"])
def api_trending():
    """API endpoint to get trending news topics with predictions"""
    try:
        from advanced_features import get_trending_topics, analyze_trending_with_model
        # Get topics
        topics = get_trending_topics()
        # Analyze with model
        analyzed_topics = analyze_trending_with_model(topics, vectorizer, model, preprocess_text)
        
        return jsonify({
            "success": True,
            "topics": analyzed_topics
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    """API endpoint to receive user feedback on predictions"""
    try:
        data = request.get_json()
        news_text = data.get("text", "")
        predicted_label = data.get("label", -1)
        is_correct = data.get("correct", True)
        
        if not news_text or predicted_label == -1:
            return jsonify({"error": "Invalid data"}), 400
            
        # Invert label if prediction was wrong
        actual_label = predicted_label if is_correct else (1 - predicted_label)
        
        # Save to CSV
        file_path = 'user_feedback.csv'
        file_exists = os.path.isfile(file_path)
        
        import csv
        with open(file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                # Add headers compatible with train_improved_model.py
                writer.writerow(['title', 'author', 'label'])
            
            # Save the text in the 'title' column since train_improved_model.py uses author+title
            writer.writerow([news_text, 'User Feedback', actual_label])

        # Log feedback to analytics engine
        try:
            from analytics import log_feedback
            log_feedback(is_correct)
        except Exception:
            pass

        return jsonify({"success": True, "message": "Feedback saved for the next training cycle!"})
        
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/fetch-news", methods=["POST"])
def api_fetch_news():
    """API endpoint to fetch latest real-world news for retraining"""
    try:
        from fetch_news import fetch_all_news
        result = fetch_all_news()
        return jsonify({
            "success": True,
            "new_articles": result["new_articles"],
            "total_articles": result["total_articles"],
            "message": f"Fetched {result['new_articles']} new articles! Total: {result['total_articles']}"
        })
    except Exception as e:
        print(f"Error fetching news: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/fetch-status")
def api_fetch_status():
    """Get status of fetched news data"""
    try:
        status = {
            "total_fetched": 0,
            "total_feedback": 0,
            "last_fetch": None
        }
        
        # Check fetched news
        if os.path.isfile('fetched_news.csv'):
            with open('fetched_news.csv', 'r', encoding='utf-8') as f:
                status["total_fetched"] = max(0, sum(1 for _ in f) - 1)
        
        # Check user feedback
        if os.path.isfile('user_feedback.csv'):
            with open('user_feedback.csv', 'r', encoding='utf-8') as f:
                status["total_feedback"] = max(0, sum(1 for _ in f) - 1)
        
        # Check fetch log
        if os.path.isfile('fetch_log.json'):
            with open('fetch_log.json', 'r') as f:
                log = json.load(f)
                status["last_fetch"] = log.get("last_fetch")
        
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats")
def api_stats():
    """Global platform statistics for the dashboard"""
    from analytics import get_dashboard_stats
    return jsonify(get_dashboard_stats())


@app.route("/api/heatmap", methods=["POST"])
def api_heatmap():
    """
    LIME-style word heatmap: returns the original text annotated
    with per-word importance scores for inline highlighting.
    """
    try:
        if not model_loaded:
            return jsonify({"error": "Model not loaded"}), 503

        data = request.get_json()
        text = data.get("text", "")
        if not text or len(text.strip()) < 10:
            return jsonify({"error": "Text too short"}), 400

        coef = model.coef_[0]
        features = vectorizer.get_feature_names_out()

        # Build word → coefficient lookup
        word_coef = {features[i]: float(coef[i]) for i in range(len(features))}

        # Tokenize original text preserving spacing
        tokens = re.findall(r'\S+|\s+', text)

        max_abs = max((abs(v) for v in word_coef.values()), default=1)

        from nltk.stem.porter import PorterStemmer
        ps = PorterStemmer()
        annotated = []
        for token in tokens:
            word = token.strip().lower()
            word_clean = re.sub(r'[^a-z]', '', word)
            stem = ps.stem(word_clean) if word_clean else ''
            score = word_coef.get(stem, word_coef.get(word_clean, 0.0))
            norm = round(float(score) / max_abs, 4) if max_abs != 0 else 0.0
            annotated.append({"token": token, "score": norm})

        return jsonify({"success": True, "annotated": annotated})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/ipr-check", methods=["POST"])
def api_ipr_check():
    """
    IPR Content Originality Analysis.
    Returns originality score, key phrases, and writing pattern flags.
    """
    try:
        data = request.get_json()
        text = data.get("text", "")
        check_online = data.get("check_online", False)  # opt-in for slower web check
        if not text or len(text.strip()) < 30:
            return jsonify({"error": "Text too short for IPR analysis"}), 400
        from ipr_checker import compute_originality_score
        result = compute_originality_score(text, check_online=check_online)
        return jsonify({"success": True, "ipr": result})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/share-card", methods=["POST"])
def api_share_card():
    """
    Generate a shareable text summary (for WhatsApp, Twitter, etc.).
    Returns a formatted share text + deep-link.
    """
    try:
        data = request.get_json()
        verdict = data.get("prediction", "Unknown")
        confidence = data.get("confidence", 0)
        lang = data.get("language", {}).get("name", "English")
        trust = data.get("overall_trust_score", 0)
        preview = data.get("text_preview", "")[:120]

        emoji = "🚨" if "Fake" in verdict else "✅"
        share_text = (
            f"{emoji} *FakeDetect AI Verdict*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📰 Article: \"{preview}...\"\n"
            f"🔍 Verdict: *{verdict}*\n"
            f"📊 Confidence: {confidence:.1f}%\n"
            f"🛡️ Trust Score: {trust}/100\n"
            f"🌍 Language: {lang}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Verified by FakeDetect AI — fakedetect.ai\n"
            f"Try it yourself 👇"
        )
        whatsapp_url = "https://wa.me/?text=" + urllib.parse.quote(share_text) if True else ""
        return jsonify({"success": True, "share_text": share_text, "whatsapp_url": whatsapp_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/dashboard")
def dashboard():
    """Analytics dashboard page"""
    return render_template("dashboard.html")


@app.route("/api-docs")
def api_docs_page():
    """API documentation page"""
    return render_template("api_docs.html")


@app.route("/api/analyze-url", methods=["POST"])
def api_analyze_url():
    """Dedicated URL analysis endpoint"""
    try:
        data = request.get_json()
        url = data.get("url", "")
        
        if not url:
            return jsonify({"error": "Please provide a URL"}), 400
        
        from url_analysis import analyze_url, scrape_article_text
        
        url_signals = analyze_url(url)
        scraped = scrape_article_text(url)
        
        result = {
            "url_analysis": url_signals,
            "scraped": {
                "title": scraped.get("title", "") if scraped else "",
                "word_count": scraped.get("word_count", 0) if scraped else 0,
                "available": scraped is not None
            }
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/report", methods=["POST"])
def api_generate_report():
    """Generate a comprehensive analysis report for sharing/download"""
    try:
        data = request.get_json()
        analysis_data = data.get("analysis", {})
        
        if not analysis_data:
            return jsonify({"error": "No analysis data provided"}), 400
        
        report = {
            "title": "FakeDetect AI — Analysis Report",
            "generated_at": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            "verdict": analysis_data.get("prediction", "Unknown"),
            "confidence": analysis_data.get("confidence", 0),
            "overall_trust": analysis_data.get("overall_trust_score", 0),
            "sentiment": analysis_data.get("content_analysis", {}).get("sentiment", {}),
            "manipulation": analysis_data.get("content_analysis", {}).get("manipulation", {}),
            "writing_quality": analysis_data.get("content_analysis", {}).get("writing_quality", {}),
            "text_preview": analysis_data.get("text_preview", ""),
            "sources": analysis_data.get("sources", []),
            "fact_checks": analysis_data.get("fact_checks", []),
            "report_id": f"FD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        return jsonify({"success": True, "report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded,
        "version": "3.0.0",
        "features": [
            "multi_language", "fact_check", "source_credibility",
            "explainability", "sentiment_analysis", "manipulation_detection",
            "url_analysis", "trending_topics", "dynamic_learning"
        ]
    })

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🛡️  FAKEDETECT AI — Fake News Detection Platform")
    print("=" * 60)
    if model_loaded:
        print("✓ Model Status: READY")
        print("✓ Features: Sentiment | Manipulation | URL | Explainability")
        print("✓ Server starting...")
    else:
        print("✗ Model Status: NOT LOADED")
        print("  To train the model, run: python train_improved_model.py")
        print("  The app will still start but predictions won't work.")
    print("=" * 60 + "\n")
    
    # Use PORT env variable for Railway, default to 5000 for local dev
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)