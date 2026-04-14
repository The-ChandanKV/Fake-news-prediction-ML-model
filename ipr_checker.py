"""
IPR & Content Originality Module — FakeDetect AI
Checks phrase originality, detects copy-paste patterns,
and computes a content uniqueness score relevant to IPR.
"""
import re
import urllib.request
import urllib.parse
import json
from collections import Counter


def extract_key_phrases(text, n=8):
    """Extract the most significant n-gram phrases from text."""
    # Clean text
    text = re.sub(r'[^a-zA-Z\s]', ' ', text).lower()
    words = [w for w in text.split() if len(w) > 4]
    
    phrases = []
    # 3-grams
    for i in range(len(words) - 2):
        phrases.append(' '.join(words[i:i+3]))
    # 4-grams (more distinctive)
    for i in range(len(words) - 3):
        phrases.append(' '.join(words[i:i+4]))

    # Return top unique phrases (pick evenly spaced for coverage)
    if len(phrases) == 0:
        return []
    step = max(1, len(phrases) // n)
    return list(dict.fromkeys(phrases[::step]))[:n]


def check_phrase_online(phrase):
    """
    Check if a phrase appears in Google search results (via scraping).
    Returns True if found, False otherwise.
    Uses DuckDuckGo Instant Answer API (free, no key needed).
    """
    try:
        query = urllib.parse.quote(f'"{phrase}"')
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "FakeDetectAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        # If there's any abstract or related topics, the phrase exists online
        has_results = bool(data.get("Abstract") or data.get("RelatedTopics"))
        return has_results
    except Exception:
        return False  # Treat network errors as "not found"


def analyze_writing_patterns(text):
    """
    Analyze internal patterns that indicate copy-paste or aggregation.
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return {"repetition_score": 0, "avg_sentence_length": 0, "pattern_flags": []}

    # Check for repeated sentence starters
    starters = [s[:30].lower() for s in sentences]
    starter_counts = Counter(starters)
    repeated_starters = {k: v for k, v in starter_counts.items() if v > 1}
    
    # Average sentence length
    avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
    
    # Detect copy-paste flags
    flags = []
    if avg_len > 40:
        flags.append("Very long sentences (typical of copy-paste from articles)")
    if len(repeated_starters) > 2:
        flags.append(f"Repeated sentence patterns detected ({len(repeated_starters)} duplicates)")
    
    # Check for ALL CAPS words (sensationalism)
    caps_words = [w for w in text.split() if w.isupper() and len(w) > 3]
    if len(caps_words) > 5:
        flags.append(f"Excessive capitalization ({len(caps_words)} ALL-CAPS words) — common in viral misinformation")
    
    # Excessive punctuation
    exclaim = text.count('!')
    if exclaim > 3:
        flags.append(f"Excessive exclamation marks ({exclaim}) — manipulative writing style")
    
    return {
        "repetition_score": min(100, len(repeated_starters) * 15),
        "avg_sentence_length": round(avg_len, 1),
        "pattern_flags": flags,
        "sentence_count": len(sentences),
        "caps_words": len(caps_words),
        "exclamation_count": exclaim
    }


def compute_originality_score(text, check_online=False):
    """
    Full IPR content originality analysis.
    Returns an originality score (0-100) and detailed breakdown.
    check_online: whether to actually query web for phrase matches (slower).
    """
    if not text or len(text) < 50:
        return {
            "originality_score": 50,
            "ipr_risk": "Unable to assess — text too short",
            "key_phrases": [],
            "writing_analysis": {},
            "online_matches": 0,
            "phrases_checked": 0
        }

    key_phrases = extract_key_phrases(text, n=6)
    writing_analysis = analyze_writing_patterns(text)
    
    # Base score starts at 100 (original) and deductions are made
    base_score = 100
    online_match_count = 0
    phrases_checked = 0
    
    if check_online:
        for phrase in key_phrases[:4]:  # Check top 4 phrases only (for speed)
            phrases_checked += 1
            if check_phrase_online(phrase):
                online_match_count += 1
                base_score -= 18  # Each online match reduces originality

    # Deduct for writing pattern issues
    base_score -= writing_analysis.get("repetition_score", 0) * 0.3
    
    # Deduct for sensationalist flags
    flag_count = len(writing_analysis.get("pattern_flags", []))
    base_score -= flag_count * 5
    
    # Generate vocabulary diversity score
    words = re.sub(r'[^a-zA-Z\s]', ' ', text.lower()).split()
    unique_words = set(words)
    vocab_diversity = round(len(unique_words) / max(len(words), 1) * 100, 1)
    
    # High vocabulary diversity = more original
    if vocab_diversity > 60:
        base_score += 5
    elif vocab_diversity < 30:
        base_score -= 10

    originality_score = max(0, min(100, round(base_score)))
    
    # IPR Risk assessment
    if originality_score >= 75:
        ipr_risk = "Low Risk — Content appears original"
        ipr_color = "green"
    elif originality_score >= 50:
        ipr_risk = "Medium Risk — Some phrases may be sourced"
        ipr_color = "yellow"
    elif originality_score >= 25:
        ipr_risk = "High Risk — Significant content overlap detected"
        ipr_color = "orange"
    else:
        ipr_risk = "Critical — Likely copied/aggregated content (IPR violation possible)"
        ipr_color = "red"

    return {
        "originality_score": originality_score,
        "ipr_risk": ipr_risk,
        "ipr_color": ipr_color,
        "key_phrases": key_phrases,
        "writing_analysis": writing_analysis,
        "vocab_diversity": vocab_diversity,
        "online_matches": online_match_count,
        "phrases_checked": phrases_checked,
        "ipr_summary": {
            "total_words": len(text.split()),
            "unique_words": len(unique_words),
            "sentence_count": writing_analysis.get("sentence_count", 0),
            "pattern_flags": writing_analysis.get("pattern_flags", []),
        }
    }
