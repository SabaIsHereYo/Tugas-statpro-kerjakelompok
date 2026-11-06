# 🎮 Steam Games & Player Analytics Dashboard (2021–2025)

**Mata Kuliah**: Statistika dan Probabilitas 1 B
**Topik**: Analisis Deskriptif Tren Rilis Game, Harga, dan Pemain Aktif Steam (2021 - 2025)
**Sumber Data**: [Kaggle - Steam Games Dataset 2021-2025](https://www.kaggle.com/datasets/jypenpen54534/steam-games-dataset-2021-2025-65k)

---

## 👥 Anggota Kelompok (Grup 2)

| No | No. Siswa |    NPM    | Nama Anggota              |
| :-: | :-------: | :--------: | :------------------------ |
| 1 |     4     | 4525210019 | Daffa Saba Al - Ghazali   |
| 2 |    31    | 4525210071 | Stevany Baetrix Salindeho |
| 3 |    47    | 4525210110 | Mochammad Jihan Isfalana  |
| 4 |    55    | 4525210128 | Arsanti Nur Indriani      |
| 5 |    41    | 4525210101 | Rayza Aqsha Aditya        |
| 6 |    40    | 4525210098 | Aulia Fachri              |
| 7 |    19    | 4525210051 | Muzaki Arifin             |

---

## 📌 Deskripsi Dataset

Dataset `rawday.csv` mencatat tren rilis game di Steam dari kurun waktu 2021 hingga 2025:

- `release_date`: Tanggal rilis game
- `release_year`: Tahun rilis (2021 - 2025)
- `game_name`: Judul game
- `developer`: Pengembang / Developer
- `genre`: Genre game
- `price_idr`: Harga game di Steam Indonesia (Rp)
- `peak_ccu`: Peak Concurrent Players (Jumlah pemain bersamaan tertinggi)
- `positive_rating_%`: Persentase ulasan positif (%)
- `total_reviews`: Total akumulasi ulasan pengguna

---

## ❓ Pertanyaan Analisis Statistika

1. **Bagaimana tren rata-rata pemain aktif harian (Peak CCU) pada rilis game dari tahun 2021 hingga 2025?**
2. **Genre game manakah yang mendominasi jumlah ulasan positif dan estimasi total pemain di Steam?**
3. **Bagaimana hubungan korelasi antara harga game (`price_idr`) dengan persentase ulasan positif (`positive_rating_%`)?**

---

## 🚀 Cara Menjalankan Dashboard

1. Aktifkan Virtual Environment dan install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
