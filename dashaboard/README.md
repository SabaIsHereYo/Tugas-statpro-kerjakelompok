
# 🎮 Steam Games & Player Analytics Dashboard (2021–2026)

**Mata Kuliah**: Statistika dan Probabilitas 1
**Topik**: Analisis Deskriptif Tren Rilis Game, Harga, dan Pemain Aktif Steam (2021 - 2026)
**Sumber Data**: Kaggle (Steam Games & Player Count Dataset Updated 2026)
**Jadwal Presentasi**: Jumat, 13 November 2026

---

## 📌 Deskripsi Dataset

Dataset ini mencatat tren rilis game di Steam dari kurun waktu 2021 hingga 2026:

- `release_date`: Tanggal rilis game
- `release_year`: Tahun rilis (2021 - 2026)
- `game_name`: Judul game
- `developer`: Pengembang / Developer
- `genre`: Genre game
- `price_idr`: Harga game di Steam Indonesia (Rp)
- `peak_ccu`: Peak Concurrent Players (Jumlah pemain bersamaan tertinggi)
- `positive_rating_%`: Persentase ulasan positif (%)
- `total_reviews`: Total akumulasi ulasan pengguna

---

## ❓ Pertanyaan Analisis Statistika (Langkah 1)

1. **Bagaimana tren rata-rata pemain aktif harian (Peak CCU) pada rilis game dari tahun 2021 hingga 2026?**
2. **Genre game manakah yang mendominasi jumlah ulasan positif dan estimasi total pemain di Steam?**
3. **Bagaimana hubungan korelasi antara harga game (`price_idr`) dengan persentase ulasan positif (`positive_rating_%`)?**

---

## 🚀 Cara Menjalankan Dashboard

1. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
