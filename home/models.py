from django.db import models


class EvaluasiSusu(models.Model):
    """Menyimpan riwayat setiap pengujian kualitas susu."""

    # Input
    ph = models.FloatField()
    suhu = models.FloatField()
    rasa = models.CharField(max_length=5)
    bau = models.CharField(max_length=5)
    lemak = models.CharField(max_length=5)
    kekeruhan = models.CharField(max_length=5)

    # Hasil
    hasil = models.CharField(max_length=10)
    skor = models.FloatField()

    # Meta
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dibuat_pada"]
        verbose_name = "Evaluasi Susu"
        verbose_name_plural = "Evaluasi Susu"

    def __str__(self):
        return f"Evaluasi {self.dibuat_pada:%Y-%m-%d} ({self.hasil}, skor {self.skor})"
