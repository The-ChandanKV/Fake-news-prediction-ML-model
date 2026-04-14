"""
Indian News Fetcher — FakeDetect AI
Scrapes real Indian news articles from The Hindu and Indian Express RSS feeds.
Labels them as Real (label=0) for retraining the model to handle Indian news.
"""

import csv
import os
import sys
import time

# Fix Unicode on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import feedparser
except ImportError:
    print("Installing feedparser...")
    os.system(f"{sys.executable} -m pip install feedparser")
    import feedparser

OUTPUT_FILE = 'indian_news.csv'

# Indian RSS feeds — all major, reputable Indian outlets
FEEDS = [
    # The Hindu
    {"url": "https://www.thehindu.com/feeder/default.rss", "source": "The Hindu"},
    {"url": "https://www.thehindu.com/news/national/feeder/default.rss", "source": "The Hindu National"},
    {"url": "https://www.thehindu.com/news/international/feeder/default.rss", "source": "The Hindu International"},
    {"url": "https://www.thehindu.com/business/feeder/default.rss", "source": "The Hindu Business"},
    {"url": "https://www.thehindu.com/sci-tech/feeder/default.rss", "source": "The Hindu SciTech"},
    {"url": "https://www.thehindu.com/sport/feeder/default.rss", "source": "The Hindu Sports"},
    
    # Indian Express
    {"url": "https://indianexpress.com/feed/", "source": "Indian Express"},
    {"url": "https://indianexpress.com/section/india/feed/", "source": "Indian Express India"},
    {"url": "https://indianexpress.com/section/business/feed/", "source": "Indian Express Business"},
    {"url": "https://indianexpress.com/section/technology/feed/", "source": "Indian Express Tech"},
    {"url": "https://indianexpress.com/section/sports/feed/", "source": "Indian Express Sports"},
    
    # NDTV
    {"url": "https://feeds.feedburner.com/ndtvnews-top-stories", "source": "NDTV"},
    {"url": "https://feeds.feedburner.com/ndtvnews-india-news", "source": "NDTV India"},
    {"url": "https://feeds.feedburner.com/ndtvnews-world-news", "source": "NDTV World"},
    
    # Times of India
    {"url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "source": "Times of India"},
    {"url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms", "source": "TOI India"},
    
    # Hindustan Times
    {"url": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml", "source": "Hindustan Times"},
    {"url": "https://www.hindustantimes.com/feeds/rss/business/rssfeed.xml", "source": "HT Business"},
    
    # Mint (Livemint)
    {"url": "https://www.livemint.com/rss/news", "source": "Livemint"},
    
    # Economic Times
    {"url": "https://economictimes.indiatimes.com/rssfeedstopstories.cms", "source": "Economic Times"},
    
    # Deccan Herald
    {"url": "https://www.deccanherald.com/rss/india.rss", "source": "Deccan Herald"},
    
    # The Wire
    {"url": "https://thewire.in/feed", "source": "The Wire"},
    
    # Scroll.in
    {"url": "https://scroll.in/feed", "source": "Scroll.in"},
]


def clean_html(text):
    """Remove HTML tags from text."""
    import re
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def fetch_indian_news():
    """Fetch articles from all Indian RSS feeds."""
    print("=" * 60)
    print("INDIAN NEWS FETCHER — FakeDetect AI")
    print("=" * 60)
    
    all_articles = []
    seen_titles = set()  # Deduplicate
    
    for feed_info in FEEDS:
        url = feed_info["url"]
        source = feed_info["source"]
        
        print(f"\n📡 Fetching from {source}...")
        try:
            feed = feedparser.parse(url)
            count = 0
            
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                
                # Skip empty or very short titles
                if not title or len(title) < 15:
                    continue
                
                # Skip duplicates
                title_key = title.lower()[:60]
                if title_key in seen_titles:
                    continue
                seen_titles.add(title_key)
                
                # Get the article body/summary
                body = ""
                if hasattr(entry, "content") and entry.content:
                    body = entry.content[0].get("value", "")
                elif hasattr(entry, "summary"):
                    body = entry.summary or ""
                elif hasattr(entry, "description"):
                    body = entry.description or ""
                
                body = clean_html(body)
                
                # Combine title + body for maximum training value
                full_text = f"{title}. {body}" if body else title
                
                # Only keep articles with reasonable length
                if len(full_text) < 30:
                    continue
                
                all_articles.append({
                    "title": full_text,
                    "author": source,
                    "label": 0  # 0 = Real News
                })
                count += 1
            
            print(f"   ✓ Got {count} articles from {source}")
            
        except Exception as e:
            print(f"   ✗ Error fetching {source}: {e}")
        
        time.sleep(0.3)  # Be polite to servers
    
    print(f"\n{'=' * 60}")
    print(f"Total unique Indian articles fetched: {len(all_articles)}")
    
    # Save to CSV
    if all_articles:
        file_exists = os.path.isfile(OUTPUT_FILE)
        existing_count = 0
        
        if file_exists:
            try:
                import pandas as pd
                existing = pd.read_csv(OUTPUT_FILE)
                existing_count = len(existing)
            except:
                pass
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'author', 'label'])
            writer.writeheader()
            writer.writerows(all_articles)
        
        print(f"✓ Saved {len(all_articles)} articles to {OUTPUT_FILE}")
        print(f"  (Previous file had {existing_count} articles)")
    else:
        print("✗ No articles fetched. Check your internet connection.")
    
    print("=" * 60)
    return all_articles


if __name__ == "__main__":
    articles = fetch_indian_news()
    print(f"\nDone! {len(articles)} Indian news articles ready for retraining.")
    print("Now run: python train_improved_model.py")
