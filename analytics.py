"""
Analytics Engine — FakeDetect AI
Tracks all predictions, domains, categories, and feedback over time.
Stored in a simple JSON log for the dashboard.
"""
import json
import os
from datetime import datetime, timedelta
from collections import Counter

ANALYTICS_FILE = 'analytics_log.json'

DEFAULT = {
    "predictions": [],          # List of {ts, verdict, confidence, category, domain, lang}
    "feedback": [],             # List of {ts, was_correct}
    "domains_flagged": [],      # List of {domain, count}
    "api_calls": 0,
}


def _load():
    if os.path.isfile(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return dict(DEFAULT)


def _save(data):
    try:
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception:
        pass


def log_prediction(verdict: str, confidence: float, category: str = "Unknown",
                   domain: str = None, lang: str = "en"):
    """Log a prediction event."""
    data = _load()
    data.setdefault("predictions", []).append({
        "ts": datetime.now().isoformat(),
        "verdict": verdict,          # "Fake News" or "Real News"
        "confidence": round(confidence, 1),
        "category": category,
        "domain": domain or "direct_input",
        "lang": lang
    })
    # Keep only last 500 predictions to avoid huge files
    data["predictions"] = data["predictions"][-500:]
    _save(data)


def log_feedback(was_correct: bool):
    """Log user feedback."""
    data = _load()
    data.setdefault("feedback", []).append({
        "ts": datetime.now().isoformat(),
        "correct": was_correct
    })
    data["feedback"] = data["feedback"][-500:]
    _save(data)


def get_dashboard_stats():
    """Compute full dashboard stats from the log."""
    data = _load()
    predictions = data.get("predictions", [])
    feedback = data.get("feedback", [])

    # ── Total counters ──
    total = len(predictions)
    fake_count = sum(1 for p in predictions if p["verdict"] == "Fake News")
    real_count = total - fake_count

    # ── Last 7 days trend (one bucket per day) ──
    today = datetime.now().date()
    trend = {}
    for i in range(6, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        trend[d] = {"fake": 0, "real": 0}
    for p in predictions:
        try:
            day = p["ts"][:10]
            if day in trend:
                if p["verdict"] == "Fake News":
                    trend[day]["fake"] += 1
                else:
                    trend[day]["real"] += 1
        except Exception:
            pass

    # ── Top fake domains ──
    fake_domains = Counter(
        p["domain"] for p in predictions
        if p["verdict"] == "Fake News" and p["domain"] != "direct_input"
    )
    top_fake_domains = [{"domain": d, "count": c} for d, c in fake_domains.most_common(5)]

    # ── Category breakdown (for heatmap) ──
    categories = Counter(p.get("category", "Unknown") for p in predictions)
    category_breakdown = [{"category": c, "count": n} for c, n in categories.most_common(8)]

    # ── Language diversity ──
    langs = Counter(p.get("lang", "en") for p in predictions)
    lang_breakdown = [{"lang": l, "count": n} for l, n in langs.most_common(5)]

    # ── Feedback accuracy ──
    total_fb = len(feedback)
    correct_fb = sum(1 for f in feedback if f.get("correct"))
    feedback_accuracy = round((correct_fb / total_fb * 100), 1) if total_fb > 0 else 0

    # ── Avg confidence ──
    avg_confidence = round(
        sum(p["confidence"] for p in predictions) / total, 1
    ) if total > 0 else 0

    return {
        "total_analyses": total,
        "fake_detected": fake_count,
        "real_detected": real_count,
        "fake_percentage": round(fake_count / total * 100, 1) if total > 0 else 0,
        "avg_confidence": avg_confidence,
        "trend_7days": [
            {"date": d, "fake": v["fake"], "real": v["real"]}
            for d, v in trend.items()
        ],
        "top_fake_domains": top_fake_domains,
        "category_breakdown": category_breakdown,
        "language_breakdown": lang_breakdown,
        "feedback_accuracy": feedback_accuracy,
        "total_feedback": total_fb,
        "model_accuracy": 98.6,
        "total_training_articles": 20810,
        "languages_supported": 45,
        "sources_in_db": 40,
    }
