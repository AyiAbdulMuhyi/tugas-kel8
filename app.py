import streamlit as st
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus
import matplotlib.pyplot as plt
# Judul aplikasi
st.set_page_config(page_title="Aplikasi Kelompok 8", layout="wide")
st.title("📊 Aplikasi Streamlit Kelompok 8")

# Membuat 3 tab
tab1, tab2, tab3, tab4 = st.tabs(["📁 Model Program Linear", "📈 Tab 2: Model Persediaan EOQ", "⚙️ Tab 3: Model Antrian M/M/1", "🌨️ Tab 4: Model Lainnya"])

with st.sidebar:
        st.title("🍦 Panduan Aplikasi")
        st.markdown("""
        *Aplikasi Model Matematika untuk Industri Es Krim*
        
        Aplikasi ini menyediakan berbagai model matematika yang berguna untuk pengambilan keputusan di pabrik es krim.
        
        *Tab-tab yang tersedia:*
        1. *Program Linear* - Menghitung kombinasi produksi optimal
        2. *Persediaan EOQ* - Memprediksi permintaan es krim
        3. *Model Antrian M/M/1* - Menghitung EOQ untuk bahan baku
        4. *Model Lainnya* - Menghitung titik impas produksi
        
        *Cara menggunakan:*
        - Pilih tab yang diinginkan
        - Masukkan parameter yang dibutuhkan
        - Lihat hasil analisis dan visualisasi
        """)

# Isi Tab 1
with tab1:
    st.header("🍦 Optimasi Produksi Pabrik Es Krim (Linear Programming)")

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
    st.header("Model Persediaan EOQ - Pabrik Es Krim")
    # Input dari user
    D = st.number_input("Permintaan Tahunan (liter)", value=12000)
    S = st.number_input("Biaya Pemesanan per Order (Rp)", value=200000)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=500)

    # Perhitungan EOQ
    EOQ = math.sqrt((2 * D * S) / H)
    st.subheader("Hasil Perhitungan:")
    st.write(f"EOQ (Jumlah Optimal Pemesanan): {EOQ:.2f} liter")

    # Biaya total
    jumlah_pesan = D / EOQ
    total_biaya = jumlah_pesan * S + (EOQ / 2) * H
    st.write(f"Jumlah Pesanan per Tahun: {jumlah_pesan:.2f} kali")
    st.write(f"Total Biaya Persediaan: Rp {total_biaya:,.0f}")

    # Visualisasi
    q_values = list(range(int(EOQ/2), int(EOQ*2)))
    total_costs = [(D/q)*S + (q/2)*H for q in q_values]

    fig, ax = plt.subplots()
    ax.plot(q_values, total_costs, label='Total Biaya')
    ax.axvline(x=EOQ, color='r', linestyle='--', label='EOQ')
    ax.set_xlabel("Jumlah Pemesanan (Q)")
    ax.set_ylabel("Total Biaya Persediaan (Rp)")
    ax.set_title("Kurva Total Biaya vs Jumlah Pemesanan")
    ax.legend()
    st.pyplot(fig)

# Isi Tab 3
with tab3:
    st.header("Tab 3: Parkiran")
    
    def mm1_queue(lambda_rate, mu_rate):
        if lambda_rate >= mu_rate:
            return {
                "error": "Sistem tidak stabil. Pastikan λ < μ"
            }
    
        rho = lambda_rate / mu_rate
        L = rho / (1 - rho)          # Rata-rata jumlah pelanggan di sistem
        Lq = rho**2 / (1 - rho)      # Rata-rata jumlah pelanggan dalam antrean
        W = 1 / (mu_rate - lambda_rate)  # Rata-rata waktu di sistem
        Wq = rho / (mu_rate - lambda_rate)  # Rata-rata waktu dalam antrean
    
        return {
            "rho": rho,
            "L": L,
            "Lq": Lq,
            "W": W,
            "Wq": Wq,
        }
    
    # Judul aplikasi
    st.title("Simulasi Model Antrian M/M/1")
    
    # Input dari user
    lambda_rate = st.number_input("Masukkan laju kedatangan (λ):", min_value=0.01, step=0.1, format="%.2f")
    mu_rate = st.number_input("Masukkan laju pelayanan (μ):", min_value=0.01, step=0.1, format="%.2f")
    
    if st.button("Hitung"):
        result = mm1_queue(lambda_rate, mu_rate)
        
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Hasil Perhitungan:")
            st.write(f"**Utilisasi Sistem (ρ)**: {result['rho']:.2f}")
            st.write(f"**Rata-rata jumlah pelanggan di sistem (L)**: {result['L']:.2f}")
            st.write(f"**Rata-rata jumlah pelanggan dalam antrean (Lq)**: {result['Lq']:.2f}")
            st.write(f"**Rata-rata waktu dalam sistem (W)**: {result['W']:.2f} satuan waktu")
            st.write(f"**Rata-rata waktu dalam antrean (Wq)**: {result['Wq']:.2f} satuan waktu")
with tab4:
        st.header("📊 Prediksi Permintaan Es Krim Musiman (Regresi Linier)")
        months = np.arange(1, 13)
        demand = np.array([500, 520, 600, 800, 900, 1000, 950, 850, 700, 600, 550, 500])
        coeffs = np.polyfit(months, demand, 1)
        trend = np.poly1d(coeffs)
        st.subheader("📌 Model Regresi Linier:")
        st.latex(f"D(x) = {coeffs[0]:.2f}x + {coeffs[1]:.2f}")
        fig4, ax4 = plt.subplots()
        ax4.scatter(months, demand, label="Data Aktual")
        ax4.plot(months, trend(months), color='red', label="Trend Regresi")
        ax4.set_xlabel("Bulan")
        ax4.set_ylabel("Permintaan")
        ax4.set_title("Prediksi Permintaan Es Krim")
        ax4.legend()
        st.pyplot(fig4)
