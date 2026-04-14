"""
URL Analysis Module for Fake News Detector
Analyzes URLs for credibility signals:
- Domain reputation checking
- URL pattern analysis  
- Content scraping from URLs
- Suspicious URL pattern detection
"""

import re
import urllib.request
import urllib.parse
import urllib.error
import json
from datetime import datetime


# ============================================================
# 1. URL PATTERN ANALYSIS
# ============================================================

SUSPICIOUS_TLD_PATTERNS = {
    '.xyz', '.top', '.win', '.bid', '.click', '.link', '.work',
    '.gq', '.ml', '.cf', '.tk', '.ga', '.buzz', '.rest',
    '.icu', '.monster', '.beauty', '.hair', '.quest'
}

SUSPICIOUS_URL_PATTERNS = [
    r'\d{5,}',                        # URLs with long numbers
    r'[a-z]{20,}',                    # Very long unbroken text
    r'(?:fake|hoax|breaking|alert)\d*\.', # Suspicious words in domain
    r'news\d{2,}\.',                  # Generic news + numbers
    r'-{3,}',                         # Multiple consecutive hyphens
    r'[^/]+\.[^/]+\.[^/]+\.[^/]+\.', # Too many subdomains
]

KNOWN_URL_SHORTENERS = {
    'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co',
    'is.gd', 'buff.ly', 'adf.ly', 'bl.ink', 'lnkd.in',
    'db.tt', 'qr.ae', 'cur.lv', 'ity.im'
}

CREDIBLE_DOMAINS = {
    'reuters.com', 'apnews.com', 'bbc.com', 'bbc.co.uk', 'nytimes.com',
    'washingtonpost.com', 'theguardian.com', 'wsj.com', 'economist.com',
    'npr.org', 'pbs.org', 'nature.com', 'science.org', 'thehindu.com',
    'ndtv.com', 'timesofindia.indiatimes.com', 'hindustantimes.com',
    'indianexpress.com', 'cnn.com', 'nbcnews.com', 'abcnews.go.com',
    'cbsnews.com', 'usatoday.com', 'time.com', 'newsweek.com',
    'bloomberg.com', 'ft.com', 'aljazeera.com', 'dw.com',
    'france24.com', 'abc.net.au', 'cbc.ca', 'thewire.in'
}


def extract_domain(url):
    """Extract the base domain from a URL."""
    try:
        # Add protocol if missing
        if not url.startswith('http'):
            url = 'https://' + url
        
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        # Remove www
        if domain.startswith('www.'):
            domain = domain[4:]
        
        return domain
    except Exception:
        return None


def analyze_url(url):
    """
    Comprehensive URL analysis.
    Returns trust signals and risk factors.
    """
    if not url or not isinstance(url, str):
        return None
    
    signals = {
        "url": url,
        "domain": None,
        "trust_score": 50,  # Start at neutral
        "risk_factors": [],
        "trust_factors": [],
        "is_shortened": False,
        "is_credible_source": False,
        "tld_suspicious": False,
        "analysis_summary": ""
    }
    
    domain = extract_domain(url)
    if not domain:
        signals["risk_factors"].append("Could not parse URL")
        signals["trust_score"] = 20
        return signals
    
    signals["domain"] = domain
    
    # 1. Check if it's a known credible source
    for credible in CREDIBLE_DOMAINS:
        if domain == credible or domain.endswith('.' + credible):
            signals["is_credible_source"] = True
            signals["trust_factors"].append(f"Known credible source: {credible}")
            signals["trust_score"] += 35
            break
    
    # 2. Check for URL shorteners
    if domain in KNOWN_URL_SHORTENERS:
        signals["is_shortened"] = True
        signals["risk_factors"].append("URL uses a URL shortener (masks the real destination)")
        signals["trust_score"] -= 15
    
    # 3. Check for suspicious TLDs
    for tld in SUSPICIOUS_TLD_PATTERNS:
        if domain.endswith(tld):
            signals["tld_suspicious"] = True
            signals["risk_factors"].append(f"Suspicious top-level domain: {tld}")
            signals["trust_score"] -= 20
            break
    
    # 4. Check for suspicious URL patterns
    for pattern in SUSPICIOUS_URL_PATTERNS:
        if re.search(pattern, url.lower()):
            signals["risk_factors"].append(f"URL contains suspicious patterns")
            signals["trust_score"] -= 10
            break
    
    # 5. Check domain length (very long domains are suspicious)
    if len(domain) > 30:
        signals["risk_factors"].append("Unusually long domain name")
        signals["trust_score"] -= 10
    
    # 6. Count subdomains
    parts = domain.split('.')
    if len(parts) > 3:
        signals["risk_factors"].append(f"Multiple subdomains ({len(parts)-2} levels)")
        signals["trust_score"] -= 10
    
    # 7. Check for IP address instead of domain
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if re.match(ip_pattern, domain):
        signals["risk_factors"].append("URL uses IP address instead of domain name")
        signals["trust_score"] -= 25
    
    # 8. HTTPS check
    if url.startswith('https://'):
        signals["trust_factors"].append("Uses HTTPS (encrypted connection)")
        signals["trust_score"] += 5
    elif url.startswith('http://'):
        signals["risk_factors"].append("Uses unencrypted HTTP")
        signals["trust_score"] -= 5
    
    # Normalize score
    signals["trust_score"] = max(0, min(100, signals["trust_score"]))
    
    # Generate summary
    if signals["trust_score"] >= 70:
        signals["analysis_summary"] = "This URL appears to be from a trustworthy source"
        signals["verdict"] = "Trusted"
        signals["verdict_color"] = "#22c55e"
    elif signals["trust_score"] >= 40:
        signals["analysis_summary"] = "This URL shows mixed trust signals — proceed with caution"
        signals["verdict"] = "Caution"
        signals["verdict_color"] = "#f59e0b"
    else:
        signals["analysis_summary"] = "This URL shows multiple risk indicators — verify content independently"
        signals["verdict"] = "Risky"
        signals["verdict_color"] = "#ef4444"
    
    return signals


def scrape_article_text(url):
    """
    Attempt to scrape article text from a URL.
    Returns the extracted text or None.
    """
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='replace')
        
        # Remove scripts and styles
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL)
        html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL)
        html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL)
        
        # Extract text from <p> tags (most article content)
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        
        # Remove remaining HTML tags
        text_parts = []
        for p in paragraphs:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 30:  # Only keep meaningful paragraphs
                text_parts.append(clean)
        
        # Also try to get the title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        
        # Get meta description
        meta_desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html)
        description = meta_desc.group(1) if meta_desc else ""
        
        article_text = ' '.join(text_parts)
        
        if len(article_text) < 50:
            return None
        
        return {
            "title": title,
            "description": description,
            "text": article_text[:5000],  # Limit to 5000 chars
            "word_count": len(article_text.split()),
            "scraped_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return None


def is_url(text):
    """Check if the input text is a URL."""
    url_pattern = r'^https?://[^\s]+$|^www\.[^\s]+$|^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s]*$'
    text_stripped = text.strip()
    return bool(re.match(url_pattern, text_stripped)) and len(text_stripped) < 500
