# BurnAway

## 👥 Tim CC26-PSU237

| Nama Anggota                     | Learning Path            | ID Cohort        |
| :------------------------------- | :----------------------- | :--------------- |
| Muhammad Fikri Rouzan Ash Shidik | Data Scientist           | `CDCC224D6Y0758` |
| Hafidz Surya Afifi               | Data Scientist           | `CDCC224D6Y2679` |
| Aulia Salsabila                  | Full-Stack Web Developer | `CFCC288D6X2031` |
| Muhammad Radhya Firaz Maynard    | Full-Stack Web Developer | `CFCC224D6Y2852` |
| Salwa Syaharani Putri            | AI Engineer              | `CACC224D6X0556` |
| Danuardi Saputro                 | AI Engineer              | `CACC224D6Y1221` |

---

## 📌 Deskripsi

Burnout diakui secara resmi oleh WHO (ICD-11) sebagai fenomena pekerjaan yang memengaruhi kesejahteraan psikologis, di mana 83% software developer dilaporkan mengalaminya akibat faktor beban kerja, pesatnya perkembangan teknologi, serta isolasi kerja (Haystack, 2021). Untuk meminimalkan penurunan performa dan menjaga kualitas perangkat lunak, proyek BurnAway mengembangkan sebuah dashboard analitik interaktif. Dashboard ini dirancang untuk memetakan dan menganalisis faktor pemicu stres pada developer, sehingga dapat memberikan wawasan berbasis data untuk menjaga kesehatan mental serta mendukung produktivitas kerja.

---

## 💾 Dataset

Dataset yang digunakan dalam proyek ini bersumber dari [Kaggle: Developer Burnout Prediction Dataset](https://www.kaggle.com/datasets/asifxzaman/developer-burnout-prediction-dataset7000-samples). Dataset ini menyajikan informasi mengenai faktor fisik dan perilaku kerja yang memengaruhi tingkat burnout pada developer. Di dalamnya mencakup 7.000 sampel data aktivitas harian yang memuat berbagai atribut seperti metrik beban kerja, pola istirahat, serta indikator produktivitas.

---

## 🛠️ Tech Stack

| Kategori                    | Teknologi yang Digunakan                                                             |
| :-------------------------- | :----------------------------------------------------------------------------------- |
| 🌐 **Programming Language** | `Python`                                                                             |
| 🌱 **Environment**          | `Jupyter Notebook`                                                                   |
| 🧩 **Framework**            | `Streamlit`                                                                          |
| ⚛️ **Libraries**            | `pandas`, `Matplotlib`, `seaborn`, `scikit-learn`, `statsmodels`, `Plotly`, `Pillow` |
| ⚡ **Tool**                 | `Google Colab`                                                                       |
| 🚀 **Deployment**           | `Streamlit Community Cloud`                                                          |

---

## ⚙️ Petunjuk Pengaturan

1. **Prasyarat**
   - Python 3.11 atau lebih baru.
   - Git terinstal di komputer.

2. **Clone Repositori**

```bash
git clone https://github.com/Fikri-Rouzan/burnaway.git
cd burnaway
```

3. **Buat Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. **Install Dependensi**

```bash
pip install -r requirements.txt
```

5. **Menjalankan Dashboard Streamlit**

```bash
streamlit run dashboard/dashboard.py
```
