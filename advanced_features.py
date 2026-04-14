"""
Advanced Features Module for Fake News Detector
Implements: Multi-Language, Fact-Check, Source Credibility, Explainability, Trending Analysis
"""

import re
import json
import urllib.request
import urllib.parse
import urllib.error
import numpy as np
from datetime import datetime


# ============================================================
# 1. MULTI-LANGUAGE SUPPORT
# ============================================================

def detect_language(text):
    """Detect the language of the input text using langdetect."""
    try:
        from langdetect import detect, DetectorFactory
        DetectorFactory.seed = 0  # For consistent results
        lang = detect(text)
        return lang
    except Exception:
        return "en"


def translate_text(text, source_lang="auto"):
    """
    Translate text to English using deep-translator (Google Translate, free).
    Returns translated text + detected source language.
    """
    if source_lang == "en":
        return text, "en", False  # Already English

    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source=source_lang, target='en')

        # deep-translator has a 5000 char limit per request, chunk if needed
        if len(text) > 4500:
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translated_chunks = [translator.translate(chunk) for chunk in chunks]
            translated = " ".join(translated_chunks)
        else:
            translated = translator.translate(text)

        return translated, source_lang, True
    except ImportError:
        return text, source_lang, False
    except Exception as e:
        print(f"Translation error: {e}")
        return text, source_lang, False


LANGUAGE_NAMES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "hi": "Hindi", "ar": "Arabic",
    "zh-cn": "Chinese", "ja": "Japanese", "ko": "Korean", "ru": "Russian",
    "nl": "Dutch", "sv": "Swedish", "tr": "Turkish", "pl": "Polish",
    "th": "Thai", "vi": "Vietnamese", "id": "Indonesian", "ms": "Malay",
    "bn": "Bengali", "ta": "Tamil", "te": "Telugu", "kn": "Kannada",
    "mr": "Marathi", "gu": "Gujarati", "ml": "Malayalam", "pa": "Punjabi",
    "ur": "Urdu", "fa": "Persian", "uk": "Ukrainian", "cs": "Czech",
    "ro": "Romanian", "hu": "Hungarian", "el": "Greek", "he": "Hebrew",
    "da": "Danish", "fi": "Finnish", "no": "Norwegian", "sk": "Slovak",
    "bg": "Bulgarian", "hr": "Croatian", "sr": "Serbian", "sl": "Slovenian",
    "lt": "Lithuanian", "lv": "Latvian", "et": "Estonian",
}


def get_language_name(code):
    """Get the full language name from a language code."""
    return LANGUAGE_NAMES.get(code, code.upper())


# ============================================================
# 2. FACT-CHECK VERIFICATION
# ============================================================

def fact_check_google(query, max_results=5):
    """
    Query Google Fact Check Tools API (free, no key required for basic usage).
    Returns list of fact-check results.
    """
    try:
        encoded_query = urllib.parse.quote(query[:200])  # Limit query length
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={encoded_query}&languageCode=en"

        req = urllib.request.Request(url, headers={
            "User-Agent": "FakeNewsDetector/2.0"
        })

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        results = []
        for claim in data.get("claims", [])[:max_results]:
            review = claim.get("claimReview", [{}])[0]
            results.append({
                "claim": claim.get("text", ""),
                "claimant": claim.get("claimant", "Unknown"),
                "rating": review.get("textualRating", "Unknown"),
                "publisher": review.get("publisher", {}).get("name", "Unknown"),
                "url": review.get("url", ""),
                "title": review.get("title", ""),
                "date": claim.get("claimDate", "")
            })

        return results

    except urllib.error.HTTPError:
        return []
    except Exception as e:
        print(f"Fact check error: {e}")
        return []


def fact_check_claimbuster(text):
    """
    Score claim-worthiness using ClaimBuster API (free).
    Returns a score 0-1 indicating how likely the text contains a checkable claim.
    """
    try:
        url = "https://idir.uta.edu/claimbuster/api/v2/score/text/"
        data = json.dumps({"input_text": text[:500]}).encode('utf-8')

        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "User-Agent": "FakeNewsDetector/2.0"
        })

        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())

        scores = result.get("results", [])
        if scores:
            avg_score = sum(s.get("score", 0) for s in scores) / len(scores)
            return round(avg_score, 3)
        return 0.0

    except Exception as e:
        print(f"ClaimBuster error: {e}")
        return None


# ============================================================
# 3. SOURCE CREDIBILITY CHECKER
# ============================================================

# Database of known news sources with trust scores (0-100)
SOURCE_CREDIBILITY_DB = {
    # Highly Reliable (80-100)
    "reuters.com": {"score": 95, "bias": "Center", "name": "Reuters"},
    "apnews.com": {"score": 95, "bias": "Center", "name": "AP News"},
    "bbc.com": {"score": 90, "bias": "Center-Left", "name": "BBC"},
    "bbc.co.uk": {"score": 90, "bias": "Center-Left", "name": "BBC"},
    "nytimes.com": {"score": 87, "bias": "Center-Left", "name": "New York Times"},
    "washingtonpost.com": {"score": 85, "bias": "Center-Left", "name": "Washington Post"},
    "theguardian.com": {"score": 85, "bias": "Center-Left", "name": "The Guardian"},
    "wsj.com": {"score": 88, "bias": "Center-Right", "name": "Wall Street Journal"},
    "economist.com": {"score": 90, "bias": "Center", "name": "The Economist"},
    "npr.org": {"score": 88, "bias": "Center-Left", "name": "NPR"},
    "pbs.org": {"score": 88, "bias": "Center", "name": "PBS"},
    "nature.com": {"score": 95, "bias": "Center", "name": "Nature"},
    "sciencemag.org": {"score": 95, "bias": "Center", "name": "Science"},
    "thehindu.com": {"score": 82, "bias": "Center-Left", "name": "The Hindu"},
    "ndtv.com": {"score": 78, "bias": "Center-Left", "name": "NDTV"},
    "timesofindia.indiatimes.com": {"score": 75, "bias": "Center", "name": "Times of India"},
    "hindustantimes.com": {"score": 75, "bias": "Center", "name": "Hindustan Times"},
    "indianexpress.com": {"score": 80, "bias": "Center", "name": "Indian Express"},

    # Moderately Reliable (50-79)
    "cnn.com": {"score": 72, "bias": "Left", "name": "CNN"},
    "foxnews.com": {"score": 58, "bias": "Right", "name": "Fox News"},
    "msnbc.com": {"score": 60, "bias": "Left", "name": "MSNBC"},
    "huffpost.com": {"score": 60, "bias": "Left", "name": "HuffPost"},
    "dailymail.co.uk": {"score": 50, "bias": "Right", "name": "Daily Mail"},
    "nypost.com": {"score": 55, "bias": "Right", "name": "New York Post"},
    "buzzfeednews.com": {"score": 62, "bias": "Left", "name": "BuzzFeed News"},
    "vice.com": {"score": 58, "bias": "Left", "name": "Vice"},

    # Low Reliability (0-49)
    "infowars.com": {"score": 10, "bias": "Far-Right", "name": "InfoWars"},
    "breitbart.com": {"score": 25, "bias": "Far-Right", "name": "Breitbart"},
    "naturalnews.com": {"score": 8, "bias": "Far-Right", "name": "Natural News"},
    "theonion.com": {"score": 5, "bias": "Satire", "name": "The Onion"},
    "babylonbee.com": {"score": 5, "bias": "Satire", "name": "Babylon Bee"},
    "worldnewsdailyreport.com": {"score": 3, "bias": "Satire/Fake", "name": "World News Daily Report"},
    "beforeitsnews.com": {"score": 10, "bias": "Conspiracy", "name": "Before It's News"},
    "yournewswire.com": {"score": 5, "bias": "Conspiracy/Fake", "name": "YourNewsWire"},
}


def extract_urls(text):
    """Extract URLs and domain names from text."""
    url_pattern = r'https?://(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    urls = re.findall(url_pattern, text)

    # Also try to match source names in the text
    source_mentions = []
    for domain, info in SOURCE_CREDIBILITY_DB.items():
        name = info["name"].lower()
        if name in text.lower():
            source_mentions.append(domain)

    return list(set(urls + source_mentions))


def check_source_credibility(text):
    """
    Analyze source credibility from text.
    Returns a list of found sources with their trust scores.
    """
    domains = extract_urls(text)
    results = []

    for domain in domains:
        # Clean domain
        domain_clean = domain.lower().strip()

        # Direct match
        if domain_clean in SOURCE_CREDIBILITY_DB:
            info = SOURCE_CREDIBILITY_DB[domain_clean]
            results.append({
                "domain": domain_clean,
                "name": info["name"],
                "score": info["score"],
                "bias": info["bias"],
                "tier": get_credibility_tier(info["score"])
            })
        else:
            # Check if it's a subdomain of a known source
            for known_domain, info in SOURCE_CREDIBILITY_DB.items():
                if domain_clean.endswith(known_domain):
                    results.append({
                        "domain": domain_clean,
                        "name": info["name"],
                        "score": info["score"],
                        "bias": info["bias"],
                        "tier": get_credibility_tier(info["score"])
                    })
                    break

    return results


def get_credibility_tier(score):
    """Get a human-readable tier from a credibility score."""
    if score >= 80:
        return "Highly Reliable"
    elif score >= 60:
        return "Generally Reliable"
    elif score >= 40:
        return "Mixed Reliability"
    elif score >= 20:
        return "Low Reliability"
    else:
        return "Unreliable / Satire"


# ============================================================
# 4. EXPLAINABILITY / TRANSPARENCY
# ============================================================

def explain_prediction(text, vectorizer, model, preprocessor, top_n=15):
    """
    Explain why the model made a specific prediction by analyzing
    TF-IDF feature weights × model coefficients.
    Returns the most influential words for both fake and real classification.
    """
    try:
        # Preprocess the text
        processed = preprocessor(text)

        # Vectorize
        tfidf_vector = vectorizer.transform([processed])

        # Get model coefficients (for binary classification)
        coefficients = model.coef_[0]

        # Get feature names
        feature_names = vectorizer.get_feature_names_out()

        # Get non-zero features in this text
        non_zero_indices = tfidf_vector.nonzero()[1]

        # Calculate impact = tfidf_weight * coefficient
        word_impacts = []
        for idx in non_zero_indices:
            word = feature_names[idx]
            tfidf_weight = tfidf_vector[0, idx]
            coef = coefficients[idx]
            impact = tfidf_weight * coef
            word_impacts.append({
                "word": word,
                "impact": round(float(impact), 4),
                "tfidf": round(float(tfidf_weight), 4),
                "coefficient": round(float(coef), 4),
                "direction": "fake" if coef > 0 else "real"
            })

        # Sort by absolute impact
        word_impacts.sort(key=lambda x: abs(x["impact"]), reverse=True)

        # Separate into fake-leaning and real-leaning words
        fake_words = [w for w in word_impacts if w["direction"] == "fake"][:top_n]
        real_words = [w for w in word_impacts if w["direction"] == "real"][:top_n]

        return {
            "top_words": word_impacts[:top_n],
            "fake_indicators": fake_words[:8],
            "real_indicators": real_words[:8],
            "total_features": len(non_zero_indices)
        }

    except Exception as e:
        print(f"Explainability error: {e}")
        return None


# ============================================================
# 5. TRENDING TOPICS ANALYSIS
# ============================================================

def get_trending_topics():
    """
    Fetch trending news topics from RSS feeds and analyze them.
    Returns categorized trending topics.
    """
    import xml.etree.ElementTree as ET

    feeds = [
        ("World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
        ("Technology", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
        ("Politics", "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"),
        ("Science", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
        ("Business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
        ("Health", "https://feeds.bbci.co.uk/news/health/rss.xml"),
    ]

    topics = []

    for category, feed_url in feeds:
        try:
            req = urllib.request.Request(feed_url, headers={
                "User-Agent": "Mozilla/5.0 FakeNewsDetector/2.0"
            })
            with urllib.request.urlopen(req, timeout=8) as response:
                content = response.read().decode("utf-8", errors="replace")

            # Parse RSS XML
            root = ET.fromstring(content)

            items = root.findall('.//item')[:5]  # Top 5 per category
            for item in items:
                title_el = item.find('title')
                desc_el = item.find('description')
                link_el = item.find('link')
                pub_date_el = item.find('pubDate')

                if title_el is not None and title_el.text:
                    title = title_el.text.strip()
                    # Clean CDATA
                    title = title.replace("<![CDATA[", "").replace("]]>", "")

                    topics.append({
                        "title": title,
                        "description": (desc_el.text or "")[:200] if desc_el is not None else "",
                        "category": category,
                        "link": link_el.text if link_el is not None else "",
                        "published": pub_date_el.text if pub_date_el is not None else "",
                        "source": "BBC" if "bbc" in feed_url else "NYT"
                    })

        except Exception as e:
            print(f"RSS error ({category}): {e}")

    return topics


def analyze_trending_with_model(topics, vectorizer, model, preprocessor):
    """
    Run each trending topic through the fake news model.
    Returns topics with prediction scores.
    """
    analyzed = []

    for topic in topics:
        try:
            text = topic["title"]
            processed = preprocessor(text)
            vector = vectorizer.transform([processed])
            prediction = model.predict(vector)[0]

            try:
                proba = model.predict_proba(vector)[0]
                confidence = round(max(proba) * 100, 1)
                fake_prob = round(proba[1] * 100, 1) if len(proba) > 1 else 0
            except Exception:
                confidence = 75.0
                fake_prob = 50.0

            analyzed.append({
                **topic,
                "prediction": "Real" if prediction == 0 else "Fake",
                "confidence": confidence,
                "fake_probability": fake_prob,
                "risk_level": "Low" if fake_prob < 30 else "Medium" if fake_prob < 60 else "High"
            })

        except Exception as e:
            print(f"Analysis error for topic: {e}")
            analyzed.append({**topic, "prediction": "Unknown", "confidence": 0, "fake_probability": 50, "risk_level": "Unknown"})

    return analyzed
