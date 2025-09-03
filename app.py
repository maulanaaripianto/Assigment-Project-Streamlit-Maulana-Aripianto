import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Dashboard Analisis Penjualan",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Base path ke folder tempat app.py berada
BASE_DIR = Path(__file__).parent

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    csv_path = BASE_DIR / "data" / "data_dummy_retail_store.csv"
    if not csv_path.exists():
        st.error(f"File data tidak ditemukan: {csv_path}")
        st.stop()
    df = pd.read_csv(csv_path)

    # Normalisasi kolom
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace(".", "", regex=False)
        .str.lower()
    )

    # Drop kolom 'unnamed' bila ada
    drop_unnamed = [c for c in df.columns if c.startswith("unnamed")]
    if drop_unnamed:
        df = df.drop(columns=drop_unnamed)

    # Alias order id
    if "order_id" not in df.columns and "orderid" in df.columns:
        df["order_id"] = df["orderid"]

    # Tanggal
    if "tanggal_pesanan" in df.columns:
        df["tanggal_pesanan"] = pd.to_datetime(df["tanggal_pesanan"], errors="coerce")

    # Pastikan numerik
    for c in ["total_penjualan", "jumlah"]:
        if c i
