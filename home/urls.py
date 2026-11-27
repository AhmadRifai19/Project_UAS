from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("predict/", views.predict, name="predict"),
    path("hasil/<int:pk>/", views.hasil, name="hasil"),
    path("riwayat/", views.riwayat, name="riwayat"),
    path("evaluasi/", views.evaluasi, name="evaluasi"),
]
