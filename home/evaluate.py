"""
Modul evaluasi: membaca dataset, menghitung akurasi latih & uji,
membuat confusion matrix, dan tabel perbandingan prediksi sistem vs hasil dataset.
"""

import os
import sys
import pandas as pd
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Tambahkan root folder project agar import `fuzzy` berjalan di luar Django
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fuzzy import get_kualitas_susu


def get_base_dir():
    """
    Mengambil BASE_DIR dari Django jika sudah terkonfigurasi.
    Jika modul ini dipanggil secara langsung (misal saat development
    dari luar Django), fallback ke parent folder dari modul ini.
    """
    try:
        return settings.BASE_DIR
    except ImproperlyConfigured:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_data():
    """Membaca dataset dan menghapus duplikat"""
    csv_path = os.path.join(get_base_dir(), "data", "milknew.csv")
    if not os.path.exists(csv_path):
        return None

    df = pd.read_csv(csv_path)
    # Bersihkan spasi di nama kolom (seperti 'Fat ')
    df.columns = [col.strip() for col in df.columns]
    df = df.rename(columns={'Grade': 'grade'})

    # Hapus baris duplikat
    df = df.drop_duplicates()
    return df


def evaluate_single_row(row):
    """Menjalankan fuzzy engine pada satu baris data"""
    res = get_kualitas_susu(
        pH=float(row['pH']),
        suhu=float(row['Temprature']),
        rasa=int(row['Taste']),
        bau=int(row['Odor']),
        lemak=int(row['Fat']),
        kekeruhan=int(row['Turbidity']),
    )
    return res


def get_evaluation_result():
    """
    Menjalankan evaluasi lengkap terhadap dataset:
    - Split 70% data latih dan 30% data uji (random_state=42)
    - Perbandingan Prediksi Sistem vs Hasil Dataset
    - Kolom Benar/Salah
    - Matriks Konfusi
    """
    u = load_data()
    if u is None:
        return {"error": "Dataset milknew.csv tidak ditemukan di folder data/"}

    # Split 70% latih, 30% uji sesuai instruksi prompt acuan
    tr = u.groupby('grade').sample(frac=0.7, random_state=42)
    te = u[~u.index.isin(tr.index)].copy()

    # Evaluasi data latih
    tr = tr.copy()
    tr_res = [evaluate_single_row(r) for _, r in tr.iterrows()]
    tr['pred'] = [r['kelas'] for r in tr_res]
    tr_correct = int((tr['pred'] == tr['grade']).sum())
    akurasi_latih = (tr_correct / len(tr)) * 100 if len(tr) > 0 else 0.0

    # Evaluasi data uji (seluruh 25 data uji)
    te_res = [evaluate_single_row(r) for _, r in te.iterrows()]
    te['pred'] = [r['kelas'] for r in te_res]
    te['skor'] = [r['skor'] for r in te_res]
    te_correct = int((te['pred'] == te['grade']).sum())
    te_wrong = len(te) - te_correct
    akurasi_uji = (te_correct / len(te)) * 100 if len(te) > 0 else 0.0

    # Confusion matrix
    cm = pd.crosstab(te['grade'], te['pred'], rownames=['Aktual'], colnames=['Prediksi'])
    
    # Format confusion matrix agar mudah ditampilkan di Django template
    # Header kolom: kelas prediksi
    cm_cols = [c for c in cm.columns]
    cm_rows = []
    for actual_label in cm.index:
        row_vals = []
        for col in cm_cols:
            row_vals.append(int(cm.loc[actual_label, col]))
        cm_rows.append({
            'label': actual_label.upper(),
            'values': row_vals,
            'total': sum(row_vals),
        })

    # Tabel perbandingan lengkap (seluruh 25 sampel data uji)
    tabel_perbandingan = []
    for idx, (_, row) in enumerate(te.iterrows(), start=1):
        res = evaluate_single_row(row)
        hasil_dataset = str(row['grade']).lower()
        prediksi_sistem = res['kelas'].lower()
        is_benar = (hasil_dataset == prediksi_sistem)

        tabel_perbandingan.append({
            'no': idx,
            'ph': round(float(row['pH']), 2),
            'suhu': int(row['Temprature']),
            'rasa': int(row['Taste']),
            'bau': int(row['Odor']),
            'lemak': int(row['Fat']),
            'kekeruhan': int(row['Turbidity']),
            'total_indikator_1': int(row['Taste']) + int(row['Odor']) + int(row['Fat']) + int(row['Turbidity']),
            'skor_fuzzy': res['skor'],
            'hasil_dataset': hasil_dataset.upper(),
            'prediksi_sistem': prediksi_sistem.upper(),
            'is_benar': is_benar,
            'status': "Benar" if is_benar else "Salah",
            'badge_color': "bg-emerald-100 text-emerald-800 border-emerald-300" if is_benar else "bg-rose-100 text-rose-800 border-rose-300",
        })

    # Uji kasus acuan dari prompt dosen
    uji_kasus_acuan = [
        {"no": 1, "pH": 6.6, "suhu": 37, "jumlah_bernilai_1": 3, "skor_acuan": 80.6, "kelas_acuan": "HIGH"},
        {"no": 2, "pH": 8.5, "suhu": 70, "jumlah_bernilai_1": 4, "skor_acuan": 19.4, "kelas_acuan": "LOW"},
        {"no": 3, "pH": 6.6, "suhu": 37, "jumlah_bernilai_1": 0, "skor_acuan": 50.0, "kelas_acuan": "MEDIUM"},
        {"no": 4, "pH": 6.3, "suhu": 37, "jumlah_bernilai_1": 3, "skor_acuan": 50.0, "kelas_acuan": "MEDIUM"},
        {"no": 5, "pH": 6.6, "suhu": 47, "jumlah_bernilai_1": 3, "skor_acuan": 55.4, "kelas_acuan": "MEDIUM"},
    ]

    for kas in uji_kasus_acuan:
        tot = kas["jumlah_bernilai_1"]
        r = 1 if tot >= 1 else 0
        b = 1 if tot >= 2 else 0
        l = 1 if tot >= 3 else 0
        k = 1 if tot >= 4 else 0
        res = get_kualitas_susu(pH=kas["pH"], suhu=kas["suhu"], rasa=r, bau=b, lemak=l, kekeruhan=k)
        kas["skor_sistem"] = res['skor']
        kas["kelas_sistem"] = res['kelas'].upper()
        kas["is_cocok"] = (res['kelas'].upper() == kas['kelas_acuan'])
        kas["status"] = "Benar" if kas["is_cocok"] else "Salah"

    return {
        "total_data_unik": len(u),
        "jumlah_latih": len(tr),
        "jumlah_uji": len(te),
        "tr_correct": tr_correct,
        "te_correct": te_correct,
        "te_wrong": te_wrong,
        "akurasi_latih": round(akurasi_latih, 2),
        "akurasi_uji": round(akurasi_uji, 2),
        "cm_cols": [c.upper() for c in cm_cols],
        "cm_rows": cm_rows,
        "tabel_perbandingan": tabel_perbandingan,
        "uji_kasus_acuan": uji_kasus_acuan,
    }
