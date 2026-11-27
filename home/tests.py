from django.test import TestCase, Client
from django.urls import reverse
from fuzzy import get_kualitas_susu
from home.models import EvaluasiSusu


class FuzzyEngineTestCase(TestCase):
    def test_kasus_acuan(self):
        """Memvalidasi 5 kasus acuan dari dokumen petunjuk."""
        kasus = [
            (6.6, 37, 1, 1, 1, 0, "high"),    # 3 bernilai 1
            (8.5, 70, 1, 1, 1, 1, "low"),     # 4 bernilai 1
            (6.6, 37, 0, 0, 0, 0, "medium"),  # 0 bernilai 1
            (6.3, 37, 1, 1, 1, 0, "medium"),  # 3 bernilai 1
            (6.6, 47, 1, 1, 1, 0, "medium"),  # 3 bernilai 1
        ]
        for ph, suhu, r, b, l, k, expected_grade in kasus:
            res = get_kualitas_susu(ph, suhu, r, b, l, k)
            self.assertEqual(
                res["kelas"],
                expected_grade,
                f"Gagal pada pH={ph}, Suhu={suhu}: diharapkan {expected_grade}, didapat {res['kelas']}"
            )


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_halaman_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menilai Kualitas Susu Secara")

    def test_halaman_predict_get(self):
        response = self.client.get(reverse("predict"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Masukkan Parameter Susu")

    def test_halaman_predict_post_redirect(self):
        data = {
            "ph": 6.6,
            "suhu": 37.0,
            "rasa": "1",
            "bau": "1",
            "lemak": "1",
            "kekeruhan": "0",
        }
        response = self.client.post(reverse("predict"), data)
        self.assertEqual(response.status_code, 302)
        ev = EvaluasiSusu.objects.first()
        self.assertIsNotNone(ev)
        self.assertEqual(ev.hasil, "high")

    def test_halaman_evaluasi(self):
        response = self.client.get(reverse("evaluasi"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evaluasi & Perbandingan Jawaban Sistem")
