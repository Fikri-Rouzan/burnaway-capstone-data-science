import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman dashboard
st.set_page_config(page_title="BurnAway Dashboard", page_icon="🔥", layout="wide")


# load Data
@st.cache_data
def load_data():
    # Load dataset
    df = pd.read_csv("data/burnout_main_data.csv")

    # mapping label burnout agar lebih informatif
    if "burnout_level" in df.columns:
        mapping = {0: "0 (Low)", 1: "1 (Medium)", 2: "2 (High)"}
        # Jika tipe data integer atau float, map ke string
        if df["burnout_level"].dtype in ["int64", "float64"]:
            df["burnout_label"] = df["burnout_level"].map(mapping)
        else:
            df["burnout_label"] = df["burnout_level"]

    return df


df_clean = load_data()

# Sidebar setup
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3254/3254107.png", width=150)
    st.title("BurnAway Data")

    # Filter interaktif untuk rentang pengalaman
    min_exp = float(df_clean["experience_years"].min())
    max_exp = float(df_clean["experience_years"].max())

    exp_range = st.slider(
        label="Pilih Rentang Pengalaman (Tahun)",
        min_value=min_exp,
        max_value=max_exp,
        value=(min_exp, max_exp),
    )

    st.caption(
        "Dashboard ini dibuat untuk menganalisis faktor-faktor fisik dan mental yang memengaruhi tingkat burnout pada developer."
    )

# Memfilter dataset berdasarkan slider di sidebar
main_df = df_clean[
    (df_clean["experience_years"] >= exp_range[0])
    & (df_clean["experience_years"] <= exp_range[1])
]

# Header dan metrik
st.title("Dashboard Analisis Burnout Developer 🔥")
st.markdown(
    "Menampilkan insight dan visualisasi interaktif terkait faktor penyebab burnout."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Developer", value=f"{len(main_df):,}")
with col2:
    avg_stress = round(main_df["stress_level"].mean(), 1)
    st.metric("Rata-Rata Tingkat Stres", value=f"{avg_stress}")
with col3:
    high_burnout = len(main_df[main_df["burnout_label"] == "2 (High)"])
    st.metric("Developer Dengan Burnout High", value=f"{high_burnout:,}")

st.markdown("---")

# Visualisasi pertanyaan bisnis 1
st.subheader("Pertanyaan Bisnis 1")
st.write(
    "Bagaimana pengaruh faktor jam kerja, waktu tidur, dan intensitas penggunaan layar terhadap tingkat burnout pada developer?"
)

# agregasi dan transformasi
eda_plot = (
    main_df.groupby("burnout_label")[["daily_work_hours", "sleep_hours", "screen_time"]]
    .mean()
    .reset_index()
)
eda_melted = eda_plot.melt(
    id_vars="burnout_label", var_name="Faktor", value_name="Rata-rata"
)

# Mapping nama faktor agar lebih informatif
faktor_map = {
    "daily_work_hours": "Daily Work Hours",
    "sleep_hours": "Sleep Hours",
    "screen_time": "Screen Time",
}
eda_melted["Faktor"] = eda_melted["Faktor"].map(faktor_map)

fig1 = px.bar(
    eda_melted,
    x="Faktor",
    y="Rata-rata",
    color="burnout_label",
    barmode="group",
    text_auto=".2f",
    title="Perbandingan Pengaruh Faktor Fisik Terhadap Tingkat Burnout",
    labels={
        "Faktor": "Faktor Fisik",
        "Rata-rata": "Rata-Rata Jam",
        "burnout_label": "Level Burnout",
    },
    color_discrete_sequence=px.colors.sequential.Blues_r,
)

fig1.update_layout(
    legend=dict(
        title="Level Burnout",
        orientation="h",
        yanchor="top",
        y=-0.3,
        xanchor="center",
        x=0.5,
    )
)
st.plotly_chart(fig1, width="stretch")

with st.expander("Lihat Insight Pertanyaan 1"):
    st.markdown("""
    - Developer dengan burnout **High** memiliki jam kerja dan screen time paling tinggi, serta waktu tidur paling rendah.
    - Developer dengan burnout **Low** memiliki jam kerja lebih rendah, screen time lebih kecil, dan waktu tidur lebih cukup.
    - Peningkatan jam kerja dan screen time, serta kurang tidur, berkontribusi terhadap kenaikan burnout.
    """)

st.markdown("---")

# Visualisasi pertanyaan bisnis 2
st.subheader("Pertanyaan Bisnis 2")
st.write(
    "Bagaimana pengaruh keseimbangan antara jam kerja dan waktu tidur terhadap tingkat burnout pada developer?"
)

# Agregasi Data
avg_work_burnout = (
    main_df.groupby("work_category", observed=False)["burnout_level"]
    .mean()
    .reset_index()
)
max_val2 = avg_work_burnout["burnout_level"].max()

# Pengaturan Highlight Warna
colors2 = [
    "#2ca02c" if val == max_val2 else "#98df8a"
    for val in avg_work_burnout["burnout_level"]
]

fig2 = px.bar(
    avg_work_burnout,
    x="work_category",
    y="burnout_level",
    text_auto=".2f",
    title="Pengaruh Rasio Beban Kerja dan Istirahat Terhadap Tingkat Burnout",
    labels={
        "work_category": "Kategori Beban Kerja dan Istirahat",
        "burnout_level": "Rata-Rata Level Burnout",
    },
)

fig2.update_traces(marker_color=colors2)
st.plotly_chart(fig2, width="stretch")

with st.expander("Lihat Insight Pertanyaan 2"):
    st.markdown("""
    - Terdapat kenaikan yang konsisten pada rata-rata burnout seiring meningkatnya kategori beban kerja dan istirahat.
    - Kategori **Sangat Tinggi** memiliki burnout tertinggi, menunjukkan kondisi kerja jauh lebih dominan dibanding waktu istirahat.
    - Kategori **Seimbang** memiliki burnout paling rendah, menandakan keseimbangan kerja dan tidur mampu menekan risiko burnout.
    - Rasio kerja terhadap istirahat menjadi indikator kuat dalam memprediksi tingkat burnout developer.
    """)

st.markdown("---")

# Visualisasi pertanyaan bisnis 3
st.subheader("Pertanyaan Bisnis 3")
st.write("Bagaimana pengaruh tingkat stres terhadap tingkat burnout pada developer?")

# Agregasi Data
avg_stress = (
    main_df.groupby("burnout_label", observed=False)["stress_level"]
    .mean()
    .reset_index()
)
max_val3 = avg_stress["stress_level"].max()

# Pengaturan Highlight Warna
colors3 = [
    "#d62728" if val == max_val3 else "#ff9896" for val in avg_stress["stress_level"]
]

fig3 = px.bar(
    avg_stress,
    x="burnout_label",
    y="stress_level",
    text_auto=".2f",
    title="Pengaruh Tingkat Stres Terhadap Tingkat Burnout",
    labels={"burnout_label": "Level Burnout", "stress_level": "Rata-Rata Level Stres"},
)

fig3.update_traces(marker_color=colors3)
st.plotly_chart(fig3, width="stretch")

with st.expander("Lihat Insight Pertanyaan 3"):
    st.markdown("""
    - Rata-rata tingkat stres meningkat tajam dari kategori **Low** ke **Medium**, lalu ke **High**.
    - Developer dengan burnout **High** memiliki tingkat stres paling tinggi dibanding kategori lainnya.
    - Pola peningkatan terlihat sangat konsisten pada setiap level burnout.
    - Tingkat stres menjadi faktor psikologis yang sangat kuat dalam memengaruhi burnout developer.
    """)

st.markdown("---")
st.caption("© 2026 Tim CC26-PSU237 - BurnAway Capstone Data Science")
