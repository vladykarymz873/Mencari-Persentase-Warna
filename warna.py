import cv2
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Analisis Persentase Warna pada Gambar")

# Fungsi untuk memetakan warna hex ke nama umum
def map_color_name(hex_color):
    color_map = {
        "#ffffff": "Putih",
        "#000000": "Hitam",
        "#ff0000": "Merah",
        "#00ff00": "Hijau",
        "#0000ff": "Biru",
        "#ffff00": "Kuning",
        "#ff00ff": "Ungu",
        "#ffa500": "Orange"
    }
    return color_map.get(hex_color, "Lainnya")

# Fungsi untuk menampilkan diagram pie
def plot_pie_chart(colors, percentages):
    fig, ax = plt.subplots()
    ax.pie(percentages, labels=colors, autopct="%1.1f%%", startangle=90, colors=colors)
    ax.axis("equal")
    st.pyplot(fig)

# Upload gambar
uploaded_file = st.file_uploader("Upload gambar (format JPG atau PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Baca gambar
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Konversi ke ruang warna RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Hitung total piksel
    total_pixels = image_rgb.shape[0] * image_rgb.shape[1]
    
    # Flatten gambar menjadi array 2D (piksel, channel)
    pixels = image_rgb.reshape(-1, 3)
    
    # Hitung jumlah piksel untuk setiap warna
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    # Hitung persentase untuk setiap warna
    percentages = (counts / total_pixels) * 100
    
    # Konversi warna RGB ke hexadecimal
    hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in unique_colors]
    
    # Filter warna dengan persentase signifikan (> 0.5%)
    significant_colors = [(hex_color, percentage) for hex_color, percentage in zip(hex_colors, percentages) if percentage > 0.5]
    
    # Tampilkan gambar yang diunggah
    st.image(image_rgb, caption="Gambar yang diunggah", use_column_width=True)
    
    # Tampilkan hasil analisis
    st.subheader("Hasil Akhir: Persentase Warna")
    if significant_colors:
        color_names = []
        color_hexes = []
        color_percentages = []
        for hex_color, percentage in significant_colors:
            color_name = map_color_name(hex_color)
            color_names.append(color_name)
            color_hexes.append(hex_color)
            color_percentages.append(percentage)
            st.write(f"Warna: {hex_color} ({color_name}), Persentase: {percentage:.2f}%")
        
        # Tampilkan diagram pie
        st.subheader("Diagram Pie Persentase Warna")
        plot_pie_chart(color_hexes, color_percentages)
    else:
        st.write("Tidak ada warna dengan persentase signifikan.")
else:
    st.info("Silakan unggah gambar untuk memulai analisis.")
