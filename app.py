import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Dashboard Analisis Penjualan",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/data_dummy_retail_store.csv")

def format_rp(x: float) -> str:
    try:
        return f"Rp {x:,.0f}".replace(",", ".")
    except Exception:
        return "Rp 0"

def kpi_card(title: str, value: str, help_text: str = ""):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(180deg, #ffffff, #fafafa);
            border: 1px solid #e7e7e7;
            border-radius: 14px;
            padding: 16px 18px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
            height: 100%;
        ">
            <div style="font-size:13px;color:#6b7280;margin-bottom:6px;">{title}</div>
            <div style="font-size:24px;font-weight:700;color:#111827;line-height:1.1;">{value}</div>
            <div style="font-size:12px;color:#9ca3af;margin-top:6px;">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

px.defaults.template = "plotly_white"

# -------------------- CLEAN DATA --------------------
df_sales = load_data()

df_sales.columns = (
    df_sales.columns.str.strip()
    .str.replace(" ", "_")
    .str.replace(".", "", regex=False)
    .str.lower()
)

drop_unnamed = [c for c in df_sales.columns if c.startswith("unnamed")]
if drop_unnamed:
    df_sales = df_sales.drop(columns=drop_unnamed)

# alias order id
if "order_id" not in df_sales.columns and "orderid" in df_sales.columns:
    df_sales["order_id"] = df_sales["orderid"]

df_sales["tanggal_pesanan"] = pd.to_datetime(df_sales["tanggal_pesanan"])

# -------------------- SIDEBAR --------------------
st.sidebar.markdown("### Filter & Navigasi")
pilihan_halaman = st.sidebar.radio(
    "Pilih Halaman:",
    ("Overview Dashboard", "Prediksi Penjualan"),
    index=0,
)

min_date = df_sales["tanggal_pesanan"].min().date()
max_date = df_sales["tanggal_pesanan"].max().date()

# Filter aktif untuk Overview
if pilihan_halaman == "Overview Dashboard":
    st.sidebar.markdown("#### Filter Dashboard")
    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if len(date_range) == 2:
        start_date_filter = pd.to_datetime(date_range[0])
        end_date_filter = pd.to_datetime(date_range[1])
        filtered_df = df_sales[
            (df_sales["tanggal_pesanan"] >= start_date_filter)
            & (df_sales["tanggal_pesanan"] <= end_date_filter)
        ]
    else:
        filtered_df = df_sales.copy()

    regions = df_sales["wilayah"].dropna().unique().tolist()
    selected_regions = st.sidebar.multiselect(
        "Pilih Wilayah:", options=regions, default=regions
    )
    filtered_df = filtered_df[filtered_df["wilayah"].isin(selected_regions)]

    categories = df_sales["kategori"].dropna().unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Pilih Kategori Produk:", options=categories, default=categories
    )
    filtered_df = filtered_df[filtered_df["kategori"].isin(selected_categories)]
else:
    filtered_df = df_sales.copy()

# -------------------- HEADER --------------------
st.title("Dashboard Penjualan HelloMart")
st.image("src/shope.jpg", caption="HelloMart Logo", use_container_width=False, width=900)
st.caption("Gunakan filter di sidebar untuk mengeksplorasi data.")

# -------------------- OVERVIEW --------------------
if pilihan_halaman == "Overview Dashboard":
    if filtered_df.empty:
        st.warning("Tidak ada data untuk filter yang dipilih. Silakan longgarkan filter.")
        st.stop()

    # KPI cards
    col1, col2, col3, col4 = st.columns([3, 2, 3, 2])
    total_sales = float(filtered_df["total_penjualan"].sum())
    total_orders = int(
        filtered_df["orderid"].nunique()
        if "orderid" in filtered_df
        else filtered_df["order_id"].nunique()
    )
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    total_products_sold = int(filtered_df["jumlah"].sum())

    with col1:
        kpi_card("Total Penjualan", format_rp(total_sales), "Akumulasi total revenue")
    with col2:
        kpi_card("Jumlah Pesanan", f"{total_orders:,}".replace(",", "."), "Unique Order")
    with col3:
        kpi_card("Rata-Rata Nilai Pesanan", format_rp(avg_order_value), "Avg. order value")
    with col4:
        kpi_card("Jumlah Produk Terjual", f"{total_products_sold:,}".replace(",", "."), "Item units")

    st.markdown("---")

    # Charts utama
    g1, g2 = st.columns(2)

    # Penjualan per Wilayah
    with g1:
        st.subheader("Total Penjualan per Wilayah")
        sales_by_region = (
            filtered_df.groupby("wilayah", as_index=False)["total_penjualan"]
            .sum()
            .sort_values("total_penjualan", ascending=False)
        )
        fig_region = px.bar(
            sales_by_region, x="wilayah", y="total_penjualan", text_auto=True
        )
        st.plotly_chart(fig_region, use_container_width=True)

    # Distribusi Kategori
    with g2:
        st.subheader("Distribusi Penjualan per Kategori")
        sales_by_category = filtered_df.groupby("kategori", as_index=False)["total_penjualan"].sum()
        fig_pie = px.pie(sales_by_category, values="total_penjualan", names="kategori", hole=0.45)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # Top Produk
    st.subheader("Top 10 Produk Terlaris")
    top_product_sold = (
        filtered_df.groupby("produk", as_index=False)["total_penjualan"]
        .sum()
        .nlargest(10, "total_penjualan")
        .sort_values("total_penjualan")
    )
    fig_top = px.bar(
        top_product_sold, x="total_penjualan", y="produk", orientation="h", text_auto=True
    )
    st.plotly_chart(fig_top, use_container_width=True)

    # -------------------- TABS --------------------
    st.subheader("Performa Penjualan Lebih Detail")
    tab1, tab2, tab3 = st.tabs(["Hari dalam Seminggu", "Kategori Produk", "Top 5 Produk"])

    # Tab 1: Hari
    with tab1:
        sales_by_day = (
            filtered_df.groupby("hari_dalam_seminggu", as_index=False)["total_penjualan"]
            .sum().sort_values("total_penjualan", ascending=False)
        )
        fig_day = px.bar(sales_by_day, x="hari_dalam_seminggu", y="total_penjualan", text_auto=True, color="hari_dalam_seminggu")
        st.plotly_chart(fig_day, use_container_width=True)

    # Tab 2: Kategori
    with tab2:
        sales_by_category = (
            filtered_df.groupby("kategori", as_index=False)["total_penjualan"]
            .sum().sort_values("total_penjualan", ascending=False)
        )
        fig_cat = px.bar(sales_by_category, x="kategori", y="total_penjualan", text_auto=True, color="kategori")
        st.plotly_chart(fig_cat, use_container_width=True)

    # Tab 3: Top 5 Produk
    with tab3:
        top_products = (
            filtered_df.groupby("produk", as_index=False)["total_penjualan"]
            .sum().nlargest(5, "total_penjualan")
            .sort_values("total_penjualan")
        )
        fig_prod = px.bar(top_products, x="total_penjualan", y="produk", orientation="h", text_auto=True, color="produk")
        st.plotly_chart(fig_prod, use_container_width=True)

# -------------------- PREDIKSI --------------------
elif pilihan_halaman == "Prediksi Penjualan":
    st.subheader("Prediksi Penjualan Sederhana")

    sales_by_month = df_sales.groupby("bulan", as_index=False)["total_penjualan"].sum()
    avg_sales = sales_by_month["total_penjualan"].mean()
    n_pred = st.slider("Prediksi berapa bulan ke depan?", 1, 6, 3)

    pred_df = pd.DataFrame({
        "bulan": [f"Prediksi {i+1}" for i in range(n_pred)],
        "total_penjualan": [avg_sales] * n_pred
    })

    st.write("### Tabel Prediksi")
    st.dataframe(pred_df.style.format({"total_penjualan": "Rp {:,.0f}"}))

    fig_pred = px.bar(sales_by_month, x="bulan", y="total_penjualan",
                      title="Ringkasan Penjualan Bulanan (Histori) & Proyeksi Sederhana")
    fig_pred.add_scatter(x=pred_df["bulan"], y=pred_df["total_penjualan"],
                         mode="lines+markers", name="Prediksi (Rata-rata)",
                         line=dict(dash="dot", color="red"))
    st.plotly_chart(fig_pred, use_container_width=True)

st.caption("© 2025 Retail Analytics — Maulana")
