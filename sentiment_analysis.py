"""
Sentiment & Emotional Manipulation Analysis Module
Adds deep content analysis beyond ML prediction:
- Sentiment polarity & subjectivity
- Emotional manipulation score
- Clickbait detection
- Writing quality analysis
"""

import re
import math


# ============================================================
# 1. SENTIMENT ANALYSIS (No external dependency fallback)
# ============================================================

# VADER-like lexicon subset for sentiment analysis
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love',
    'happy', 'joy', 'best', 'beautiful', 'success', 'successful', 'win',
    'positive', 'hope', 'benefit', 'improve', 'progress', 'achievement',
    'breakthrough', 'innovative', 'outstanding', 'remarkable', 'brilliant',
    'celebrate', 'proud', 'grateful', 'inspiring', 'optimistic', 'thriving',
    'growth', 'recovery', 'support', 'enhanced', 'advanced', 'superior'
}

NEGATIVE_WORDS = {
    'bad', 'terrible', 'horrible', 'awful', 'worst', 'hate', 'kill',
    'death', 'dead', 'die', 'destroy', 'attack', 'war', 'crisis',
    'danger', 'threat', 'fear', 'scary', 'evil', 'crime', 'criminal',
    'corrupt', 'scandal', 'fraud', 'fake', 'lie', 'lies', 'hoax',
    'conspiracy', 'disaster', 'catastrophe', 'plague', 'pandemic',
    'collapse', 'crash', 'devastate', 'shocking', 'outrage', 'alarming',
    'terrifying', 'nightmare', 'toxic', 'violent', 'brutal', 'chaos'
}

INTENSIFIERS = {
    'very', 'extremely', 'incredibly', 'absolutely', 'totally', 'completely',
    'utterly', 'highly', 'deeply', 'truly', 'really', 'seriously'
}

NEGATORS = {
    'not', 'no', 'never', 'neither', 'nobody', 'nothing', 'nowhere',
    'nor', 'cannot', "can't", "won't", "don't", "doesn't", "didn't",
    "isn't", "aren't", "wasn't", "weren't"
}


def analyze_sentiment(text):
    """
    Analyze sentiment of text using a lexicon-based approach.
    Returns polarity (-1 to 1), subjectivity (0 to 1), and label.
    Falls back to TextBlob if available.
    """
    try:
        from textblob import TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
    except ImportError:
        polarity, subjectivity = _lexicon_sentiment(text)
    
    # Determine label
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    
    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "label": label,
        "polarity_pct": round(abs(polarity) * 100, 1),
        "subjectivity_pct": round(subjectivity * 100, 1)
    }


def _lexicon_sentiment(text):
    """Fallback lexicon-based sentiment analysis."""
    words = text.lower().split()
    pos_count = 0
    neg_count = 0
    intensifier_boost = 0
    total_words = len(words) if words else 1
    
    for i, word in enumerate(words):
        # Check for negator in previous 3 words
        is_negated = any(words[max(0, i-j)] in NEGATORS 
                        for j in range(1, min(4, i+1)))
        is_intensified = any(words[max(0, i-j)] in INTENSIFIERS 
                            for j in range(1, min(3, i+1)))
        
        multiplier = 1.5 if is_intensified else 1.0
        
        if word in POSITIVE_WORDS:
            if is_negated:
                neg_count += multiplier
            else:
                pos_count += multiplier
        elif word in NEGATIVE_WORDS:
            if is_negated:
                pos_count += multiplier
            else:
                neg_count += multiplier
    
    # Calculate polarity (-1 to 1)
    total_sentiment = pos_count + neg_count
    if total_sentiment == 0:
        polarity = 0.0
    else:
        polarity = (pos_count - neg_count) / total_sentiment
    
    # Calculate subjectivity (0 to 1) - ratio of sentiment words to total
    subjectivity = min(1.0, total_sentiment / (total_words * 0.3))
    
    return polarity, subjectivity


# ============================================================
# 2. EMOTIONAL MANIPULATION DETECTION
# ============================================================

MANIPULATION_PATTERNS = {
    "excessive_caps": {
        "desc": "Excessive use of ALL CAPS (shouting)",
        "weight": 2.0
    },
    "excessive_exclamation": {
        "desc": "Overuse of exclamation marks (!!!) for emotional impact",
        "weight": 1.5
    },
    "fear_mongering": {
        "desc": "Fear-inducing language designed to provoke anxiety",
        "weight": 2.5
    },
    "urgency_pressure": {
        "desc": "Creates artificial urgency to bypass critical thinking",
        "weight": 2.0
    },
    "us_vs_them": {
        "desc": "Divisive 'us vs them' framing to create tribal conflict",
        "weight": 2.0
    },
    "appeal_to_emotion": {
        "desc": "Emotional manipulation through loaded language",
        "weight": 1.5
    },
    "conspiracy_language": {
        "desc": "Conspiracy theory language patterns",
        "weight": 3.0
    },
    "clickbait_patterns": {
        "desc": "Clickbait phrasing designed to manipulate clicks",
        "weight": 1.5
    }
}

FEAR_WORDS = {
    'warning', 'alert', 'danger', 'deadly', 'fatal', 'terrifying',
    'alarming', 'emergency', 'catastrophic', 'devastating', 'nightmare',
    'horrifying', 'shocking', 'outrageous', 'unbelievable', 'disturbing',
    'panic', 'chaos', 'collapse', 'apocalypse', 'doomsday', 'plague'
}

URGENCY_WORDS = {
    'breaking', 'urgent', 'immediately', 'now', 'hurry', 'act now',
    'before it\'s too late', 'last chance', 'limited time', 'while you still can',
    'must see', 'must read', 'share before deleted', 'they don\'t want you to know',
    'spread the word', 'everyone needs to see'
}

CONSPIRACY_PHRASES = {
    'they don\'t want you to know', 'mainstream media won\'t tell you',
    'the truth they\'re hiding', 'wake up', 'open your eyes', 'sheeple',
    'deep state', 'new world order', 'cover up', 'big pharma',
    'what they\'re not telling you', 'hidden agenda', 'suppressed information',
    'the real truth', 'exposed', 'bombshell', 'government doesn\'t want'
}

CLICKBAIT_PATTERNS = [
    r'you won\'?t believe',
    r'what happens next',
    r'doctors hate',
    r'one weird trick',
    r'shocking truth',
    r'number \d+ will (?:shock|surprise|amaze)',
    r'this (?:changes|destroys|proves) everything',
    r'\d+ (?:reasons|things|ways|facts) (?:you|that)',
    r'what .+ don\'?t want you to (?:know|see)',
    r'exposed[!:.]',
    r'gone wrong',
    r'is (?:dead|dying|over)',
]

US_VS_THEM_WORDS = {
    'they', 'them', 'those people', 'the enemy', 'traitors',
    'patriots', 'real americans', 'true believers', 'outsiders',
    'elites', 'the establishment', 'the other side'
}


def detect_manipulation(text):
    """
    Detect emotional manipulation patterns in text.
    Returns a manipulation score (0-100) and detailed breakdown.
    """
    findings = []
    total_score = 0
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words) if words else 1
    
    # 1. Excessive CAPS
    caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
    caps_ratio = len(caps_words) / word_count
    if caps_ratio > 0.1:
        score = min(10, caps_ratio * 50)
        findings.append({
            "pattern": "excessive_caps",
            "description": MANIPULATION_PATTERNS["excessive_caps"]["desc"],
            "severity": "high" if caps_ratio > 0.3 else "medium",
            "score": round(score, 1),
            "examples": caps_words[:5]
        })
        total_score += score * MANIPULATION_PATTERNS["excessive_caps"]["weight"]
    
    # 2. Excessive exclamation marks
    exclamation_count = text.count('!')
    excl_ratio = exclamation_count / max(len(text.split('.')), 1)
    if excl_ratio > 0.5:
        score = min(10, excl_ratio * 5)
        findings.append({
            "pattern": "excessive_exclamation",
            "description": MANIPULATION_PATTERNS["excessive_exclamation"]["desc"],
            "severity": "high" if excl_ratio > 2 else "medium",
            "score": round(score, 1)
        })
        total_score += score * MANIPULATION_PATTERNS["excessive_exclamation"]["weight"]
    
    # 3. Fear-mongering
    fear_found = [w for w in FEAR_WORDS if w in text_lower]
    if fear_found:
        score = min(10, len(fear_found) * 2)
        findings.append({
            "pattern": "fear_mongering",
            "description": MANIPULATION_PATTERNS["fear_mongering"]["desc"],
            "severity": "high" if len(fear_found) > 3 else "medium" if len(fear_found) > 1 else "low",
            "score": round(score, 1),
            "examples": fear_found[:5]
        })
        total_score += score * MANIPULATION_PATTERNS["fear_mongering"]["weight"]
    
    # 4. Urgency/pressure
    urgency_found = [w for w in URGENCY_WORDS if w in text_lower]
    if urgency_found:
        score = min(10, len(urgency_found) * 3)
        findings.append({
            "pattern": "urgency_pressure",
            "description": MANIPULATION_PATTERNS["urgency_pressure"]["desc"],
            "severity": "high" if len(urgency_found) > 2 else "medium",
            "score": round(score, 1),
            "examples": urgency_found[:5]
        })
        total_score += score * MANIPULATION_PATTERNS["urgency_pressure"]["weight"]
    
    # 5. Conspiracy language
    conspiracy_found = [p for p in CONSPIRACY_PHRASES if p in text_lower]
    if conspiracy_found:
        score = min(10, len(conspiracy_found) * 4)
        findings.append({
            "pattern": "conspiracy_language",
            "description": MANIPULATION_PATTERNS["conspiracy_language"]["desc"],
            "severity": "high",
            "score": round(score, 1),
            "examples": conspiracy_found[:3]
        })
        total_score += score * MANIPULATION_PATTERNS["conspiracy_language"]["weight"]
    
    # 6. Clickbait patterns
    clickbait_matches = []
    for pattern in CLICKBAIT_PATTERNS:
        if re.search(pattern, text_lower):
            clickbait_matches.append(pattern)
    if clickbait_matches:
        score = min(10, len(clickbait_matches) * 3)
        findings.append({
            "pattern": "clickbait_patterns",
            "description": MANIPULATION_PATTERNS["clickbait_patterns"]["desc"],
            "severity": "high" if len(clickbait_matches) > 2 else "medium",
            "score": round(score, 1)
        })
        total_score += score * MANIPULATION_PATTERNS["clickbait_patterns"]["weight"]
    
    # 7. Us vs Them
    us_vs_found = [w for w in US_VS_THEM_WORDS if w in text_lower]
    # More nuanced - only flag if combined with negative sentiment
    if len(us_vs_found) > 1:
        score = min(10, len(us_vs_found) * 2)
        findings.append({
            "pattern": "us_vs_them",
            "description": MANIPULATION_PATTERNS["us_vs_them"]["desc"],
            "severity": "medium",
            "score": round(score, 1),
            "examples": us_vs_found[:5]
        })
        total_score += score * MANIPULATION_PATTERNS["us_vs_them"]["weight"]
    
    # Normalize final score to 0-100
    manipulation_score = min(100, total_score)
    
    if manipulation_score >= 60:
        verdict = "High Manipulation"
        verdict_color = "#ef4444"
    elif manipulation_score >= 30:
        verdict = "Moderate Manipulation"
        verdict_color = "#f59e0b"
    elif manipulation_score >= 10:
        verdict = "Low Manipulation"
        verdict_color = "#3b82f6"
    else:
        verdict = "Minimal Manipulation"
        verdict_color = "#22c55e"
    
    return {
        "score": round(manipulation_score, 1),
        "verdict": verdict,
        "verdict_color": verdict_color,
        "findings": findings,
        "total_patterns_found": len(findings)
    }


# ============================================================
# 3. WRITING QUALITY ANALYSIS
# ============================================================

def analyze_writing_quality(text):
    """
    Analyze the writing quality of the text.
    Poor writing quality often correlates with fake news.
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    word_count = len(words)
    sentence_count = len(sentences) if sentences else 1
    
    # Average sentence length
    avg_sentence_len = word_count / sentence_count
    
    # Vocabulary richness (type-token ratio)
    unique_words = set(w.lower() for w in words if w.isalpha())
    vocab_richness = len(unique_words) / max(word_count, 1)
    
    # Spelling heuristics (words with unusual patterns)
    # Count words that are likely misspellings (all lowercase, with numbers mixed in)
    mixed_alpha_num = len([w for w in words if re.match(r'^[a-zA-Z]+\d+[a-zA-Z]*$', w)])
    
    # Readability approximation (Flesch-Kincaid-like)
    avg_word_len = sum(len(w) for w in words) / max(word_count, 1)
    
    # Calculate quality score
    quality_score = 50  # Base score
    
    # Adjust for sentence length (too short or too long is bad)
    if 15 <= avg_sentence_len <= 25:
        quality_score += 15
    elif 10 <= avg_sentence_len <= 30:
        quality_score += 8
    else:
        quality_score -= 5
    
    # Adjust for vocabulary richness
    if vocab_richness > 0.6:
        quality_score += 15
    elif vocab_richness > 0.4:
        quality_score += 8
    else:
        quality_score -= 5
    
    # Adjust for appropriate word length
    if 4 <= avg_word_len <= 6:
        quality_score += 10
    elif avg_word_len > 6:
        quality_score += 5
    
    # Penalize very short texts
    if word_count < 50:
        quality_score -= 10
    elif word_count > 200:
        quality_score += 10
    
    quality_score = max(0, min(100, quality_score))
    
    if quality_score >= 70:
        quality_label = "Professional"
        quality_color = "#22c55e"
    elif quality_score >= 50:
        quality_label = "Average"
        quality_color = "#3b82f6"
    elif quality_score >= 30:
        quality_label = "Below Average"
        quality_color = "#f59e0b"
    else:
        quality_label = "Poor"
        quality_color = "#ef4444"
    
    return {
        "score": round(quality_score),
        "label": quality_label,
        "color": quality_color,
        "metrics": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_len, 1),
            "vocabulary_richness": round(vocab_richness * 100, 1),
            "avg_word_length": round(avg_word_len, 1)
        }
    }


# ============================================================
# 4. COMPREHENSIVE CONTENT ANALYSIS
# ============================================================

def full_content_analysis(text):
    """
    Run all content analysis features on the text.
    Returns a comprehensive analysis report.
    """
    sentiment = analyze_sentiment(text)
    manipulation = detect_manipulation(text)
    writing = analyze_writing_quality(text)
    
    # Calculate overall credibility signal from content analysis
    content_credibility = 50
    
    # Negative sentiment + high subjectivity = suspicious
    if sentiment["polarity"] < -0.3 and sentiment["subjectivity"] > 0.6:
        content_credibility -= 15
    
    # High manipulation = suspicious
    content_credibility -= manipulation["score"] * 0.3
    
    # Good writing quality = more credible
    content_credibility += (writing["score"] - 50) * 0.3
    
    content_credibility = max(0, min(100, content_credibility))
    
    return {
        "sentiment": sentiment,
        "manipulation": manipulation,
        "writing_quality": writing,
        "content_credibility": round(content_credibility, 1)
    }
