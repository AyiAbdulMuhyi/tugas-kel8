import streamlit as st
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus
import matplotlib.pyplot as plt

# Judul aplikasi
st.set_page_config(page_title="Aplikasi Tiga Tab", layout="wide")
st.title("📊 Aplikasi Streamlit dengan 3 Tab")

# Membuat 3 tab
tab1, tab2, tab3 = st.tabs(["📁 Optimasi Produksi Pabrik Es Krim", "📈 Tab 2: Analisis", "⚙️ Tab 3: Pengaturan"])

# Isi Tab 1
with tab1:
    st.title("🍦 Optimasi Produksi Pabrik Es Krim (Linear Programming)")

    st.subheader("🧾 Input Data Produksi Es Krim")

    # Input dinamis untuk 3 jenis es krim
    jenis_es_krim = ['Cokelat', 'Vanila', 'Stroberi']
    data = {}

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**Jenis Es Krim**")
        for j in jenis_es_krim:
            st.text(j)

    with col2:
        st.markdown("**Bahan Baku (liter/unit)**")
        for j in jenis_es_krim:
            data[f"{j}_bahan"] = st.number_input(f"{j}", min_value=0.0, value=3.0 if j == "Cokelat" else (2.0 if j == "Vanila" else 4.0), key=f"bahan_{j}")

    with col3:
        st.markdown("**Jam Kerja (jam/unit)**")
        for j in jenis_es_krim:
            data[f"{j}_jam"] = st.number_input(f"{j}", min_value=0.0, value=2.0 if j == "Cokelat" else (1.5 if j == "Vanila" else 2.5), key=f"jam_{j}")

    with col4:
        st.markdown("**Keuntungan (Rp/unit)**")
        for j in jenis_es_krim:
            data[f"{j}_profit"] = st.number_input(f"{j}", min_value=0, value=3000 if j == "Cokelat" else (2500 if j == "Vanila" else 3500), key=f"profit_{j}")

    # Input batasan total sumber daya
    st.subheader("⚙️ Batasan Sumber Daya")
    max_bahan_baku = st.number_input("Kapasitas Total Bahan Baku (liter)", min_value=1.0, value=100.0)
    max_jam_kerja = st.number_input("Kapasitas Total Jam Kerja (jam)", min_value=1.0, value=80.0)

    # Mulai optimasi
    if st.button("🔍 Jalankan Optimasi"):
        # Buat model LP
        model = LpProblem("Optimasi_Produksi_Es_Krim", LpMaximize)

        # Variabel keputusan
        variables = {}
        for j in jenis_es_krim:
            variables[j] = LpVariable(j, lowBound=0, cat='Continuous')

        # Fungsi Tujuan
        model += lpSum([data[f"{j}_profit"] * variables[j] for j in jenis_es_krim]), "Total_Keuntungan"

        # Kendala bahan baku
        model += lpSum([data[f"{j}_bahan"] * variables[j] for j in jenis_es_krim]) <= max_bahan_baku, "Kapasitas_Bahan_Baku"

        # Kendala jam kerja
        model += lpSum([data[f"{j}_jam"] * variables[j] for j in jenis_es_krim]) <= max_jam_kerja, "Jam_Kerja"

        # Jalankan solver
        model.solve()

        # Tampilkan hasil
        st.subheader("📈 Hasil Optimasi Produksi:")

        if LpStatus[model.status] == 'Optimal':
            total = 0
            jumlah = []
            for j in jenis_es_krim:
                hasil = variables[j].varValue
                jumlah.append(hasil)
                st.write(f"Produksi Es Krim {j}: {hasil:.2f} unit")
                total += hasil * data[f"{j}_profit"]
            st.success(f"💰 Total Keuntungan: Rp {total:,.0f}")

            # Visualisasi
            fig, ax = plt.subplots()
            ax.bar(jenis_es_krim, jumlah, color=['brown', 'beige', 'pink'])
            ax.set_ylabel("Jumlah Produksi (unit)")
            ax.set_title("📊 Visualisasi Hasil Produksi Optimal")
            st.pyplot(fig)
        else:
            st.error("⚠️ Tidak ditemukan solusi optimal. Coba ubah parameter input.")


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
