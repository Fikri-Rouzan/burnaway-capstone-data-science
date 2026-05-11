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

    # mapping label kategori beban kerja dan istirahat agar lebih informatif
    if "work_category" in df.columns:
        work_mapping = {
            0: "0 (Seimbang)",
            1: "1 (Cukup Tinggi)",
            2: "2 (Tinggi)",
            3: "3 (Sangat Tinggi)",
        }

        # Mapping angka ke teks
        df["work_category"] = df["work_category"].map(work_mapping)

        # Mengatur urutan kategori agar grafik konsisten
        category_order = [
            "0 (Seimbang)",
            "1 (Cukup Tinggi)",
            "2 (Tinggi)",
            "3 (Sangat Tinggi)",
        ]
        df["work_category"] = pd.Categorical(
            df["work_category"], categories=category_order, ordered=True
        )

    return df


df_clean = load_data()

# Sidebar setup
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/426/426833.png", width=150)
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

    # Filter interaktif untuk rentang usia
    min_age = int(df_clean["age"].min())
    max_age = int(df_clean["age"].max())

    age_range = st.slider(
        label="Pilih Rentang Usia (Tahun)",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
    )

    st.caption(
        "Dashboard ini dibuat untuk menganalisis faktor-faktor fisik dan mental yang memengaruhi tingkat burnout pada developer."
    )

# Memfilter dataset berdasarkan slider di sidebar
main_df = df_clean[
    (df_clean["experience_years"] >= exp_range[0])
    & (df_clean["experience_years"] <= exp_range[1])
    & (df_clean["age"] >= age_range[0])
    & (df_clean["age"] <= age_range[1])
]

# Header dan metrik
st.title("Dashboard Analisis Developer Burnout 🔥")
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

# Grafik bar
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

# Insight pertanyaan 1
with st.expander("Insight Pertanyaan 1"):
    st.markdown("""
    - Developer dengan burnout **High** memiliki rata-rata jam kerja dan waktu layar paling tinggi, serta waktu tidur paling rendah.
    - Developer dengan burnout **Low** menunjukkan kondisi sebaliknya yaitu jam kerja lebih rendah, waktu layar lebih kecil, dan waktu tidur lebih cukup.
    - Developer dengan burnout **Medium** berada di antara keduanya, menunjukkan pola yang konsisten.
    - Pola ini mengindikasikan bahwa peningkatan jam kerja dan waktu layar, serta penurunan waktu tidur, berkontribusi signifikan terhadap kenaikan tingkat burnout.
    """)

st.markdown("---")

# Visualisasi pertanyaan bisnis 2
st.subheader("Pertanyaan Bisnis 2")
st.write(
    "Bagaimana pengaruh keseimbangan antara jam kerja dan waktu tidur terhadap tingkat burnout pada developer?"
)

# Agregasi data
avg_work_burnout = (
    main_df.groupby("work_category", observed=False)["burnout_level"]
    .mean()
    .reset_index()
)
max_val2 = avg_work_burnout["burnout_level"].max()

# Pengaturan highlight warna
colors2 = [
    "#2ca02c" if val == max_val2 else "#98df8a"
    for val in avg_work_burnout["burnout_level"]
]

# Grafik bar
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

# Insight pertanyaan 2
with st.expander("Insight Pertanyaan 2"):
    st.markdown("""
    - Terdapat kenaikan yang konsisten pada rata-rata burnout seiring meningkatnya kategori beban kerja dan istirahat.
    - Kategori **Sangat Tinggi** memiliki burnout tertinggi, menunjukkan kondisi kerja jauh lebih dominan dibanding waktu istirahat.
    - Kategori **Seimbang** memiliki burnout paling rendah, menandakan keseimbangan kerja dan tidur mampu menekan resiko burnout.
    - Perbedaan antar kategori terlihat cukup signifikan, sehingga rasio kerja terhadap istirahat menjadi indikator kuat dalam memprediksi tingkat burnout developer.
    """)

st.markdown("---")

# Visualisasi pertanyaan bisnis 3
st.subheader("Pertanyaan Bisnis 3")
st.write("Bagaimana pengaruh tingkat stres terhadap tingkat burnout pada developer?")

# Agregasi data
avg_stress = (
    main_df.groupby("burnout_label", observed=False)["stress_level"]
    .mean()
    .reset_index()
)
max_val3 = avg_stress["stress_level"].max()

# Pengaturan highlight warna
colors3 = [
    "#d62728" if val == max_val3 else "#ff9896" for val in avg_stress["stress_level"]
]

# Grafik bar
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

# Insight pertanyaan 3
with st.expander("Insight Pertanyaan 3"):
    st.markdown("""
    - Rata-rata tingkat stres meningkat tajam dari kategori **Low** ke **Medium**, lalu ke **High**.
    - Developer dengan burnout **High** memiliki tingkat stres yang jauh lebih tinggi dibanding kategori lainnya.
    - Kenaikan ini menunjukkan pola yang sangat konsisten dan signifikan antar tingkat burnout.
    - Hal ini mengindikasikan bahwa tingkat stres merupakan faktor yang sangat kuat dan dominan dalam memengaruhi tingkat burnout developer.
    """)

# Visualisasi pertanyaan bisnis 4
st.subheader("Pertanyaan Bisnis 4")
st.write(
    "Apakah intensitas paparan layar yang tinggi relatif terhadap jam kerja secara signifikan meningkatkan resiko burnout yang lebih berat?"
)

# Agregasi data
avg_intensity = (
    main_df.groupby("burnout_label", observed=False)["screen_time_intensity"]
    .mean()
    .reset_index()
)
max_val4 = avg_intensity["screen_time_intensity"].max()

# Pengaturan highlight warna
colors4 = [
    "#6a51a3" if val == max_val4 else "#bcbddc"
    for val in avg_intensity["screen_time_intensity"]
]

# Grafik bar
fig4 = px.bar(
    avg_intensity,
    x="burnout_label",
    y="screen_time_intensity",
    text_auto=".2f",
    title="Pengaruh Intensitas Paparan Layar Terhadap Tingkat Burnout",
    labels={
        "burnout_label": "Level Burnout",
        "screen_time_intensity": "Rata-Rata Intensitas Waktu Layar",
    },
)

fig4.update_traces(marker_color=colors4)
st.plotly_chart(fig4, width="stretch")

# Insight pertanyaan 4
with st.expander("Insight Pertanyaan 4"):
    st.markdown("""
    - Developer dengan burnout **Low** memiliki rata-rata intensitas waktu layar paling tinggi dibandingkan kategori lainnya.
    - Developer dengan burnout **High** menunjukkan rata-rata intensitas paling rendah.
    - Penurunan angka intensitas pada tingkat burnout **High** menandakan bahwa kenaikan total jam kerja harian meningkat jauh lebih pesat daripada durasi penggunaan layar.
    - Hasil ini mengindikasikan bahwa beban jam kerja secara keseluruhan merupakan faktor pendorong burnout yang lebih kuat dibandingkan rasio penggunaan layar terhadap jam kerja.
    """)

st.markdown("---")

# Visualisasi pertanyaan bisnis 5
st.subheader("Pertanyaan Bisnis 5")
st.write(
    "Bagaimana hubungan antara efisiensi kerja dengan tingkat burnout developer? Apakah developer dengan efisiensi rendah cenderung mengalami burnout lebih tinggi?"
)

# Agregasi data
avg_efficiency = (
    main_df.groupby("burnout_label", observed=False)["commit_bug_ratio"]
    .mean()
    .reset_index()
)
max_val5 = avg_efficiency["commit_bug_ratio"].max()

# Pengaturan highlight warna
colors5 = [
    "#084594" if val == max_val5 else "#9ecae1"
    for val in avg_efficiency["commit_bug_ratio"]
]

# Grafik bar
fig5 = px.bar(
    avg_efficiency,
    x="burnout_label",
    y="commit_bug_ratio",
    text_auto=".2f",
    title="Hubungan Antara Efisiensi Produksi Dengan Tingkat Burnout",
    labels={
        "burnout_label": "Level Burnout",
        "commit_bug_ratio": "Rata-Rata Rasio Commit dan Bug",
    },
)

fig5.update_traces(marker_color=colors5)
st.plotly_chart(fig5, width="stretch")

# Insight pertanyaan 5
with st.expander("Insight Pertanyaan 5"):
    st.markdown("""
    - Developer dengan tingkat burnout **Low** memiliki rata-rata rasio commit terhadap bug paling tinggi.
    - Developer dengan tingkat burnout **High** mencatatkan skor efisiensi paling rendah.
    - Terjadi penurunan efisiensi kerja yang sangat signifikan dan konsisten seiring dengan meningkatnya level burnout dari **Low** ke **High**.
    - Data ini menunjukkan bahwa rendahnya efisiensi kerja yang diukur melalui rasio commit dan bug berkorelasi kuat dengan tingginya tingkat burnout pada developer.
    """)

st.markdown("---")

# Kesimpulan
st.subheader("Kesimpulan")

# Kesimpulan pertanyaan 1
with st.expander("Kesimpulan Pertanyaan 1"):
    st.info("""
    Berdasarkan hasil analisis, faktor jam kerja, waktu tidur, dan intensitas penggunaan layar memiliki pengaruh yang jelas terhadap tingkat burnout developer. 
    Burnout yang lebih tinggi cenderung terjadi pada developer dengan jam kerja dan waktu layar yang tinggi, serta waktu tidur yang lebih rendah. Sebaliknya, 
    developer dengan jam kerja lebih seimbang, waktu layar lebih rendah, dan waktu tidur yang cukup menunjukkan tingkat burnout yang lebih rendah. 
    Dengan demikian, kombinasi beban kerja berlebih dan kurangnya waktu istirahat menjadi faktor utama yang meningkatkan resiko burnout.
    """)

# Kesimpulan pertanyaan 2
with st.expander("Kesimpulan Pertanyaan 2"):
    st.info("""
    Hasil analisis menunjukkan bahwa keseimbangan antara jam kerja dan waktu tidur memiliki pengaruh yang signifikan terhadap tingkat burnout developer. 
    Semakin tidak seimbang rasio kerja terhadap istirahat, semakin tinggi tingkat burnout yang dialami. Developer dengan kondisi kerja yang jauh lebih 
    dominan dibanding waktu istirahat cenderung mengalami burnout yang lebih tinggi, sedangkan keseimbangan antara kerja dan tidur terbukti mampu menekan 
    resiko burnout. Dengan demikian, menjaga proporsi waktu kerja dan istirahat yang seimbang menjadi faktor penting dalam mengurangi burnout.
    """)

# Kesimpulan pertanyaan 3
with st.expander("Kesimpulan Pertanyaan 3"):
    st.info("""
    Berdasarkan hasil analisis, tingkat stres memiliki pengaruh yang sangat kuat terhadap tingkat burnout pada developer. Semakin tinggi 
    tingkat stres yang dialami, semakin tinggi pula tingkat burnout yang terjadi. Pola peningkatan yang konsisten dari kategori rendah 
    ke tinggi menunjukkan bahwa stres merupakan faktor utama yang mendorong terjadinya burnout. Oleh karena itu, pengelolaan stres 
    menjadi aspek penting yang perlu diperhatikan untuk mengurangi resiko burnout pada developer.
    """)

# Kesimpulan pertanyaan 4
with st.expander("Kesimpulan Pertanyaan 4"):
    st.info("""
    Berdasarkan hasil analisis, intensitas paparan layar relatif terhadap jam kerja bukan merupakan pendorong utama burnout yang lebih berat. 
    Developer dengan tingkat burnout tinggi memiliki nilai intensitas yang lebih rendah dikarenakan peningkatan total jam kerja harian yang 
    jauh lebih dominan dibandingkan durasi penggunaan layar itu sendiri. Hal ini menunjukkan bahwa volume beban kerja secara keseluruhan 
    memiliki pengaruh yang lebih signifikan terhadap resiko burnout dibandingkan dengan sekadar rasio intensitas waktu layar.
    """)

# Kesimpulan pertanyaan 5
with st.expander("Kesimpulan Pertanyaan 5"):
    st.info("""
    Hasil analisis menunjukkan bahwa efisiensi kerja memiliki hubungan yang sangat erat dan berbanding terbalik dengan tingkat burnout developer. 
    Penurunan rasio commit terhadap bug yang konsisten dari level rendah ke tinggi membuktikan bahwa tingkat burnout yang berat berdampak langsung 
    pada penurunan kualitas serta produktivitas hasil kerja. Dengan demikian, developer dengan efisiensi produksi yang rendah terbukti memiliki 
    resiko burnout yang lebih tinggi, menjadikan skor efisiensi sebagai indikator yang kuat untuk memantau kondisi kesehatan mental kerja developer.
    """)

st.markdown("---")

# Footer
st.caption("© 2026 Tim CC26-PSU237 - BurnAway Capstone Data Science")
