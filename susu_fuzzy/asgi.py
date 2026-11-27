"""
ASGI config for susu_fuzzy project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'susu_fuzzy.settings')

application = get_asgi_application()
