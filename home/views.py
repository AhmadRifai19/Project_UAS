from django.shortcuts import render, redirect, get_object_or_404
from .forms import MilkForm
from fuzzy import get_kualitas_susu, RULES
from .models import EvaluasiSusu
from .evaluate import get_evaluation_result


def index(request):
    """Landing page"""
    return render(request, "home/index.html")


def predict(request):
    """Form input dan eksekusi inferensi fuzzy"""
    form = MilkForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        result = get_kualitas_susu(
            pH=data['ph'],
            suhu=data['suhu'],
            rasa=int(data['rasa']),
            bau=int(data['bau']),
            lemak=int(data['lemak']),
            kekeruhan=int(data['kekeruhan']),
        )

        # Simpan evaluasi ke database
        ev = EvaluasiSusu.objects.create(
            ph=data['ph'],
            suhu=data['suhu'],
            rasa=data['rasa'],
            bau=data['bau'],
            lemak=data['lemak'],
            kekeruhan=data['kekeruhan'],
            hasil=result['kelas'],
            skor=result['skor'],
        )

        return redirect("hasil", pk=ev.pk)

    return render(request, "home/predict.html", {"form": form, "rules": RULES})


def hasil(request, pk):
    """Detail hasil fuzzy + aturan aktif"""
    ev = get_object_or_404(EvaluasiSusu, pk=pk)
    result = get_kualitas_susu(
        pH=ev.ph,
        suhu=ev.suhu,
        rasa=int(ev.rasa),
        bau=int(ev.bau),
        lemak=int(ev.lemak),
        kekeruhan=int(ev.kekeruhan),
    )

    context = {
        "ev": ev,
        "result": result,
        "rules": RULES,
    }
    return render(request, "home/hasil.html", context)


def riwayat(request):
    """Daftar semua riwayat evaluasi"""
    riwayat_list = EvaluasiSusu.objects.all()
    high_count = riwayat_list.filter(hasil="high").count()
    medium_count = riwayat_list.filter(hasil="medium").count()
    low_count = riwayat_list.filter(hasil="low").count()

    context = {
        "riwayat": riwayat_list,
        "total_count": riwayat_list.count(),
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
    }
    return render(request, "home/riwayat.html", context)


def evaluasi(request):
    """Hasil evaluasi model: akurasi, confusion matrix, tabel uji kasus"""
    eval_res = get_evaluation_result()
    return render(request, "home/evaluasi.html", eval_res)
