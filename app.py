import streamlit as st

# Judul aplikasi
st.set_page_config(page_title="Aplikasi Tiga Tab", layout="wide")
st.title("📊 Aplikasi Streamlit dengan 3 Tab")

# Membuat 3 tab
tab1, tab2, tab3 = st.tabs(["📁 Tab 1: Data", "📈 Tab 2: Analisis", "⚙️ Tab 3: Pengaturan"])

# Isi Tab 1
with tab1:
    st.header("Tab 1: Data")
    st.write("Tampilkan data atau input form di sini.")
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])
    if uploaded_file is not None:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

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
