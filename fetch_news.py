"""
Dynamic News Fetcher - Keeps the model updated with real-world news
Fetches latest news articles from free APIs and saves them for retraining.
"""

import os
import csv
import json
import urllib.request
import urllib.error
from datetime import datetime


# ===== GNews API (free, no key required for basic usage) =====
GNEWS_API_URL = "https://gnews.io/api/v4/top-headlines"

# ===== NewsData.io (free tier, generous limits) =====
NEWSDATA_API_URL = "https://newsdata.io/api/1/latest"

FETCHED_NEWS_FILE = "fetched_news.csv"
FETCH_LOG_FILE = "fetch_log.json"


def fetch_from_gnews(api_key=None, category="general", lang="en", max_results=10):
    """
    Fetch top headlines from GNews API.
    Free tier: 100 requests/day, 10 articles per request.
    Get a free key at: https://gnews.io/
    """
    if not api_key:
        print("  ⚠ GNews API key not set. Skipping GNews source.")
        return []

    params = f"?category={category}&lang={lang}&max={max_results}&apikey={api_key}"
    url = GNEWS_API_URL + params

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FakeNewsDetector/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())

        articles = []
        for article in data.get("articles", []):
            title = article.get("title", "").strip()
            author = article.get("source", {}).get("name", "Unknown")
            if title:
                articles.append({
                    "title": title,
                    "author": author,
                    "label": 0,  # 0 = Real (from verified news sources)
                    "source": "gnews",
                    "fetched_at": datetime.now().isoformat()
                })

        print(f"  ✓ GNews: Fetched {len(articles)} articles")
        return articles

    except urllib.error.HTTPError as e:
        print(f"  ✗ GNews HTTP Error: {e.code} - {e.reason}")
        return []
    except Exception as e:
        print(f"  ✗ GNews Error: {e}")
        return []


def fetch_from_newsdata(api_key=None, language="en", size=10):
    """
    Fetch latest news from NewsData.io API.
    Free tier: 200 credits/day, up to 10 results per request.
    Get a free key at: https://newsdata.io/
    """
    if not api_key:
        print("  ⚠ NewsData API key not set. Skipping NewsData source.")
        return []

    params = f"?language={language}&size={size}&apikey={api_key}"
    url = NEWSDATA_API_URL + params

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FakeNewsDetector/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())

        articles = []
        for article in data.get("results", []):
            title = article.get("title", "").strip()
            author = article.get("creator")
            if isinstance(author, list):
                author = ", ".join(author) if author else "Unknown"
            elif not author:
                author = article.get("source_id", "Unknown")
            if title:
                articles.append({
                    "title": title,
                    "author": author,
                    "label": 0,  # 0 = Real (from verified news sources)
                    "source": "newsdata",
                    "fetched_at": datetime.now().isoformat()
                })

        print(f"  ✓ NewsData: Fetched {len(articles)} articles")
        return articles

    except urllib.error.HTTPError as e:
        print(f"  ✗ NewsData HTTP Error: {e.code} - {e.reason}")
        return []
    except Exception as e:
        print(f"  ✗ NewsData Error: {e}")
        return []


def fetch_from_rss():
    """
    Fetch news from free RSS feeds (no API key needed).
    Uses reliable sources like Reuters, AP News, BBC via their RSS feeds.
    """
    rss_feeds = [
        ("Reuters", "https://feeds.reuters.com/reuters/topNews"),
        ("AP News", "https://rss.app/feeds/v1.1/ts5kDJgoOmCqF6QT.json"),
        ("BBC", "https://feeds.bbci.co.uk/news/rss.xml"),
    ]

    articles = []

    for source_name, feed_url in rss_feeds:
        try:
            req = urllib.request.Request(feed_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FakeNewsDetector/1.0"
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode("utf-8", errors="replace")

            # Simple XML title extraction (works for RSS feeds without external libraries)
            titles = []
            in_item = False
            for line in content.split("\n"):
                line = line.strip()
                if "<item" in line.lower():
                    in_item = True
                if in_item and "<title" in line.lower():
                    # Extract text between <title> and </title>
                    start = line.find(">") + 1
                    end = line.find("</")
                    if start > 0 and end > start:
                        title = line[start:end].strip()
                        # Remove CDATA wrapper if present
                        title = title.replace("<![CDATA[", "").replace("]]>", "").strip()
                        if title and len(title) > 10:
                            titles.append(title)
                    in_item = False  # Only grab first title per item

            for title in titles[:10]:  # Limit to 10 per source
                articles.append({
                    "title": title,
                    "author": source_name,
                    "label": 0,  # 0 = Real (from verified news outlets)
                    "source": f"rss_{source_name.lower().replace(' ', '_')}",
                    "fetched_at": datetime.now().isoformat()
                })

            print(f"  ✓ RSS ({source_name}): Fetched {len(titles[:10])} articles")

        except Exception as e:
            print(f"  ✗ RSS ({source_name}): {e}")

    return articles


def save_articles(articles, filepath=FETCHED_NEWS_FILE):
    """Save fetched articles to CSV, appending to existing data."""
    if not articles:
        print("\n  ⚠ No new articles to save.")
        return 0

    file_exists = os.path.isfile(filepath)

    # Load existing titles to avoid duplicates
    existing_titles = set()
    if file_exists:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_titles.add(row.get("title", "").strip().lower())
        except Exception:
            pass

    new_count = 0
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["title", "author", "label"])

        for article in articles:
            title = article["title"].strip()
            if title.lower() not in existing_titles:
                writer.writerow([title, article["author"], article["label"]])
                existing_titles.add(title.lower())
                new_count += 1

    return new_count


def update_fetch_log(new_count, total_articles):
    """Update the fetch log with timestamp and counts."""
    log = {"fetches": []}

    if os.path.isfile(FETCH_LOG_FILE):
        try:
            with open(FETCH_LOG_FILE, "r") as f:
                log = json.load(f)
        except Exception:
            pass

    log["fetches"].append({
        "timestamp": datetime.now().isoformat(),
        "new_articles": new_count,
        "total_articles": total_articles
    })
    log["last_fetch"] = datetime.now().isoformat()
    log["total_fetched_articles"] = total_articles

    with open(FETCH_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def get_total_fetched():
    """Count total articles in the fetched news file."""
    if not os.path.isfile(FETCHED_NEWS_FILE):
        return 0
    try:
        with open(FETCHED_NEWS_FILE, "r", encoding="utf-8") as f:
            return sum(1 for _ in f) - 1  # Subtract header
    except Exception:
        return 0


def fetch_all_news(gnews_key=None, newsdata_key=None):
    """
    Main function: fetch news from all available sources.
    Returns summary dict with results.
    """
    print("\n" + "=" * 50)
    print("📰 FETCHING LATEST NEWS")
    print("=" * 50)

    all_articles = []

    # 1. Always try RSS feeds (free, no key needed)
    print("\n[1] Fetching from RSS feeds (no API key needed)...")
    rss_articles = fetch_from_rss()
    all_articles.extend(rss_articles)

    # 2. Try GNews if key is available
    print("\n[2] Fetching from GNews API...")
    gnews_key = gnews_key or os.environ.get("GNEWS_API_KEY")
    gnews_articles = fetch_from_gnews(api_key=gnews_key)
    all_articles.extend(gnews_articles)

    # 3. Try NewsData if key is available
    print("\n[3] Fetching from NewsData API...")
    newsdata_key = newsdata_key or os.environ.get("NEWSDATA_API_KEY")
    newsdata_articles = fetch_from_newsdata(api_key=newsdata_key)
    all_articles.extend(newsdata_articles)

    # Save all articles
    print(f"\n[4] Saving articles...")
    new_count = save_articles(all_articles)
    total = get_total_fetched()

    # Update log
    update_fetch_log(new_count, total)

    print(f"\n{'=' * 50}")
    print(f"✓ {new_count} new articles added (duplicates skipped)")
    print(f"✓ Total articles in fetched_news.csv: {total}")
    print(f"{'=' * 50}\n")

    return {
        "new_articles": new_count,
        "total_articles": total,
        "sources_tried": 3,
        "timestamp": datetime.now().isoformat()
    }


# Run directly for testing
if __name__ == "__main__":
    result = fetch_all_news()
    print("\nDone! To retrain the model with this new data, run:")
    print("  python train_improved_model.py")
