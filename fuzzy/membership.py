"""
Fuzzy membership functions untuk sistem penilaian kualitas susu.
Menggunakan fungsi trapesium (a, b, c, d) dan segitiga (a, b, c).
Semua dihitung manual dengan numpy (tanpa scikit-fuzzy).
"""

import numpy as np


def trapmf(x, a, b, c, d):
    """
    Trapezoidal membership function.
    Naik dari a ke b, tetap di c, turun ke d.
    """
    x = float(x)
    if x <= a or x >= d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if a < x < b:
        return (x - a) / (b - a) if b != a else 0.0
    return (d - x) / (d - c) if d != c else 0.0


def trimf(x, a, b, c):
    """
    Triangular membership function.
    """
    return trapmf(x, a, b, b, c)


# ==============================
# 1. Himpunan input
# ==============================

def mu_pH_normal(ph):
    """pH normal: (6.2, 6.4, 6.8, 7.0)"""
    return trapmf(ph, 6.2, 6.4, 6.8, 7.0)

def mu_suhu_aman(suhu):
    """Suhu aman: (25, 34, 45, 50)"""
    return trapmf(suhu, 25, 34, 45, 50)


# ==============================
# 2. Himpunan output (skor 0 - 100)
# ==============================

def out_low(y):
    """Full 0-25, turun ke 0 di 50."""
    return trapmf(y, 0, 0, 25, 50)

def out_medium(y):
    """Segitiga (25, 50, 75)."""
    return trimf(y, 25, 50, 75)

def out_high(y):
    """Naik dari 50, full 75-100."""
    return trapmf(y, 50, 75, 100, 100)


OUTPUT_GRID = np.linspace(0.0, 100.0, 1001)
OUT_LOW_ARRAY = np.array([out_low(y) for y in OUTPUT_GRID])
OUT_MEDIUM_ARRAY = np.array([out_medium(y) for y in OUTPUT_GRID])
OUT_HIGH_ARRAY = np.array([out_high(y) for y in OUTPUT_GRID])


# ==============================
# 3. Helper defuzzifikasi centroid
# ==============================

def defuzzify_centroid(agg_curve):
    """Menghitung nilai centroid dari kurva agregasi fuzzy."""
    total_luas = np.sum(agg_curve)
    if total_luas == 0:
        return 0.0
    return float(np.sum(OUTPUT_GRID * agg_curve) / total_luas)
