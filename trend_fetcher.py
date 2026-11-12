import json
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_hacker_news_top(limit: int = 6) -> List[Dict[str, str]]:
    """Fetch top stories from Hacker News official API."""
    stories = []
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            ids = json.loads(resp.read().decode())[:limit]
        
        for item_id in ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            item_req = urllib.request.Request(item_url, headers=HEADERS)
            with urllib.request.urlopen(item_req, timeout=5) as item_resp:
                data = json.loads(item_resp.read().decode())
                if data and "title" in data:
                    stories.append({
                        "source": "Hacker News",
                        "title": data.get("title", ""),
                        "url": data.get("url", f"https://news.ycombinator.com/item?id={item_id}"),
                        "score": data.get("score", 0),
                        "comments": data.get("descendants", 0)
                    })
    except Exception as e:
        # Gracefully handle network issues
        pass
    return stories

def fetch_google_tech_news(limit: int = 5) -> List[Dict[str, str]]:
    """Fetch breaking tech headlines from Google News RSS."""
    headlines = []
    try:
        url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            tree = ET.fromstring(resp.read().decode("utf-8", errors="ignore"))
            channel = tree.find("channel")
            if channel is not None:
                for item in channel.findall("item")[:limit]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    if title_elem is not None and title_elem.text:
                        headlines.append({
                            "source": "Google Tech News",
                            "title": title_elem.text,
                            "url": link_elem.text if link_elem is not None else ""
                        })
    except Exception:
        pass
    return headlines

def fetch_reddit_top(subreddit: str = "MachineLearning", limit: int = 4) -> List[Dict[str, str]]:
    """Fetch top discussions from a tech subreddit."""
    discussions = []
    try:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            children = data.get("data", {}).get("children", [])
            for child in children:
                post = child.get("data", {})
                # Skip stickied posts
                if post.get("stickied"):
                    continue
                discussions.append({
                    "source": f"r/{subreddit}",
                    "title": post.get("title", ""),
                    "score": post.get("ups", 0),
                    "comments": post.get("num_comments", 0),
                    "url": f"https://reddit.com{post.get('permalink', '')}"
                })
    except Exception:
        pass
    return discussions

def get_current_tech_trends() -> List[Dict[str, str]]:
    """Combine top trending sources across tech and AI."""
    all_trends = []
    hn = fetch_hacker_news_top(limit=5)
    all_trends.extend(hn)
    
    reddit_ml = fetch_reddit_top("MachineLearning", limit=3)
    all_trends.extend(reddit_ml)
    
    gnews = fetch_google_tech_news(limit=4)
    all_trends.extend(gnews)
    
    # Fallback default evergreen trends if completely offline or restricted
    if not all_trends:
        all_trends = [
            {"source": "Curated Tech Trend", "title": "Large Language Models in production vs Local small SLMs latency & cost"},
            {"source": "Curated Tech Trend", "title": "Developers debating whether automated AI coding tools reduce foundational understanding"},
            {"source": "Curated Tech Trend", "title": "Evaluating imbalanced datasets: why high accuracy hides poor model performance"},
            {"source": "Curated Tech Trend", "title": "The reality of building an end-to-end RAG architecture with real validation gates"}
        ]
    
    return all_trends
