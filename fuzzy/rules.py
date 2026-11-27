"""
Modul metadata aturan fuzzy untuk display dan evaluasi.
"""

RULES = [
    {
        'id': 1,
        'nama': "IF pH TIDAK normal OR Suhu TIDAK aman THEN Kualitas LOW",
        'antecedent': "pH TIDAK normal OR Suhu TIDAK aman",
        'consequent': "LOW",
        'deskripsi': "Kualitas rendah jika pH di luar batas normal atau suhu terlalu rendah/tinggi."
    },
    {
        'id': 2,
        'nama': "IF pH normal AND Suhu aman AND Kondisi TIDAK baik THEN MEDIUM",
        'antecedent': "pH normal AND Suhu aman AND Kondisi TIDAK baik",
        'consequent': "MEDIUM",
        'deskripsi': "Kualitas sedang jika pH dan suhu baik, tetapi beberapa indikator fisik (rasa/bau/lemak/kekeruhan) buruk."
    },
    {
        'id': 3,
        'nama': "IF pH normal AND Suhu aman AND Kondisi baik THEN HIGH",
        'antecedent': "pH normal AND Suhu aman AND Kondisi baik",
        'consequent': "HIGH",
        'deskripsi': "Kualitas tinggi jika pH normal, suhu aman, dan mayoritas indikator fisik dalam kondisi baik."
    }
]
