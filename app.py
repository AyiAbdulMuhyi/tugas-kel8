import streamlit as st
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus
import matplotlib.pyplot as plt
import math

# Judul aplikasi
st.set_page_config(page_title="Aplikasi Kelompok 6", layout="wide")
st.title("📊 Aplikasi Streamlit Kelompok 6")

# Membuat 3 tab
tab1, tab2, tab3, tab4 = st.tabs(["📁 Model Program Linear", "📈 Tab 2: Model Persediaan EOQ", "⚙️ Tab 3: Model Antrian M/M/1", "🌨️ Tab 4: Model Lainnya"])

with st.sidebar:
    st.header("Aplikasi Kelompok 6")
    st.write("""
    1. tes
    2. tess
    3. baa
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
   
    
    # Sidebar dengan dokumentasi
    with st.sidebar:
        st.title("🍦 Panduan Aplikasi")
        st.markdown("""
        *Aplikasi Model Matematika untuk Industri Es Krim*
        
        Aplikasi ini menyediakan berbagai model matematika yang berguna untuk pengambilan keputusan di pabrik es krim.
        
        *Tab-tab yang tersedia:*
        1. *Optimasi Produksi* - Menghitung kombinasi produksi optimal
        2. *Peramalan Permintaan* - Memprediksi permintaan es krim
        3. *Manajemen Inventori* - Menghitung EOQ untuk bahan baku
        4. *Analisis Break Even* - Menghitung titik impas produksi
        
        *Cara menggunakan:*
        - Pilih tab yang diinginkan
        - Masukkan parameter yang dibutuhkan
        - Lihat hasil analisis dan visualisasi
        """)
    
    # Data contoh untuk permintaan es krim
    @st.cache_data
    def load_sample_data():
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        demand = [1200, 1300, 1500, 1800, 2500, 3200, 
                  3500, 3400, 2800, 2000, 1500, 1300]
        return pd.DataFrame({'Bulan': months, 'Permintaan (kg)': demand})
    
    # Fungsi untuk tab Optimasi Produksi
    def production_optimization():
        st.header("Optimasi Produksi Es Krim")
        st.markdown("""
        Model ini membantu menentukan kombinasi produksi optimal untuk memaksimalkan keuntungan 
        dengan mempertimbangkan kapasitas produksi dan ketersediaan bahan baku.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parameter Produk")
            vanilla_price = st.number_input("Harga Es Krim Vanilla per kg ($)", 5.0, 20.0, 8.0)
            chocolate_price = st.number_input("Harga Es Krim Coklat per kg ($)", 5.0, 20.0, 10.0)
            vanilla_cost = st.number_input("Biaya Produksi Vanilla per kg ($)", 1.0, 10.0, 3.0)
            chocolate_cost = st.number_input("Biaya Produksi Coklat per kg ($)", 1.0, 10.0, 4.0)
        
        with col2:
            st.subheader("Kendala Produksi")
            milk = st.number_input("Susu tersedia per hari (kg)", 100, 2000, 500)
            sugar = st.number_input("Gula tersedia per hari (kg)", 50, 1000, 200)
            labor = st.number_input("Jam kerja tersedia per hari", 8, 24, 16)
        
        # Koefisien kebutuhan bahan per kg es krim
        vanilla_milk = 0.5
        chocolate_milk = 0.6
        vanilla_sugar = 0.2
        chocolate_sugar = 0.3
        vanilla_labor = 0.1
        chocolate_labor = 0.15
        
        # Fungsi tujuan untuk optimasi
        def profit(x):
            return -( (vanilla_price - vanilla_cost)*x[0] + (chocolate_price - chocolate_cost)*x[1] )
        
        # Kendala produksi
        constraints = [
            {'type': 'ineq', 'fun': lambda x: milk - (vanilla_milk*x[0] + chocolate_milk*x[1])},
            {'type': 'ineq', 'fun': lambda x: sugar - (vanilla_sugar*x[0] + chocolate_sugar*x[1])},
            {'type': 'ineq', 'fun': lambda x: labor - (vanilla_labor*x[0] + chocolate_labor*x[1])}
        ]
        
        # Batasan produksi
        bounds = [(0, None), (0, None)]
        
        # Solusi awal
        x0 = [100, 100]
        
        # Menyelesaikan optimasi
        solution = minimize(profit, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if solution.success:
            vanilla_opt = round(solution.x[0], 2)
            chocolate_opt = round(solution.x[1], 2)
            total_profit = round(-solution.fun, 2)
            
            st.success(f"Kombinasi produksi optimal: Vanilla {vanilla_opt} kg, Coklat {chocolate_opt} kg")
            st.success(f"Keuntungan maksimal per hari: ${total_profit}")
            
            # Visualisasi
            fig, ax = plt.subplots()
            products = ['Vanilla', 'Coklat']
            quantities = [vanilla_opt, chocolate_opt]
            ax.bar(products, quantities, color=['#FFD700', '#8B4513'])
            ax.set_ylabel('Jumlah Produksi (kg)')
            ax.set_title('Produksi Optimal Es Krim')
            st.pyplot(fig)
            
            # Tabel penggunaan sumber daya
            resources = pd.DataFrame({
                'Sumber Daya': ['Susu', 'Gula', 'Tenaga Kerja'],
                'Digunakan': [
                    f"{vanilla_milk*vanilla_opt + chocolate_milk*chocolate_opt:.1f} kg dari {milk} kg",
                    f"{vanilla_sugar*vanilla_opt + chocolate_sugar*chocolate_opt:.1f} kg dari {sugar} kg",
                    f"{vanilla_labor*vanilla_opt + chocolate_labor*chocolate_opt:.1f} jam dari {labor} jam"
                ]
            })
            st.table(resources)
        else:
            st.error("Tidak dapat menemukan solusi optimal dengan parameter saat ini.")
    
    # Fungsi untuk tab Peramalan Permintaan
    def demand_forecasting():
        st.header("Peramalan Permintaan Es Krim")
        st.markdown("""
        Model ini memprediksi permintaan es krim berdasarkan data historis dengan metode moving average.
        """)
        
        data = load_sample_data()
        
        st.subheader("Data Historis Permintaan")
        st.line_chart(data.set_index('Bulan')['Permintaan (kg)'])
        
        st.subheader("Parameter Peramalan")
        window_size = st.slider("Ukuran Window untuk Moving Average", 1, 6, 3)
        
        # Menghitung moving average
        data['Moving Average'] = data['Permintaan (kg)'].rolling(window=window_size).mean()
        
        # Visualisasi
        fig = px.line(data, x='Bulan', y=['Permintaan (kg)', 'Moving Average'],
                      title='Peramalan Permintaan dengan Moving Average')
        st.plotly_chart(fig, use_container_width=True)
        
        # Prediksi untuk bulan berikutnya
        last_months = data['Permintaan (kg)'].tail(window_size).values
        next_month_pred = np.mean(last_months)
        
        st.subheader("Hasil Prediksi")
        st.info(f"Prediksi permintaan untuk bulan berikutnya: {next_month_pred:.0f} kg")
        
        # Menghitung error
        if window_size < len(data):
            mae = np.mean(np.abs(data['Permintaan (kg)'][window_size:] - data['Moving Average'][window_size:]))
            st.info(f"Mean Absolute Error (MAE): {mae:.0f} kg")
    
    # Fungsi untuk tab Manajemen Inventori
    def inventory_management():
        st.header("Manajemen Inventori Bahan Baku")
        st.markdown("""
        Model Economic Order Quantity (EOQ) untuk menghitung jumlah pesanan optimal bahan baku 
        yang meminimalkan total biaya persediaan.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parameter Bahan Baku")
            demand = st.number_input("Permintaan tahunan (kg)", 1000, 100000, 10000, step=1000)
            order_cost = st.number_input("Biaya pesanan per order ($)", 10, 500, 50)
            holding_cost = st.number_input("Biaya penyimpanan per kg per tahun ($)", 0.1, 10.0, 1.0)
        
        with col2:
            st.subheader("Hasil Perhitungan EOQ")
            # Menghitung EOQ
            eoq = np.sqrt((2 * demand * order_cost) / holding_cost)
            optimal_orders = demand / eoq
            total_cost = (order_cost * demand / eoq) + (holding_cost * eoq / 2)
            
            st.metric("Jumlah Pesanan Optimal (EOQ)", f"{eoq:.1f} kg")
            st.metric("Frekuensi Pesanan per Tahun", f"{optimal_orders:.1f} kali")
            st.metric("Total Biaya Persediaan Tahunan", f"${total_cost:.2f}")
        
        # Visualisasi
        order_quantities = np.linspace(100, 2*eoq, 50)
        ordering_costs = (order_cost * demand) / order_quantities
        holding_costs = (holding_cost * order_quantities) / 2
        total_costs = ordering_costs + holding_costs
        
        fig, ax = plt.subplots()
        ax.plot(order_quantities, ordering_costs, label='Biaya Pesanan')
        ax.plot(order_quantities, holding_costs, label='Biaya Penyimpanan')
        ax.plot(order_quantities, total_costs, label='Total Biaya')
        ax.axvline(eoq, color='r', linestyle='--', label='EOQ')
        ax.set_xlabel('Jumlah Pesanan (kg)')
        ax.set_ylabel('Biaya ($)')
        ax.set_title('Model Economic Order Quantity')
        ax.legend()
        st.pyplot(fig)
    
    # Fungsi untuk tab Analisis Break Even
    def break_even_analysis():
        st.header("Analisis Break Even Produksi Es Krim")
        st.markdown("""
        Menghitung titik impas (break-even point) produksi es krim berdasarkan biaya tetap, 
        biaya variabel, dan harga jual.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parameter Biaya dan Harga")
            fixed_cost = st.number_input("Biaya Tetap per Bulan ($)", 1000, 100000, 10000)
            variable_cost = st.number_input("Biaya Variabel per kg ($)", 0.1, 10.0, 2.5)
            selling_price = st.number_input("Harga Jual per kg ($)", 1.0, 20.0, 5.0)
        
        with col2:
            st.subheader("Hasil Analisis")
            # Menghitung BEP
            contribution_margin = selling_price - variable_cost
            bep_units = fixed_cost / contribution_margin
            bep_sales = bep_units * selling_price
            
            st.metric("Titik Impas (Unit)", f"{bep_units:.1f} kg")
            st.metric("Titik Impas (Penjualan)", f"${bep_sales:.2f}")
        
        # Visualisasi
        units_range = np.linspace(0, 2*bep_units, 100)
        total_revenue = selling_price * units_range
        total_cost = fixed_cost + variable_cost * units_range
        
        fig, ax = plt.subplots()
        ax.plot(units_range, total_revenue, label='Pendapatan')
        ax.plot(units_range, total_cost, label='Total Biaya')
        ax.axvline(bep_units, color='r', linestyle='--', label='Titik Impas')
        ax.fill_between(units_range, total_cost, total_revenue, 
                       where=(total_revenue >= total_cost), 
                       color='green', alpha=0.3, label='Keuntungan')
        ax.fill_between(units_range, total_cost, total_revenue, 
                       where=(total_revenue < total_cost), 
                       color='red', alpha=0.3, label='Kerugian')
        ax.set_xlabel('Volume Produksi (kg)')
        ax.set_ylabel('Nilai ($)')
        ax.set_title('Analisis Break Even')
        ax.legend()
        st.pyplot(fig)
    
    # Membuat tab-tab utama
    tab1, tab2, tab3, tab4 = st.tabs([
        "Optimasi Produksi", 
        "Peramalan Permintaan", 
        "Manajemen Inventori", 
        "Analisis Break Even"
    ])
    
    with tab1:
        production_optimization()
    
    with tab2:
        demand_forecasting()
    
    with tab3:
        inventory_management()
    
    with tab4:
        break_even_analysis()
    
    # Catatan kaki
    st.markdown("---")
    st.caption("Aplikasi Model Matematika untuk Industri Es Krim © 2023 - Dibangun dengan Streamlit")
