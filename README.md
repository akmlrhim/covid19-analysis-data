# Analisis COVID-19 Negara-Negara ASEAN

Dashboard interaktif dan exploratory data analysis (EDA) untuk membandingkan tren kasus, kematian, dan vaksinasi COVID-19 di 6 negara ASEAN selama periode **Maret 2020 – Desember 2022**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://covid19-analysis-data-mc3lzrvpj5mqhfgtezages.streamlit.app/)

🔗 **Live Demo**: [covid19-analysis-data.streamlit.app](https://covid19-analysis-data-mc3lzrvpj5mqhfgtezages.streamlit.app/)

---

## Latar Belakang

Pandemi COVID-19 berdampak berbeda pada setiap negara tergantung populasi, kebijakan kesehatan, dan kapasitas testing. Perbandingan angka mentah antar negara tidak adil karena perbedaan ukuran populasi. Proyek ini menjawab pertanyaan:

> **Bagaimana tren kasus dan kematian COVID-19 di negara-negara ASEAN jika dinormalisasi per kapita, dan bagaimana hubungannya dengan cakupan vaksinasi?**

---

## Negara yang Dianalisis

| Negara    | Populasi (estimasi 2021) |
| --------- | ------------------------ |
| Indonesia | 275.500.000              |
| Malaysia  | 33.900.000               |
| Filipina  | 115.600.000              |
| Singapura | 5.600.000                |
| Thailand  | 71.700.000               |
| Vietnam   | 98.200.000               |

---

## Sumber Data

Data bersumber dari **[Our World in Data (OWID)](https://ourworldindata.org/coronavirus)** — dataset publik yang dikurasi oleh Universitas Oxford.

- **Dataset**: `owid-covid-data.csv` (429.435 baris, 67 kolom)
- **URL**: [GitHub OWID](https://github.com/owid/covid-19-data)
- **Lisensi**: CC BY 4.0

---

## Metodologi

### 1. Pengumpulan & Pembersihan Data

- Filter 6 negara ASEAN dari dataset global
- Batasi periode: 1 Maret 2020 – 31 Desember 2022
- Nilai negatif pada kasus/kematian harian (koreksi data) diubah menjadi 0
- Forward-fill untuk kolom kumulatif yang kosong
- Cek missing value per kolom

### 2. Feature Engineering

| Fitur             | Deskripsi                                   |
| ----------------- | ------------------------------------------- |
| `cases_per_100k`  | Kasus harian per 100.000 penduduk           |
| `deaths_per_100k` | Kematian harian per 100.000 penduduk        |
| `cases_ma7`       | Rata-rata bergerak 7 hari kasus per 100k    |
| `deaths_ma7`      | Rata-rata bergerak 7 hari kematian per 100k |
| `cfr`             | Case Fatality Rate kumulatif (%)            |

### 3. Analisis yang Dilakukan

1. **Tren Waktu** — Line chart kasus harian per 100k (MA7) keenam negara
2. **Heatmap Bulanan** — Intensitas kasus per bulan x negara untuk identifikasi gelombang
3. **Deteksi Puncak (Peak Detection)** — Algoritma `scipy.signal.find_peaks` untuk identifikasi gelombang COVID-19 per negara
4. **Visualisasi Gelombang per Negara** — Line chart dengan marker puncak
5. **Korelasi Vaksinasi vs Kematian** — Bar chart grouped: rata-rata kematian per 100k berdasarkan tingkat cakupan vaksinasi
6. **Perbandingan Agregat** — Total kasus dan kematian per 100k antar negara

### 4. Dashboard Interaktif

Dashboard **Streamlit** dengan fitur:

- Filter multi-negara
- Filter rentang tanggal
- Pilihan metrik: kasus MA7, kematian MA7, CFR, vaksinasi
- Tab: Tren Waktu, Perbandingan, Catatan & Keterbatasan
- KPI ringkas: total kasus, total kematian, jumlah negara

---

## Struktur Proyek

```
covid-analysis/
├── app.py                          # Dashboard Streamlit
├── index.ipynb                     # Notebook analisis (Google Colab)
├── requirements.txt                # Dependensi Python
├── data/
│   ├── raw/                        # Data mentah OWID (CSV)
│   └── processed/
│       └── covid_asean.parquet     # Data hasil cleaning & feature engineering
└── README.md
```

---

## Tech Stack

| Kategori        | Teknologi            |
| --------------- | -------------------- |
| Bahasa          | Python 3.10+         |
| Manipulasi Data | Pandas, NumPy        |
| Visualisasi     | Plotly               |
| Analisis Sinyal | SciPy (`find_peaks`) |
| Dashboard       | Streamlit            |
| Format Data     | Parquet (PyArrow)    |
| Environment     | Google Colab         |

---

## Cara Menjalankan

### Prasyarat

- Python 3.10+
- pip

### Instalasi

```bash
# Clone repositori
git clone https://github.com/akmlrhim/covid19-analysis-data.git
cd covid19-analysis-data

# Buat virtual environment (opsional tapi disarankan)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependensi
pip install -r requirements.txt
```

### Jalankan Dashboard

```bash
streamlit run app.py
```

Dashboard terbuka di `http://localhost:8501`.

**Atau coba langsung versi online**: [Live Demo Streamlit](https://covid19-analysis-data-mc3lzrvpj5mqhfgtezages.streamlit.app/)

### Jalankan Notebook Analisis

Buka `index.ipynb` di Jupyter Notebook, VS Code, atau Google Colab.

---

## Temuan Utama

| Negara    | Kasus per 100k | Kematian per 100k |
| --------- | -------------- | ----------------- |
| Singapura | 38.917,7       | 30,4              |
| Malaysia  | 14.801,3       | 108,5             |
| Vietnam   | 11.737,0       | 44,0              |
| Thailand  | 6.585,7        | 46,9              |
| Filipina  | 3.512,8        | 56,5              |
| Indonesia | 2.437,8        | 58,3              |

- **Singapura** punya kasus per kapita tertinggi, namun kematian per kapita terendah — mengindikasikan tingkat testing tinggi dan sistem kesehatan kuat.
- **Malaysia** memiliki kematian per kapita tertinggi di antara keenam negara.
- **Indonesia** kasus per kapita relatif rendah, namun CFR cukup tinggi — kemungkinan dipengaruhi under-reporting dan kapasitas testing terbatas di awal pandemi.
- Gelombang terbesar di mayoritas negara terjadi pada periode **Juli–September 2021** (varian Delta) dan **Februari–April 2022** (varian Omicron).

---

## Keterbatasan

- Data kasus bergantung pada kapasitas testing dan kebijakan setiap negara — perbandingan tidak sepenuhnya setara.
- Hubungan vaksinasi dan kematian bersifat **korelasi, bukan sebab-akibat**.
- Tidak memperhitungkan faktor perancah (confounding) seperti usia populasi, komorbiditas, atau kebijakan kesehatan spesifik.
- Data OWID berhenti diperbarui Agustus 2024; analisis ini dibatasi sampai Desember 2022.

---

## Lisensi

Proyek ini dibuat untuk keperluan edukasi dan portofolio. Data bersumber dari [Our World in Data](https://ourworldindata.org/coronavirus) di bawah lisensi **CC BY 4.0**.

---

## Kontak

Dibuat oleh **Akmal Rahim** — [GitHub](https://github.com/akmlrhim)
