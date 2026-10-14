import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard COVID-19 ASEAN", layout="wide")

@st.cache_data
def load_data():
    return pd.read_parquet("data/processed/covid_asean.parquet")

df = load_data()

st.title("Dashboard Analisis COVID-19 ASEAN")
st.caption("Sumber data: Our World in Data. Periode 2020-2022.")

# ---------- Sidebar ----------
st.sidebar.header("Filter")
negara = st.sidebar.multiselect(
    "Pilih negara", sorted(df["location"].unique()),
    default=[n for n in ["Indonesia", "Malaysia"] if n in df["location"].unique()],
)
tgl = st.sidebar.date_input("Rentang tanggal", [df["date"].min(), df["date"].max()])

label_metrik = {
    "Kasus per 100k (MA7)": "cases_ma7",
    "Kematian per 100k (MA7)": "deaths_ma7",
    "CFR kumulatif (%)": "cfr",
}
if df["people_fully_vaccinated_per_hundred"].notna().any():
    label_metrik["Vaksinasi lengkap (per 100 penduduk)"] = "people_fully_vaccinated_per_hundred"

pilihan = st.sidebar.selectbox("Metrik", list(label_metrik))
metrik = label_metrik[pilihan]

if not negara or len(tgl) != 2:
    st.info("Pilih minimal satu negara dan rentang tanggal lengkap.")
    st.stop()

d = df[df["location"].isin(negara) &
       df["date"].between(pd.to_datetime(tgl[0]), pd.to_datetime(tgl[1]))]

# ---------- KPI ----------
c1, c2, c3 = st.columns(3)
c1.metric("Total Kasus", f"{d['new_cases'].sum():,.0f}")
c2.metric("Total Kematian", f"{d['new_deaths'].sum():,.0f}")
c3.metric("Negara Dipilih", len(negara))

# ---------- Tab ----------
tab1, tab2, tab3 = st.tabs(["Tren Waktu", "Perbandingan", "Catatan & Keterbatasan"])

with tab1:
    st.plotly_chart(
        px.line(d, x="date", y=metrik, color="location",
                labels={metrik: pilihan, "date": "Tanggal", "location": "Negara"}),
        use_container_width=True,
    )

with tab2:
    agg = d.groupby("location").agg(
        kasus_per_100k=("cases_per_100k", "sum"),
        kematian_per_100k=("deaths_per_100k", "sum"),
    ).reset_index()
    a, b = st.columns(2)
    a.plotly_chart(px.bar(agg, x="location", y="kasus_per_100k", color="location",
                          title="Total Kasus per 100k"), use_container_width=True)
    b.plotly_chart(px.bar(agg, x="location", y="kematian_per_100k", color="location",
                          title="Total Kematian per 100k"), use_container_width=True)

with tab3:
    st.markdown("""
    - Angka dinormalisasi per 100.000 penduduk agar adil antar negara.
    - Rata-rata bergerak 7 hari dipakai untuk meredam fluktuasi harian.
    - Perbedaan tingkat testing dan sistem pelaporan membuat perbandingan kasus tidak sepenuhnya setara.
    - Hubungan vaksinasi dan kematian bersifat korelasi, bukan sebab-akibat.
    - Nilai harian negatif (koreksi data) diubah menjadi 0.
    """)
