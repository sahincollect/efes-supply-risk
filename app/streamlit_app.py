import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import os

st.set_page_config(
    page_title="Efes Tedarik Zinciri Risk Analizi",
    page_icon="🏭",
    layout="wide"
)

st.title("Efes Tedarik Zinciri Risk Analizi")
st.caption("Gerçek zamanlı haber tabanlı risk izleme sistemi")

def run_pipeline():
    with st.spinner("Haberler toplanıyor..."):
        subprocess.run(["python", "src/collectors/rss_collector.py"], check=True)
        subprocess.run(["python", "src/collectors/gdelt_collector.py"], check=True)
    with st.spinner("NLP analizi yapılıyor..."):
        subprocess.run(["python", "src/nlp/sentiment_analyzer.py"], check=True)
    with st.spinner("Risk skorlanıyor..."):
        subprocess.run(["python", "src/scoring/risk_engine.py"], check=True)
    st.success("Pipeline tamamlandı!")
    st.rerun()

@st.cache_data
def load_data():
    try:
        gdelt = pd.read_csv("data/processed/gdelt_scored.csv")
        rss = pd.read_csv("data/processed/articles.csv")
        return gdelt, rss
    except Exception:
        return pd.DataFrame(), pd.DataFrame()

gdelt, rss = load_data()

if gdelt.empty:
    st.warning("Henüz veri yok. Pipeline'ı başlatmak için aşağıdaki butona bas.")
    if st.button("Pipeline Başlat"):
        run_pipeline()
    st.stop()

col1, col2, col3, col4 = st.columns(4)
kritik = len(gdelt[gdelt["alert"] == "KRITIK"])
orta = len(gdelt[gdelt["alert"] == "ORTA"])
dusuk = len(gdelt[gdelt["alert"] == "DUSUK"])
ort_skor = round(gdelt["risk_score"].mean(), 1)

col1.metric("Kritik Alert", kritik)
col2.metric("Orta Alert", orta)
col3.metric("Düşük Risk", dusuk)
col4.metric("Ortalama Skor", ort_skor)

if st.button("Verileri Yenile"):
    st.cache_data.clear()
    run_pipeline()

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Risk Dağılımı")
    alert_counts = gdelt["alert"].value_counts().reset_index()
    alert_counts.columns = ["alert", "count"]
    color_map = {"KRITIK": "#E24B4A", "ORTA": "#EF9F27", "DUSUK": "#639922"}
    fig_pie = px.pie(
        alert_counts,
        names="alert",
        values="count",
        color="alert",
        color_discrete_map=color_map
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("Risk Skoru Dağılımı")
    fig_hist = px.histogram(
        gdelt,
        x="risk_score",
        nbins=20,
        color_discrete_sequence=["#378ADD"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

st.subheader("En Yüksek Riskli Haberler")
alert_filter = st.selectbox("Filtrele", options=["Tümü", "KRITIK", "ORTA", "DUSUK"])
filtered = gdelt if alert_filter == "Tümü" else gdelt[gdelt["alert"] == alert_filter]
filtered = filtered.sort_values("risk_score", ascending=False)

for _, row in filtered.head(15).iterrows():
    color = {"KRITIK": "🔴", "ORTA": "🟡", "DUSUK": "🟢"}.get(row["alert"], "⚪")
    with st.expander(f"{color} [{row['risk_score']}] {row['title'][:100]}..."):
        col_a, col_b, col_c = st.columns(3)
        col_a.write(f"**Risk Skoru:** {row['risk_score']}")
        col_b.write(f"**Alert:** {row['alert']}")
        col_c.write(f"**Kaynak:** {row.get('source', '-')}")
        if row.get("url"):
            st.markdown(f"[Habere git →]({row['url']})")

st.divider()

st.subheader("Son RSS Haberleri")
if not rss.empty:
    st.dataframe(
        rss[["title", "source", "published"]].head(20),
        use_container_width=True
    )