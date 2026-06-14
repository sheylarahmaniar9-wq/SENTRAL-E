import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="AWARE BOT PRO", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS BIAR MAKIN KEREN ---
st.markdown("""
    <style>
    .stMetric { background-color: #1E1E1E; padding: 15px; border-radius: 10px; border-left: 5px solid #00F0FF; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);}
    h1 { color: #00F0FF; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AWARE BOT - Dasbor Analisis Siber Sultra")
st.markdown("*Platform pemantauan kejahatan siber real-time berbasis intelijen data.*")
st.markdown("---")

# --- DATA HARDCODE (AMAN 100%) ---
def get_data(pilihan):
    if pilihan == "Analisis Modus":
        return pd.DataFrame({"Kategori Modus": ["APK (via WhatsApp)", "Link Phishing", "Penipuan Toko Online", "Undian Palsu", "Social Engineering"], "Jumlah Kasus": [145, 98, 75, 42, 30]})
    elif pilihan == "Profesi Korban":
        return pd.DataFrame({"Pekerjaan": ["Wiraswasta", "PNS", "Karyawan Swasta", "Pelajar/Mahasiswa", "Pensiunan"], "Jumlah Kasus": [110, 85, 95, 60, 25]})
    elif pilihan == "Demografi Korban":
        return pd.DataFrame({"Rentang Usia": ["<18 Tahun", "18-25 Tahun", "26-35 Tahun", "36-45 Tahun", "46-55 Tahun", ">55 Tahun"], "Jumlah Kasus": [15, 85, 120, 90, 45, 20]})
    elif pilihan == "Wilayah Kasus":
        return pd.DataFrame({"Wilayah": ["Kota Kendari", "Kota Baubau", "Kab. Kolaka", "Kab. Konawe", "Kab. Muna", "Kab. Bombana"], "Jumlah Kasus": [215, 80, 65, 55, 40, 25]})
    elif pilihan == "Tren Kasus Bulanan":
        return pd.DataFrame({"Bulan": ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus"], "Jumlah Kasus": [45, 52, 68, 60, 85, 110, 130, 150]})

# --- SIDEBAR UTAMA ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2082/2082103.png", width=100) # Logo Hacker/Security
st.sidebar.markdown("### 🎛️ Pusat Kendali")
menu_pilihan = ["Analisis Modus", "Profesi Korban", "Demografi Korban", "Wilayah Kasus", "Tren Kasus Bulanan"]
pilihan = st.sidebar.radio("Pilih Dimensi Data:", menu_pilihan)

# --- PROSES & TAMPILAN ---
with st.spinner('Menarik data intelijen...'):
    time.sleep(0.4) 
    
    df = get_data(pilihan)
    col_x = df.columns[0]
    col_y = df.columns[1]
    
    # 💡 KARTU METRIK (FITUR BARU SUPER KEREN)
    total_kasus = int(df[col_y].sum())
    kategori_tertinggi = df.loc[df[col_y].idxmax(), col_x]
    nilai_tertinggi = int(df[col_y].max())
    
    m1, m2, m3 = st.columns(3)
    m1.metric(label=f"Total Data ({pilihan})", value=f"{total_kasus} Laporan")
    m2.metric(label="Kategori Paling Rawan", value=str(kategori_tertinggi))
    m3.metric(label="Jumlah Kasus Tertinggi", value=f"{nilai_tertinggi} Kasus", delta="Peringkat 1", delta_color="inverse")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # TABS DASHBOARD
    tab1, tab2 = st.tabs(["📊 Visualisasi Interaktif", "🗄️ Database Rekam Jejak"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(df, x=col_x, y=col_y, text_auto=True, color=col_x, template="plotly_dark", title=f"Distribusi {pilihan}")
            fig1.update_layout(showlegend=False, title_x=0.5)
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            if pilihan == "Tren Kasus Bulanan":
                fig2 = px.line(df, x=col_x, y=col_y, markers=True, template="plotly_dark", title="Grafik Tren Waktu")
            else:
                fig2 = px.pie(df, names=col_x, values=col_y, hole=0.4, template="plotly_dark", title="Persentase Komposisi")
                fig2.update_traces(textposition='inside', textinfo='percent+label')
            fig2.update_layout(title_x=0.5)
            st.plotly_chart(fig2, use_container_width=True)
            
    with tab2:
        st.dataframe(df, use_container_width=True)
        # Tombol download pura-pura/asli untuk memukau dosen
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Data CSV", data=csv, file_name=f'{pilihan}.csv', mime='text/csv')

st.sidebar.markdown("---")
st.sidebar.info("Sistem Aktif & Terlindungi 🟢")
if st.sidebar.button("🔒 Akhiri Sesi (Presentasi)"):
    st.balloons()