import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from statistics import mode, StatisticsError

st.set_page_config(page_title="Simulasi Statistik Deskriptif", layout="centered")
st.title("📊 Simulasi Statistik Deskriptif")

# Input tipe
input_type = st.radio("Pilih metode input data:", ["Input Manual", "Upload File CSV"])

# Input data
if input_type == "Input Manual":
    user_input = st.text_area("Masukkan data numerik (pisahkan dengan koma atau spasi):")
    if user_input:
        try:
            data = [float(i) for i in user_input.replace(',', ' ').split()]
            df = pd.DataFrame(data, columns=["Data"])
        except:
            st.error("Pastikan hanya memasukkan angka yang valid!")
            st.stop()
    else:
        st.warning("Masukkan data terlebih dahulu")
        st.stop()

else:
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_columns:
                st.error("Tidak ada kolom numerik dalam file.")
                st.stop()
            selected_col = st.selectbox("Pilih kolom numerik:", numeric_columns)
            df = df[[selected_col]].dropna().rename(columns={selected_col: "Data"})
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            st.stop()
    else:
        st.warning("Upload file CSV terlebih dahulu")
        st.stop()

# Statistik Deskriptif
st.subheader("📈 Statistik Deskriptif")

data = df["Data"]
try:
    data_mode = mode(data)
except StatisticsError:
    data_mode = "Tidak unik"

stats = {
    "Mean (Jumlah Data Keseluruhan)": np.mean(data),
    "Median (Nilai Tengah Saat Data Diurutkan)": np.median(data),
    "Modus (Nilai yang Paling Sering Muncul)": data_mode,
    "Varians (Rata-rata Kuadrat Selisih Tiap Data Terhadap Mean)": np.var(data, ddof=1),
    "Standar Deviasi (Akar dari varians (sebaran data dari rata-rata)": np.std(data, ddof=1)
}
st.table(pd.DataFrame(stats, index=["Nilai"]).T)

# Visualisasi
st.subheader("🖼️ Visualisasi Data")
chart_type = st.selectbox("Pilih jenis grafik:", ["Boxplot", "Histogram"])

fig, ax = plt.subplots()
if chart_type == "Boxplot":
    sns.boxplot(data, ax=ax)
    ax.set_title("Boxplot")
else:
    sns.histplot(data, kde=True, ax=ax)
    ax.set_title("Histogram")
    ax.set_xlabel("Nilai")

st.pyplot(fig)
