"""
Paket fuzzy untuk sistem penilaian kualitas susu berbasis logika Mamdani.
"""

from .engine import get_kualitas_susu
from .rules import RULES

__all__ = ["get_kualitas_susu", "RULES"]
