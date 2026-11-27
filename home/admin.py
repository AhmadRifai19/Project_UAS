from django.contrib import admin
from .models import EvaluasiSusu


@admin.register(EvaluasiSusu)
class EvaluasiSusuAdmin(admin.ModelAdmin):
    list_display = ('id', 'ph', 'suhu', 'rasa', 'bau', 'lemak', 'kekeruhan', 'hasil', 'skor', 'dibuat_pada')
    list_filter = ('hasil',)
    search_fields = ('hasil',)
    list_max_show_all = True
