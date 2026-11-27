"""
Sistem Penilaian Kualitas Susu dengan Logika Fuzzy Mamdani.
Diproses dari dataset milknew.csv (Kaggle Milk Quality).
"""

import sys
import os
import pandas as pd

# Tambahkan root path agar import fuzzy bisa jalan
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fuzzy import get_kualitas_susu


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "milknew.csv")
    if not os.path.exists(csv_path):
        print(f"Error: File tidak ditemukan di {csv_path}")
        return

    # ==============================
    # 1. BACA DATA & BERSIHKAN
    # ==============================
    df = pd.read_csv(csv_path)
    df.columns = [col.strip() for col in df.columns]
    df = df.rename(columns={"Grade": "grade"})

    # Hapus baris ganda
    u = df.drop_duplicates()
    print(f"Total baris asli     : {len(df)}")
    print(f"Total baris unik (u) : {len(u)}")

    # Split 70% latih, 30% uji (acuan prompt random_state=42)
    tr = u.groupby("grade").sample(frac=0.7, random_state=42)
    te = u[~u.index.isin(tr.index)].copy()

    print(f"Data latih (train)   : {len(tr)} baris")
    print(f"Data uji (test)      : {len(te)} baris")
    print("=" * 95)

    def evaluasi_satu_baris(row):
        res = get_kualitas_susu(
            pH=row["pH"],
            suhu=row["Temprature"],
            rasa=int(row["Taste"]),
            bau=int(row["Odor"]),
            lemak=int(row["Fat"]),
            kekeruhan=int(row["Turbidity"]),
        )
        return res

    # ==============================
    # 2. PERBANDINGAN JAWABAN SISTEM vs DATASET
    #    (Dengan kolom BENER / SALAH)
    # ==============================
    te["prediksi_sistem"] = [evaluasi_satu_baris(r)["kelas"] for _, r in te.iterrows()]
    te["skor_sistem"]     = [evaluasi_satu_baris(r)["skor"] for _, r in te.iterrows()]
    te["hasil_dataset"]   = [str(x).lower() for x in te["grade"]]
    te["status"]          = ["BENAR" if a == b else "SALAH" for a, b in zip(te["hasil_dataset"], te["prediksi_sistem"])]

    # Cetak Tabel Perbandingan
    print("\n[PERBANDINGAN: JAWABAN SISTEM vs HASIL DATASET]")
    print(f"{'No':<3} | {'pH':>5} | {'Suhu':>4} | {'Fisik(R/B/L/K)':<14} | {'Skor':>5} | {'Hasil Dataset':<14} | {'Jawaban Sistem':<14} | {'Status'}")
    print("-" * 95)

    for i, row in enumerate(te.itertuples(), start=1):
        fisik_str = f"{int(row.Taste)}/{int(row.Odor)}/{int(row.Fat)}/{int(row.Turbidity)}"
        print(
            f"{i:<3} | {row.pH:5.1f} | {int(row.Temprature):4d} | {fisik_str:<14} | "
            f"{row.skor_sistem:5.1f} | {row.grade.upper():<14} | {row.prediksi_sistem.upper():<14} | "
            f"{'[√] BENAR' if row.status == 'BENAR' else '[X] SALAH'}"
        )

    # ==============================
    # 3. RINGKASAN STATISTIK
    # ==============================
    tr_benar = 0
    tr = tr.copy()
    tr["prediksi_sistem"] = [evaluasi_satu_baris(r)["kelas"] for _, r in tr.iterrows()]
    tr_benar = (tr["prediksi_sistem"] == tr["grade"]).sum()
    
    te_benar = (te["status"] == "BENAR").sum()
    te_total = len(te)
    
    print("-" * 95)
    print(f"\n[HASIL EVALUASI AKHIR]")
    print(f"  Data Latih : {tr_benar}/{len(tr)} Benar   => Akurasi {(tr_benar/len(tr)*100):.2f}%")
    print(f"  Data Uji   : {te_benar}/{te_total} Benar => Akurasi {(te_benar/te_total*100):.2f}%")
    print(f"\n  Total Kasus SALAH : {te_total - te_benar} (semua dari data uji)")
    print("=" * 95)

    # Confusion matrix
    print("\n[CONFUSION MATRIX]")
    cm = pd.crosstab(te["grade"], te["prediksi_sistem"], margins=True)
    print(cm)

    # ==============================
    # 4. UJI KASUS ACUAN DARI MODUL
    # ==============================
    print("\n[UJI KASUS ACUAN DARI PANDUAN MODUL]")
    kasus_acuan = [
        {"pH": 6.6, "suhu": 37, "jumlah_bernai": 3, "skor": 80.6, "kelas": "high"},
        {"pH": 8.5, "suhu": 70, "jumlah_bernai": 4, "skor": 19.4, "kelas": "low"},
        {"pH": 6.6, "suhu": 37, "jumlah_bernai": 0, "skor": 50.0, "kelas": "medium"},
        {"pH": 6.3, "suhu": 37, "jumlah_bernai": 3, "skor": 50.0, "kelas": "medium"},
        {"pH": 6.6, "suhu": 47, "jumlah_bernai": 3, "skor": 55.4, "kelas": "medium"},
    ]

    for kas in kasus_acuan:
        total_1 = kas["jumlah_bernai"]
        r, b, l, k = (1 if total_1 >= 1 else 0,
                      1 if total_1 >= 2 else 0,
                      1 if total_1 >= 3 else 0,
                      1 if total_1 >= 4 else 0)
        res = get_kualitas_susu(pH=kas["pH"], suhu=kas["suhu"], rasa=r, bau=b, lemak=l, kekeruhan=k)
        print(
            f"  pH={kas['pH']:4.1f}, Suhu={kas['suhu']:2d}, 1s={kas['jumlah_bernai']} "
            f"| Skor: {res['skor']:5.2f} (acuan {kas['skor']:4.1f}) "
            f"| Kelas: {res['kelas']:6s} (acuan {kas['kelas']:6s}) "
            f"| Cocok: {'Ya' if res['kelas']==kas['kelas'] else 'Tidak'}"
        )

    print("\nSelesai. Evaluasi berjalan normal.")
    print(f"Jumlah data uji yang SALAH: {te_total - te_benar}")
    print(f"Jumlah data uji yang BENAR: {te_benar}")


if __name__ == "__main__":
    main()
