"""
WSGI config for susu_fuzzy project.

Vercel membutuhkan file ini, dan file yang di-export sebagai aplikasi
jika menggunakan framework Python Vercel.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "susu_fuzzy.settings")

application = get_wsgi_application()

# Mount export yang dibutuhkan platform serverless seperti Vercel
app = application
