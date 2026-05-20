import requests
import pandas as pd
from datetime import datetime

QUERIES = [
    "Efes Breweries supply chain",
    "barley shortage Europe",
    "aluminum can shortage",
    "logistics disruption Black Sea",
    "port closure supply risk",
    "grain export Ukraine",
]

def fetch_gdelt(query: str, timespan: str = "7d") -> list:
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": 50,
        "timespan": timespan,
        "format": "json",
        "sourcelang": "english"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        articles = data.get("articles", [])
        results = []
        for a in articles:
            results.append({
                "title": a.get("title", ""),
                "url": a.get("url", ""),
                "source": a.get("domain", ""),
                "published": a.get("seendate", ""),
                "query": query,
                "collected_at": datetime.utcnow().isoformat()
            })
        return results
    except Exception as e:
        print(f"Hata ({query}): {e}")
        return []

def collect_all() -> pd.DataFrame:
    all_articles = []
    for query in QUERIES:
        print(f"Sorgulanıyor: {query}...")
        articles = fetch_gdelt(query)
        all_articles.extend(articles)
        print(f"  {len(articles)} haber bulundu")

    df = pd.DataFrame(all_articles)
    df.to_csv("data/processed/gdelt_articles.csv", index=False)
    print(f"\nToplam {len(df)} haber kaydedildi -> data/processed/gdelt_articles.csv")
    return df

if __name__ == "__main__":
    df = collect_all()
    print(df.head())