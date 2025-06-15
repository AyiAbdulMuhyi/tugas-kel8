import streamlit as st
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import matplotlib.pyplot as plt

# Judul aplikasi
st.set_page_config(page_title="Aplikasi Tiga Tab", layout="wide")
st.title("📊 Aplikasi Streamlit dengan 3 Tab")

# Membuat 3 tab
tab1, tab2, tab3 = st.tabs(["📁 Optimasi Produksi Pabrik Es Krim", "📈 Tab 2: Analisis", "⚙️ Tab 3: Pengaturan"])

# Isi Tab 1
with tab1:
    st.title("Optimasi Produksi Pabrik Es Krim (Linear Programming)")

    # Membuat model LP
    model = LpProblem("Optimasi_Produksi_Es_Krim", LpMaximize)

    # Variabel keputusan
    x = LpVariable("Cokelat", lowBound=0, cat='Continuous')
    y = LpVariable("Vanila", lowBound=0, cat='Continuous')
    z = LpVariable("Stroberi", lowBound=0, cat='Continuous')

    # Fungsi tujuan
    model += 3000*x + 2500*y + 3500*z, "Total_Keuntungan"

    # Kendala
    model += 3*x + 2*y + 4*z <= 100, "Kapasitas_Bahan_Baku"
    model += 2*x + 1.5*y + 2.5*z <= 80, "Jam_Kerja"

    # Menyelesaikan model
    model.solve()

    # Menampilkan hasil
    st.subheader("Hasil Optimasi Produksi:")
    st.write(f"Produksi Es Krim Cokelat: {x.varValue:.2f} unit")
    st.write(f"Produksi Es Krim Vanila : {y.varValue:.2f} unit")
    st.write(f"Produksi Es Krim Stroberi: {z.varValue:.2f} unit")
    st.write(f"Total Keuntungan: Rp {model.objective.value():,.0f}")

    # Visualisasi
    fig, ax = plt.subplots()
    jenis = ['Cokelat', 'Vanila', 'Stroberi']
    jumlah = [x.varValue, y.varValue, z.varValue]
    ax.bar(jenis, jumlah, color=['brown', 'beige', 'pink'])
    ax.set_ylabel("Jumlah Produksi (unit)")
    ax.set_title("Visualisasi Hasil Produksi Optimal")
    st.pyplot(fig)

# Isi Tab 2
with tab2:
    st.header("Tab 2: Analisis")
    st.write("Visualisasi atau hasil analisis ditampilkan di sini.")
    st.line_chart({"data": [1, 5, 2, 6, 8]})

# Isi Tab 3
with tab3:
    st.header("Tab 3: Pengaturan")
    st.write("Atur parameter atau preferensi di sini.")
    name = st.text_input("Masukkan nama Anda:")
    st.write(f"Nama yang dimasukkan: {name}")
