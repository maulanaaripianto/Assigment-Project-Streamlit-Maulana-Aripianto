# 📊 Dashboard Penjualan HelloMart

Dashboard interaktif berbasis **Streamlit** untuk menganalisis performa penjualan **HelloMart**.  
Aplikasi ini menampilkan ringkasan KPI, analisis per wilayah & kategori, produk terlaris, hingga **prediksi penjualan sederhana** untuk mendukung pengambilan keputusan bisnis.

---

## 🚀 Fitur Utama

- **Ringkasan KPI**: Total penjualan, jumlah pesanan, rata-rata nilai order, jumlah produk terjual.  
- **Analisis Per Wilayah**: Grafik batang total penjualan per kota (Jakarta, Surabaya, Medan, Makassar, Denpasar).  
- **Distribusi Kategori**: Donut chart perbandingan Elektronik, Periferal, dan Aksesoris.  
- **Top Produk Terlaris**: Ranking produk dengan kontribusi penjualan tertinggi (contoh: Laptop Gaming, Smartphone Terbaru).  
- **Performa Lebih Detail**:  
  - Tren penjualan harian dalam seminggu.  
  - Performa per kategori.  
  - Analisis **Top 5 Produk**.  
- **Prediksi Penjualan**: Proyeksi sederhana untuk beberapa bulan ke depan berdasarkan rata-rata historis.  

---

## 🖼️ Cuplikan Layar

### Overview Dashboard
![Overview](assets/overview.png)

### Top Produk Terlaris
![Top Produk](assets/top-products.png)

### Distribusi Kategori
![By Category](assets/by-category.png)

### Top 5 Produk
![Top 5 Produk](assets/top5-products.png)

### Prediksi Penjualan
![Forecast](assets/forecast.png)

---

## 🛠️ Tech Stack

- Python 3.10+  
- Streamlit  
- Pandas, Numpy  
- Plotly / Altair (visualisasi)  
- scikit-learn / statsmodels (prediksi sederhana)  

## 📦 Contoh requirements.txt
- streamlit>=1.36
- pandas>=2.0
- numpy>=1.24
- plotly>=5.20
- altair>=5.0
- scikit-learn>=1.3
statsmodels>=0.14
