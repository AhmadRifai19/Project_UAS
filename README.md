## 1. Masalah yang Diselesaikan

Menilai kualitas susu secara manual atau dengan batas ambang tegas dapat menyebabkan bias pada sampel yang nilainya berada di perbatasan. Pendekatan fuzzy digunakan agar transisi penilaian menjadi halus dan toleran terhadap ketidakpastian kondisi lapangan.

---

## 2. Dataset

- **Nama Dataset:** Milk Quality Prediction
- **Sumber:** [Kaggle - Milk Quality Prediction](https://www.kaggle.com/datasets/cpluzshrijayan/milkquality)
- **Lisensi:** Open Data Commons Public Domain Dedication and License (PDDL) / CC0
- **Jumlah Data:** 1.059 baris asli, dengan **83 baris data unik** setelah penghapusan duplikasi.
- **Fitur yang Digunakan:**
  - `pH`: derajat keasaman susu (fuzzifikasi normal, trapezoid $(6.2, 6.4, 6.8, 7.0)$).
  - `Temprature`: suhu susu dalam °C (fuzzifikasi aman, trapezoid $(25, 34, 45, 50)$).

---

## 3. Metode Fuzzy Mamdani

Sistem menggunakan mesin inferensi Mamdani murni berbasis **NumPy** (tanpa pustaka `scikit-fuzzy`):

### A. Fungsi Keanggotaan Input
1. **pH Normal (Trapesium):** $(a=6.2, b=6.4, c=6.8, d=7.0)$
2. **Suhu Aman (Trapesium):** $(a=25, b=34, c=45, d=50)$
3. **Kondisi Baik (Tegas):** bernilai $1.0$ jika `Taste + Odor + Fat + Turbidity` $\ge 2$, selain itu $0.0$

### B. Fungsi Keanggotaan Output (Skor 0–100)
- **Low:** trapesium $(0, 0, 25, 50)$ — penuh di 0–25, turun ke 0 di 50.
- **Medium:** segitiga $(25, 50, 75)$.
- **High:** trapesium $(50, 75, 100, 100)$ — naik dari 50, penuh di 75–100.

### C. Basis Aturan Fuzzy (3 Aturan)
1. `IF pH TIDAK normal OR suhu TIDAK aman THEN low`
2. `IF pH normal AND suhu aman AND kondisi TIDAK baik THEN medium`
3. `IF pH normal AND suhu aman AND kondisi baik THEN high`

*Operator:* `AND` = MIN, `OR` = MAX, `NOT` = $1 - \mu$.  
*Implikasi:* MIN, *Agregasi:* MAX.  
*Defuzzifikasi:* **Centroid** pada 1.001 titik diskrit.

### D. Penentuan Kelas
- Skor $< 37.5 \rightarrow$ **Rendah**
- Skor $< 62.5 \rightarrow$ **Sedang**
- Selain itu $\rightarrow$ **Tinggi**

---

## 4. Hasil dan Evaluasi

Evaluasi dilakukan pada 83 data unik yang dibagi menjadi 70% data latih dan 30% data uji menggunakan `random_state=42`:

- **Data Latih (58 baris):** Akurasi **93.10%** (54/58)
- **Data Uji (25 baris):** Akurasi **80.00%** (20/25)

### Matriks Konfusi (Data Uji)

| Kelas Asli | Prediksi Tinggi | Prediksi Rendah | Prediksi Sedang | Total |
|---|:---:|:---:|:---:|:---:|
| **Tinggi** | 7 | 0 | 0 | 7 |
| **Rendah** | 1 | 7 | 0 | 8 |
| **Sedang** | 4 | 0 | 6 | 10 |

### Tabel Perbandingan: Jawaban Sistem vs Hasil Dataset
Seluruh 25 data uji dievaluasi dengan penanda **Benar** (emerald) dan **Salah** (rose) untuk setiap baris. Sistem menunjukkan 5 kasus salah (semua dari kelas *Sedang* yang terprediksi *Tinggi*), yang sesuai dengan keterbatasan metode fuzzy.

### Uji 5 Kasus Acuan Dosen
Seluruh 5 kasus acuan dari modul berhasil menghasilkan klasifikasi yang **100% cocok** dengan acuan dosen:

| # | pH | Suhu | Jumlah 1 | Skor Acuan | Kelas Acuan | Skor Sistem | Kelas Sistem | Validasi |
|---|----|------|----------|------------|-------------|-------------|--------------|----------|
| 1 | 6.6 | 37 | 3 | 80.6 | Tinggi | 80.53 | Tinggi | ✓ Cocok |
| 2 | 8.5 | 70 | 4 | 19.4 | Rendah | 19.47 | Rendah | ✓ Cocok |
| 3 | 6.6 | 37 | 0 | 50.0 | Sedang | 50.00 | Sedang | ✓ Cocok |
| 4 | 6.3 | 37 | 3 | 50.0 | Sedang | 50.00 | Sedang | ✓ Cocok |
| 5 | 6.6 | 47 | 3 | 55.4 | Sedang | 55.38 | Sedang | ✓ Cocok |

---

## 5. Antarmuka Pengguna (UI Modern)

Antarmuka aplikasi dirancang dengan gaya modern menggunakan **Tailwind CSS** dengan desain kartu, gradien warna, bayangan lembut, dan animasi transisi yang halus:

- **Halaman Beranda:** Hero section, kartu statistik (dataset, aturan fuzzy, akurasi uji & latih), diagram alur kerja fuzzy, dan tabel 5 kasus acuan dosen.
- **Halaman Uji Susu:** Form interaktif untuk input pH, suhu, dan 4 indikator fisik biner (rasa, bau, lemak, kekeruhan) dengan styling input modern.
- **Halaman Hasil:** Menampilkan skor fuzzy, klasifikasi kualitas (Tinggi/Sedang/Rendah), derajat keanggotaan input, kekuatan aturan (α), dan daftar aturan aktif.
- **Halaman Riwayat:** Rekapitulasi seluruh pengujian yang tersimpan di database (12 data sampel awal tersedia), lengkap dengan kartu statistik (Total, Tinggi, Sedang, Rendah) dan tombol aksi detail.
- **Halaman Evaluasi:** Tabel perbandingan 25 data uji (jawaban sistem vs label dataset dengan penanda Benar/Salah), matriks konfusi, dan uji 5 kasus acuan.

---

## 6. Cara Menjalankan

```bash
# 1. Masuk ke direktori proyek
cd "/home/ahmad/semester 3/Sistem Cerdas/Project_UAS"

# 2. Aktifkan virtual environment
source .venv/bin/activate

# 3. Instal dependensi
pip install -r requirements.txt

# 4. Jalankan migrasi database
python manage.py migrate

# 5. Jalankan server lokal
python manage.py runserver
```

Buka browser dan akses: `http://localhost:8000`

Untuk menjalankan evaluasi data via skrip terminal:
```bash
python evaluate.py
```

---

## 7. Keterbatasan Sistem

1. **Jumlah Sampel Terbatas:** Hanya terdapat 83 baris data unik, dan data uji berjumlah 25 baris.
2. **Potensi Optimistis:** Batas parameter trapesium pH dan suhu ditentukan setelah mengamati sebaran data keseluruhan.
3. **Pola Kesalahan:** Kesalahan prediksi terbanyak terjadi pada kelas *Sedang* yang terprediksi sebagai *Tinggi*.
4. **Variabel yang Diabaikan:** Variabel warna (`Colour`) tidak dilibatkan dalam aturan inferensi.
5. **Konteks Medis/Pangan:** Sistem ini merupakan simulasi inferensi cerdas dan **bukan pengganti uji laboratorium mikrobiologi**.
6. **Ketergantungan CDN:** Tampilan antarmuka Tailwind CSS membutuhkan koneksi internet untuk memuat file CSS.

---

## 8. Refleksi

- **Kelebihan:** Sistem fuzzy Mamdani yang dibangun menggunakan NumPy sangat transparan, sehingga setiap tahapan (fuzzifikasi, implikasi, hingga defuzzifikasi) dapat dilacak dan dijelaskan secara matematis saat pengujian.
- **Rencana Pengembangan:** Memperluas fungsi keanggotaan variabel sensorik (rasa, bau, kekeruhan) menjadi himpunan fuzzy bertingkat, bukan sekadar biner tegas.