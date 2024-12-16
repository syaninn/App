import streamlit as st
import datetime
import pandas as pd
from colorsys import rgb_to_hls

# Fungsi warna teks otomatis
def warna_teks_otomatis(background_color):
    bg_color = background_color.lstrip('#')
    r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
    luminance = rgb_to_hls(r/255, g/255, b/255)[1]
    return '#FFFFFF' if luminance < 0.5 else '#000000'

# Fungsi untuk menerapkan tema global dengan CSS
def set_theme(background_color, sidebar_color, font_family, font_size):
    text_color = warna_teks_otomatis(background_color)
    sidebar_text_color = warna_teks_otomatis(sidebar_color)
    st.markdown(
        f"""
        <style>
        /* Latar belakang utama */
        .stApp {{
            background-color: {background_color} !important;
            color: {text_color} !important;
            font-family: '{font_family}' !important;
            font-size: {font_size}px !important;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_color} !important;
            color: {sidebar_text_color} !important;
            font-family: '{font_family}' !important;
            font-size: {font_size}px !important;
        }}

        /* Semua teks di input, slider, button, dsb */
        * {{
            font-family: '{font_family}', sans-serif !important;
            font-size: {font_size}px !important;
        }}

        /* Tombol dan input spesifik */
        button, input, textarea {{
            font-family: '{font_family}', sans-serif !important;
            font-size: {font_size}px !important;
        }}

        /* Komponen teks lain */
        .stTextInput, .stNumberInput, .stDateInput, .stRadio, .stMarkdown {{
            font-family: '{font_family}' !important;
            font-size: {font_size}px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Fungsi menghitung BMI
def hitung_bmi(berat, tinggi):
    return berat / ((tinggi / 100) ** 2)

# Fungsi menghitung Berat Badan Ideal
def hitung_bb_ideal(tinggi):
    return 22 * ((tinggi / 100) ** 2)

# Fungsi status BMI
def status_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "Perbanyak konsumsi makanan bergizi.", "Cobalah makan makanan berkalori tinggi seperti daging, kacang-kacangan, dan susu."
    elif 18.5 <= bmi < 24.9:
        return "Normal", "Pertahankan pola makan seimbang dan olahraga.", "Anda dalam kondisi sehat. Pertahankan gaya hidup aktif dan makan makanan bergizi."
    elif 25 <= bmi < 29.9:
        return "Overweight", "Kurangi konsumsi lemak dan gula, tingkatkan olahraga.", "Lakukan olahraga rutin seperti jogging atau bersepeda selama 30 menit per hari."
    else:
        return "Obesitas", "Konsultasikan dengan dokter atau ahli gizi.", "Hindari makanan cepat saji dan tingkatkan aktivitas fisik untuk mengontrol berat badan."

# Fungsi menu pengaturan tema
def pengaturan_tema():
    st.title("Pengaturan Tema")
    # Warna latar belakang dan sidebar
    bg_color = st.color_picker("Warna Latar Belakang", st.session_state["theme"]["background_color"])
    sidebar_color = st.color_picker("Warna Sidebar", st.session_state["theme"]["sidebar_color"])
    # Font dan ukuran font
    font_family = st.selectbox("Pilih Font", ["Arial", "Courier", "Verdana", "Times New Roman"], 
                               index=["Arial", "Courier", "Verdana", "Times New Roman"].index(st.session_state["theme"]["font_family"]))
    font_size = st.slider("Ukuran Font", 10, 50, st.session_state["theme"]["font_size"])

    # Tombol terapkan
    if st.button("Terapkan"):
        st.session_state["theme"] = {
            "background_color": bg_color,
            "sidebar_color": sidebar_color,
            "font_family": font_family,
            "font_size": font_size
        }
        st.success("Pengaturan berhasil diterapkan!")
        st.rerun()

# Inisialisasi sesi tema dan data
if "theme" not in st.session_state:
    st.session_state["theme"] = {
        "background_color": "#FFFFFF",
        "sidebar_color": "#F0F2F6",
        "font_family": "Arial",
        "font_size": 16
    }
if "data" not in st.session_state:
    st.session_state["data"] = []

# Terapkan tema global
set_theme(
    st.session_state["theme"]["background_color"],
    st.session_state["theme"]["sidebar_color"],
    st.session_state["theme"]["font_family"],
    st.session_state["theme"]["font_size"]
)

# Menu Utama
menu = st.sidebar.radio("Pilih Menu", ["Mulai", "Pengaturan", "Hasil Tersimpan", "Penjelasan", "Keluar"])

if menu == "Pengaturan":
    pengaturan_tema()

elif menu == "Mulai":
    st.title("Aplikasi Pengecek Berat Badan")

    nama = st.text_input("Masukkan Nama Anda")
    tanggal = st.date_input("Tanggal Hari Ini", datetime.date.today())
    umur = st.number_input("Masukkan Umur Anda", min_value=5, max_value=100)
    jenis_kelamin = st.radio("Pilih Jenis Kelamin", ["Pria", "Wanita"])
    berat = st.number_input("Masukkan Berat Badan Anda (kg)", min_value=10.0)
    tinggi = st.number_input("Masukkan Tinggi Badan Anda (cm)", min_value=50.0)

    if st.button("Hitung BMI"):
        if nama and berat > 0 and tinggi > 0:
            bmi = hitung_bmi(berat, tinggi)
            bb_ideal = hitung_bb_ideal(tinggi)
            status, saran, tips = status_bmi(bmi)

            # Menyimpan hasil ke dalam session state
            st.session_state["data"].append({
                "Nama": nama,
                "Tanggal": tanggal,
                "Umur": umur,
                "Jenis Kelamin": jenis_kelamin,
                "Berat": berat,
                "Tinggi": tinggi,
                "BMI": bmi,
                "Berat Badan Ideal": bb_ideal
            })

            st.subheader("Hasil Perhitungan Anda:")
            st.write(f"**BMI Anda:** {bmi:.2f}")
            st.write(f"**Berat Badan Ideal:** {bb_ideal:.2f} kg")
            st.write(f"**Status BMI:** {status}")
            st.info(f"**Saran:** {saran}")
            st.success(f"**Tips Tambahan:** {tips}")
        else:
            st.error("Harap isi semua data dengan benar!")

elif menu == "Hasil Tersimpan":
    st.title("Hasil Tersimpan")
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.table(df)
        if st.button("Hapus Data"):
            st.session_state["data"] = []
            st.success("Data berhasil dihapus!")
            st.rerun()
    else:
        st.info("Belum ada data yang tersimpan.")

elif menu == "Penjelasan":
    st.title("Penjelasan tentang BMI dan Berat Badan Ideal")
    st.write("""
    **BMI (Body Mass Index)** adalah ukuran yang digunakan untuk menilai apakah seseorang memiliki berat badan yang sehat berdasarkan tinggi badan mereka. 
    Rumus untuk menghitung BMI adalah:
    
    \[ BMI = \frac{berat \, (kg)}{(tinggi \, (m))^2} \]
    
    Kategori BMI adalah sebagai berikut:
    - **Underweight**: BMI kurang dari 18.5
    - **Normal**: BMI antara 18.5 dan 24.9
    - **Overweight**: BMI antara 25 dan 29.9
    - **Obesitas**: BMI 30 atau lebih

    **Berat Badan Ideal** adalah berat badan yang dianggap sehat untuk tinggi badan tertentu. 
    Berat badan ideal dapat dihitung dengan rumus:
    
    \[ Berat \, Badan \, Ideal = 22 \times (tinggi \, (m))^2 \]

    Mempertahankan berat badan ideal penting untuk kesehatan secara keseluruhan dan dapat membantu mencegah berbagai penyakit.
    """)

elif menu == "Keluar":
    st.title("Terima Kasih!")
    st.write("Sampai jumpa kembali!")
    st.markdown(
        """
        <meta http-equiv="refresh" content="0; url=https://syaninn.github.io/ninn/Terimakasih.html">
        """,
        unsafe_allow_html=True
    )