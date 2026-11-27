"""
Mesin inferensi fuzzy Mamdani untuk penilaian kualitas susu.
Pipeline: fuzzifikasi -> evaluasi aturan -> implikasi MIN -> agregasi MAX
-> defuzzifikasi centroid -> klasifikasi low/medium/high.
"""

import numpy as np

from .membership import (
    mu_pH_normal,
    mu_suhu_aman,
    OUT_LOW_ARRAY,
    OUT_MEDIUM_ARRAY,
    OUT_HIGH_ARRAY,
    defuzzify_centroid,
)


def get_kualitas_susu(pH, suhu, rasa, bau, lemak, kekeruhan):
    """
    Menghitung kualitas susu berdasarkan 3 aturan fuzzy Mamdani.

    Parameter:
        pH        : float 0-14
        suhu      : float 0-100 (derajat Celsius)
        rasa      : 0/1
        bau       : 0/1
        lemak     : 0/1
        kekeruhan : 0/1

    Returns:
        dict berisi skor, kelas, derajat keanggotaan, dan alpha aturan.
    """
    # --- Fuzzifikasi input ---
    mu_ph = mu_pH_normal(pH)
    mu_suhu = mu_suhu_aman(suhu)

    # Kondisi baik bersifat tegas (crisp):
    # 1 jika jumlah rasa+bau+lemak+kekeruhan yang bernilai 1 >= 2, selain itu 0
    total_bernilai_1 = sum(
        1 for nilai in (rasa, bau, lemak, kekeruhan) if int(nilai) == 1
    )
    kondisi_baik = 1.0 if total_bernilai_1 >= 2 else 0.0

    # --- Evaluasi 3 aturan ---
    # Aturan 1: IF pH TIDAK normal OR suhu TIDAK aman THEN low
    # NOT = 1 - mu, OR = max
    alpha_low = max(1.0 - mu_ph, 1.0 - mu_suhu)

    # Aturan 2: IF pH normal AND suhu aman AND kondisi TIDAK baik THEN medium
    # AND = min, NOT kondisi = 1 - kondisi
    alpha_medium = min(mu_ph, mu_suhu, 1.0 - kondisi_baik)

    # Aturan 3: IF pH normal AND suhu aman AND kondisi baik THEN high
    alpha_high = min(mu_ph, mu_suhu, kondisi_baik)

    # --- Implikasi MIN (clipping) ---
    agg_low = np.minimum(alpha_low, OUT_LOW_ARRAY)
    agg_medium = np.minimum(alpha_medium, OUT_MEDIUM_ARRAY)
    agg_high = np.minimum(alpha_high, OUT_HIGH_ARRAY)

    # --- Agregasi MAX ---
    agregasi = np.maximum(np.maximum(agg_low, agg_medium), agg_high)

    # --- Defuzzifikasi centroid ---
    skor = defuzzify_centroid(agregasi)

    # --- Klasifikasi akhir ---
    if skor < 37.5:
        kelas = "low"
    elif skor < 62.5:
        kelas = "medium"
    else:
        kelas = "high"

    return {
        "skor": round(skor, 2),
        "skor_akurat": skor,
        "kelas": kelas,
        "mu": {
            "ph": round(mu_ph, 4),
            "suhu": round(mu_suhu, 4),
            "kondisi_baik": round(kondisi_baik, 4),
            "total_bernilai_1": total_bernilai_1,
        },
        "alpha": {
            "low": round(alpha_low, 4),
            "medium": round(alpha_medium, 4),
            "high": round(alpha_high, 4),
        },
    }
