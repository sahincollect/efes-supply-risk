import feedparser
import pandas as pd
from datetime import datetime

FEEDS = {
    "reuters": "https://feeds.reuters.com/reuters/businessNews",
    "bbc_business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "brewers_journal": "https://www.brewersjournal.info/feed/",
}

def collect_feed(source_name: str, feed_url: str) -> list:
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "source": source_name,
            "collected_at": datetime.utcnow().isoformat()
        })
    return articles

def collect_all() -> pd.DataFrame:
    all_articles = []
    for source_name, url in FEEDS.items():
        print(f"Toplaniyor: {source_name}...")
        articles = collect_feed(source_name, url)
        all_articles.extend(articles)
        print(f"  {len(articles)} haber bulundu")

    df = pd.DataFrame(all_articles)
    df.to_csv("data/processed/articles.csv", index=False)
    print(f"\nToplam {len(df)} haber kaydedildi -> data/processed/articles.csv")
    return df

if __name__ == "__main__":
    df = collect_all()
    print(df.head())