# Efes Tedarik Zinciri Risk Analizi

Gerçek zamanlı haber ve NLP tabanlı tedarik zinciri risk izleme sistemi.
Anadolu Group / Efes Breweries senaryosu üzerine geliştirilmiştir.

## Problem

Efes gibi küresel bir içecek şirketi; arpa, alüminyum, cam ve lojistik
tedarikçilerine bağımlıdır. 2021 Süveyş Kanalı krizi veya 2022 Ukrayna
savaşı gibi olaylar tedarik zincirini ciddi şekilde etkiler. Bu sistem,
bu tür riskleri haberler çıkmadan önce tespit etmeyi hedefler.

## Çözüm

- 400+ haber kaynağından gerçek zamanlı veri toplama (RSS + GDELT)
- FinBERT ile finansal sentiment analizi
- Keyword tabanlı risk sınıflandırması (high / medium / low)
- Zaman, kaynak güvenilirliği ve entity relevance ağırlıklı composite risk skoru
- Streamlit ile canlı dashboard

## Teknoloji Stack

| Katman | Teknoloji |
|--------|-----------|
| Veri toplama | feedparser, requests, GDELT API |
| NLP | HuggingFace Transformers, FinBERT, spaCy |
| Skorlama | NumPy, Pandas |
| Dashboard | Streamlit, Plotly |

## Kurulum

```bash
git clone https://github.com/KULLANICIADUN/efes-supply-risk.git
cd efes-supply-risk
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
# Veri topla
python src/collectors/rss_collector.py
python src/collectors/gdelt_collector.py

# NLP analizi
python src/nlp/sentiment_analyzer.py

# Risk skorla
python src/scoring/risk_engine.py

# Dashboard başlat
streamlit run app/streamlit_app.py
```

## Örnek Çıktı

Sistem bugün tespit ettiği en yüksek riskli haberler:

- [57.9] Oil prices rise as Iraq Hormuz shipments collapse amid conflict
- [48.0] Russian strike damages Ukraine Danube port
- [39.3] How the Iran conflict pushed Atlantic grain freight to a four-year high

## Geliştirme Planı

- [ ] BERT fine-tune ile tedarik zinciri özel NER
- [ ] Tedarikçi knowledge graph (NetworkX)
- [ ] Email / Slack alert entegrasyonu
- [ ] Türkçe haber kaynaklarının eklenmesi
- [ ] Docker containerization