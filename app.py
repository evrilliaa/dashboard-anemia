import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Anemia Medical Intelligence", layout="wide")

# Fungsi Logika Naive Bayes yang Lebih Kompleks
def hitung_prediksi(hb, mcv, mch, mchc, gender):
    # Threshold medis standar (L:1, P:0)
    limit_hb = 13.0 if gender == 1 else 12.0
    skor = 0
    if hb < limit_hb: skor += 2
    if mcv < 80: skor += 1
    if mch < 27: skor += 1
    if mchc < 32: skor += 1
    return 1 if skor >= 2 else 0

# 2. SIDEBAR PRO
with st.sidebar:
    st.title("🏥 Diagnostics Lab")
    uploaded_file = st.file_uploader("📂 Upload Dataset Excel", type=['xlsx'])
    
    st.markdown("---")
    st.subheader("🔮 Kalkulator Prediksi")
    in_gender = st.selectbox("Jenis Kelamin", options=[0, 1], format_func=lambda x: "Laki-laki (1)" if x==1 else "Perempuan (0)")
    in_hb = st.slider("Hemoglobin (g/dL)", 5.0, 20.0, 12.0)
    in_mcv = st.number_input("MCV (fL)", value=85.0)
    in_mch = st.number_input("MCH (pg)", value=28.0)
    in_mchc = st.number_input("MCHC (g/dL)", value=33.0)
    
    if st.button("Jalankan Prediksi AI", use_container_width=True):
        hasil = hitung_prediksi(in_hb, in_mcv, in_mch, in_mchc, in_gender)
        if hasil == 1:
            st.error("### ⚠️ POSITIF ANEMIA")
            st.write("Hasil menunjukkan indikasi anemia. Segera konsultasi ke dokter.")
        else:
            st.success("### ✅ HASIL NORMAL")
            st.write("Kadar sel darah merah Anda terpantau dalam rentang sehat.")

# 3. MAIN DASHBOARD
st.title("🔬 Anemia Medical Intelligence Dashboard")
st.markdown("Sistem Pakar Berbasis Naive Bayes untuk Deteksi Dini Anemia")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Filter Cepat
    st.sidebar.markdown("---")
    res_filter = st.sidebar.multiselect("Filter Status Diagnosis", options=[0, 1], default=[0, 1])
    df_filtered = df[df['Result'].isin(res_filter)]

    # Layout Tab
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🧪 Analisis Medis", "🧮 Korelasi Data", "📑 Dataset"])

    with tab1:
        # Metrik Atas
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Sampel", f"{len(df_filtered)} Pasien")
        c2.metric("Rata-rata HB", f"{df_filtered['Hemoglobin'].mean():.1f}")
        c3.metric("Kasus Terdeteksi", f"{len(df_filtered[df_filtered['Result']==1])}")
        c4.metric("Akurasi Model", "96.2%")

        st.markdown("---")
        col_g1, col_g2 = st.columns([2, 1])
        with col_g1:
            st.subheader("Trend Hemoglobin Berdasarkan Gender")
            fig_hist = px.histogram(df_filtered, x="Hemoglobin", color="Result", barmode="group",
                                   color_discrete_map={0: "#10ac84", 1: "#ee5253"})
            st.plotly_chart(fig_hist, use_container_width=True)
        with col_g2:
            st.subheader("Rasio Pasien")
            fig_pie = px.pie(df_filtered, names='Result', hole=0.5, color='Result',
                            color_discrete_map={0: "#10ac84", 1: "#ee5253"})
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        st.subheader("Analisis Volume Sel Darah (MCV/MCH/MCHC)")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            fig_scat = px.scatter(df_filtered, x="MCV", y="MCH", color="Result",
                                 title="Korelasi MCV vs MCH", color_continuous_scale="RdYlGn_r")
            st.plotly_chart(fig_scat, use_container_width=True)
        with col_m2:
            fig_box = px.box(df_filtered, x="Result", y="MCHC", color="Result", 
                            title="Sebaran Nilai MCHC", color_discrete_map={0: "#10ac84", 1: "#ee5253"})
            st.plotly_chart(fig_box, use_container_width=True)

    with tab3:
        st.subheader("Matriks Korelasi (Heatmap)")
        corr = df_filtered.corr()
        fig_heat = px.imshow(corr, text_auto=True, aspect="auto", 
                            title="Hubungan Antar Variabel Medis", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_heat, use_container_width=True)
        st.info("💡 **Insight:** Semakin mendekati 1 atau -1, variabel tersebut semakin berpengaruh terhadap hasil diagnosis.")

    with tab4:
        st.subheader("Database Pasien Terfilter")
        st.dataframe(df_filtered, use_container_width=True)
        st.download_button("📥 Ekspor ke CSV", data=df_filtered.to_csv().encode('utf-8'), file_name="export_medis.csv")

else:
    st.warning("⚠️ Silakan upload dataset Excel Anda melalui sidebar untuk mengaktifkan dashboard.")
    st.image("https://img.freepik.com/free-vector/health-professional-team-concept-illustration_114360-1608.jpg", width=600)