import pandas as pd
import numpy as np
from datetime import datetime

SOURCE_WEIGHTS = {
    "reuters.com": 1.0,
    "bloomberg.com": 1.0,
    "ft.com": 0.9,
    "bbc.co.uk": 0.85,
    "hellenicshippingnews.com": 0.8,
    "agrimoney.com": 0.8,
}

RISK_SCORES = {
    "high": 80,
    "medium": 40,
    "low": 10
}

SENTIMENT_MULTIPLIER = {
    "negative": 1.5,
    "neutral": 1.0,
    "positive": 0.5
}

def parse_date(date_str: str) -> datetime:
    formats = [
        "%Y%m%dT%H%M%SZ",
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str)[:20], fmt[:len(str(date_str)[:20])])
        except Exception:
            continue
    return datetime.utcnow()

def calculate_score(row: pd.Series) -> float:
    # 1. Temel risk skoru
    base = RISK_SCORES.get(row.get("risk_level", "low"), 10)

    # 2. Sentiment çarpanı
    sentiment = str(row.get("sentiment", "neutral")).lower()
    multiplier = SENTIMENT_MULTIPLIER.get(sentiment, 1.0)

    # 3. Kaynak güvenilirliği
    source = str(row.get("source", "")).lower()
    source_weight = 0.6
    for domain, weight in SOURCE_WEIGHTS.items():
        if domain in source:
            source_weight = weight
            break

    # 4. Zaman decay
    published = parse_date(row.get("published", ""))
    days_old = max(0, (datetime.utcnow() - published.replace(tzinfo=None)).days)
    time_decay = np.exp(-0.05 * days_old)

    # Composite skor
    score = base * multiplier * source_weight * time_decay
    return round(min(100, score), 1)

def run_scoring(input_path: str, output_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    print(f"{len(df)} haber skorlanıyor...")

    df["risk_score"] = df.apply(calculate_score, axis=1)
    df["alert"] = df["risk_score"].apply(
        lambda x: "KRITIK" if x >= 60 else "ORTA" if x >= 30 else "DUSUK"
    )

    df = df.sort_values("risk_score", ascending=False)
    df.to_csv(output_path, index=False)

    print(f"\nAlert dagilimi:")
    print(df["alert"].value_counts())
    print(f"\nEn yuksek riskli 5 haber:")
    print(df[["title", "risk_score", "alert"]].head())
    return df

if __name__ == "__main__":
    run_scoring(
        input_path="data/processed/gdelt_analyzed.csv",
        output_path="data/processed/gdelt_scored.csv"
    )