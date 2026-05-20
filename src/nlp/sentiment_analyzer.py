from transformers import pipeline
import pandas as pd

finbert = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    return_all_scores=True
)

RISK_KEYWORDS = {
    "high": [
        "shortage", "disruption", "strike", "bankruptcy", "sanctions",
        "flood", "drought", "port closure", "labor dispute", "collapse",
        "crisis", "war", "conflict", "blocked", "shutdown"
    ],
    "medium": [
        "delay", "slowdown", "warning", "concern", "risk",
        "increase", "pressure", "uncertainty"
    ]
}

def classify_risk(text: str) -> dict:
    try:
        scores = finbert(text[:512])[0]
        top = max(scores, key=lambda x: x["score"])
        sentiment = top["label"]
        confidence = round(top["score"], 3)
    except Exception:
        sentiment = "neutral"
        confidence = 0.0

    text_lower = text.lower()
    risk_level = "low"
    for keyword in RISK_KEYWORDS["high"]:
        if keyword in text_lower:
            risk_level = "high"
            break
    if risk_level == "low":
        for keyword in RISK_KEYWORDS["medium"]:
            if keyword in text_lower:
                risk_level = "medium"
                break

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "risk_level": risk_level
    }

def analyze_dataframe(df: pd.DataFrame, text_col: str = "title") -> pd.DataFrame:
    print(f"Analiz ediliyor: {len(df)} haber...")
    results = []
    for i, row in df.iterrows():
        text = str(row[text_col])
        result = classify_risk(text)
        results.append(result)
        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(df)} tamamlandi")

    result_df = pd.DataFrame(results)
    final_df = pd.concat([df.reset_index(drop=True), result_df], axis=1)
    return final_df

if __name__ == "__main__":
    df = pd.read_csv("data/processed/gdelt_articles.csv")
    analyzed = analyze_dataframe(df)
    analyzed.to_csv("data/processed/gdelt_analyzed.csv", index=False)
    print("\nRisk dagilimi:")
    print(analyzed["risk_level"].value_counts())
    print("\nSentiment dagilimi:")
    print(analyzed["sentiment"].value_counts())
    print("\nIlk 5 yuksek riskli haber:")
    high_risk = analyzed[analyzed["risk_level"] == "high"][["title", "sentiment", "risk_level"]]
    print(high_risk.head())