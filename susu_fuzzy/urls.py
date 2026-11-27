"""
Susu kualitas fuzzy URL configuration.
Mengarahkan request ke app home untuk form, hasil, evaluasi, dan riwayat.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
