import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# Load dataset
df_clean = pd.read_csv("data/burnout_main_data.csv")

st.title("BurnAway Dashboard")

st.header("Pertanyaan Bisnis 1")
st.write("""
Bagaimana pengaruh faktor jam kerja, waktu tidur, dan intensitas penggunaan layar terhadap tingkat burnout pada developer?
""")

# Agregasi data
eda_plot = df_clean.groupby("burnout_level")[[
    "daily_work_hours",
    "sleep_hours",
    "screen_time"
]].mean().reset_index()

# Transformasi data
eda_melted = eda_plot.melt(
    id_vars="burnout_level",
    var_name="Faktor",
    value_name="Rata-rata"
)

# Warna
palette_base = sns.color_palette("Blues", 6)
colors = {
    0: palette_base[1],
    1: palette_base[3],
    2: palette_base[5]
}

# Figure
fig, ax = plt.subplots(figsize=(12, 7))

sns.barplot(
    data=eda_melted,
    x="Faktor",
    y="Rata-rata",
    hue="burnout_level",
    palette=colors,
    errorbar=None,
    ax=ax
)

max_val = eda_melted["Rata-rata"].max()

ax.set_ylim(0, max_val * 1.2)
ax.set_title(
    "Perbandingan Pengaruh Faktor Fisik Terhadap Tingkat Burnout",
    fontsize=14,
    fontweight='bold',
    pad=20
)

ax.set_ylabel("Rata-Rata Jam")
ax.set_xlabel("Faktor Fisik")

ax.set_xticks([0, 1, 2])
ax.set_xticklabels([
    "Daily Work Hours",
    "Sleep Hours",
    "Screen Time"
])

# Legend
low_patch = mpatches.Patch(color=colors[0], label='0 (Low)')
med_patch = mpatches.Patch(color=colors[1], label='1 (Medium)')
high_patch = mpatches.Patch(color=colors[2], label='2 (High)')

ax.legend(
    handles=[low_patch, med_patch, high_patch],
    title="Level Burnout",
    loc='upper left'
)

# Label angka
for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(
            format(p.get_height(), '.2f'),
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='center',
            xytext=(0, 12),
            textcoords='offset points',
            fontweight='bold'
        )

st.pyplot(fig)

# Insight
st.subheader("Insight")
st.markdown("""
- Developer dengan burnout **High** memiliki jam kerja dan screen time paling tinggi, serta waktu tidur paling rendah.
- Developer dengan burnout **Low** memiliki jam kerja lebih rendah, screen time lebih kecil, dan waktu tidur lebih cukup.
- Peningkatan jam kerja dan screen time, serta kurang tidur, berkontribusi terhadap kenaikan burnout.
""")

st.header("Pertanyaan Bisnis 2")

st.write("""
Bagaimana pengaruh keseimbangan antara jam kerja dan waktu tidur terhadap tingkat burnout pada developer?
""")

# Agregasi data
avg_work_burnout = df_clean.groupby(
    'work_category',
    observed=False
)['burnout_level'].mean()

max_val = avg_work_burnout.max()

# Skema warna
palette_base = sns.color_palette("Greens", 6)
base_color = palette_base[1]
highlight_color = palette_base[4]

colors = [
    highlight_color if i == avg_work_burnout.idxmax()
    else base_color
    for i in avg_work_burnout.index
]

# Visualisasi
fig2, ax2 = plt.subplots(figsize=(10, 6))

sns.barplot(
    x=avg_work_burnout.index,
    y=avg_work_burnout.values,
    palette=colors,
    hue=avg_work_burnout.index,
    legend=False,
    errorbar=None,
    ax=ax2
)

ax2.set_xticks(range(len(avg_work_burnout.index)))
ax2.set_xticklabels([
    'Seimbang',
    'Cukup Tinggi',
    'Tinggi',
    'Sangat Tinggi'
], fontsize=11)

ax2.set_ylim(0, max_val * 1.2)

ax2.set_title(
    'Pengaruh Rasio Beban Kerja dan Istirahat Terhadap Tingkat Burnout',
    fontsize=14,
    fontweight='bold',
    pad=20
)

ax2.set_xlabel(
    'Kategori Beban Kerja dan Istirahat',
    fontsize=12
)

ax2.set_ylabel(
    'Rata-Rata Level Burnout',
    fontsize=12
)

# Label angka
for p in ax2.patches:
    ax2.annotate(
        format(p.get_height(), '.2f'),
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 12),
        textcoords='offset points',
        fontweight='bold'
    )

plt.tight_layout()

st.pyplot(fig2)

# Insight
st.subheader("Insight")

st.markdown("""
- Terdapat kenaikan yang konsisten pada rata-rata burnout seiring meningkatnya kategori beban kerja dan istirahat.
- Kategori **Sangat Tinggi** memiliki burnout tertinggi, menunjukkan kondisi kerja jauh lebih dominan dibanding waktu istirahat.
- Kategori **Seimbang** memiliki burnout paling rendah, menandakan keseimbangan kerja dan tidur mampu menekan risiko burnout.
- Rasio kerja terhadap istirahat menjadi indikator kuat dalam memprediksi tingkat burnout developer.
""")

st.header("Pertanyaan Bisnis 3")

st.write("""
Bagaimana pengaruh tingkat stres terhadap tingkat burnout pada developer?
""")

# Agregasi data
avg_stress = df_clean.groupby(
    'burnout_level',
    observed=False
)['stress_level'].mean()

max_val = avg_stress.max()

# Skema warna
palette_base = sns.color_palette("Reds", 6)
base_color = palette_base[1]
highlight_color = palette_base[4]

colors = [
    highlight_color if i == avg_stress.idxmax()
    else base_color
    for i in avg_stress.index
]

# Visualisasi
fig3, ax3 = plt.subplots(figsize=(10, 6))

sns.barplot(
    x=avg_stress.index,
    y=avg_stress.values,
    palette=colors,
    hue=avg_stress.index,
    legend=False,
    errorbar=None,
    ax=ax3
)

ax3.set_xticks(range(len(avg_stress.index)))
ax3.set_xticklabels([
    'Low',
    'Medium',
    'High'
], fontsize=11)

ax3.set_ylim(0, max_val * 1.2)

ax3.set_title(
    'Pengaruh Tingkat Stres Terhadap Tingkat Burnout',
    fontsize=14,
    fontweight='bold',
    pad=20
)

ax3.set_xlabel(
    'Level Burnout',
    fontsize=12
)

ax3.set_ylabel(
    'Rata-Rata Level Stres',
    fontsize=12
)

# Label angka
for p in ax3.patches:
    ax3.annotate(
        format(p.get_height(), '.2f'),
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 12),
        textcoords='offset points',
        fontweight='bold'
    )

plt.tight_layout()

st.pyplot(fig3)

# Insight
st.subheader("Insight")

st.markdown("""
- Rata-rata tingkat stres meningkat tajam dari kategori **Low** ke **Medium**, lalu ke **High**.
- Developer dengan burnout **High** memiliki tingkat stres paling tinggi dibanding kategori lainnya.
- Pola peningkatan terlihat sangat konsisten pada setiap level burnout.
- Tingkat stres menjadi faktor psikologis yang sangat kuat dalam memengaruhi burnout developer.
""")