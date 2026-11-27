"""
Form input parameter kualitas susu.
Menerima pH, suhu, dan 4 indikator fisik (0/1).
"""

from django import forms


class MilkForm(forms.Form):
    """Form data susu untuk dievaluasi oleh mesin fuzzy."""

    ph = forms.FloatField(
        label="pH",
        min_value=0.0,
        max_value=14.0,
        initial=6.6,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2.5 border border-slate-300 rounded-xl focus:ring-2 focus:ring-teal-500 text-base',
            'step': '0.1',
            'placeholder': '0.0 - 14.0',
        })
    )
    suhu = forms.FloatField(
        label="Suhu (°C)",
        min_value=0.0,
        max_value=100.0,
        initial=37.0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2.5 border border-slate-300 rounded-xl focus:ring-2 focus:ring-teal-500 text-base',
            'step': '0.1',
            'placeholder': '0.0 - 100.0',
        })
    )

    rasa = forms.ChoiceField(
        label="Rasa (0=Buruk, 1=Baik)",
        choices=[("1", "Baik"), ("0", "Buruk")],
        initial="1",
        widget=forms.RadioSelect(attrs={'class': 'radio-indicator'})
    )
    bau = forms.ChoiceField(
        label="Bau (0=Buruk, 1=Baik)",
        choices=[("1", "Baik"), ("0", "Buruk")],
        initial="1",
        widget=forms.RadioSelect(attrs={'class': 'radio-indicator'})
    )
    lemak = forms.ChoiceField(
        label="Lemak (0=Kurang, 1=Cukup)",
        choices=[("1", "Cukup"), ("0", "Kurang")],
        initial="1",
        widget=forms.RadioSelect(attrs={'class': 'radio-indicator'})
    )
    kekeruhan = forms.ChoiceField(
        label="Kekeruhan (0=Keruh, 1=Jernih)",
        choices=[("1", "Jernih"), ("0", "Keruh")],
        initial="1",
        widget=forms.RadioSelect(attrs={'class': 'radio-indicator'})
    )

    def clean_ph(self):
        val = self.cleaned_data.get('ph')
        if val is not None and not (0.0 <= val <= 14.0):
            raise forms.ValidationError("pH harus dalam rentang 0 - 14.")
        return val

    def clean_suhu(self):
        val = self.cleaned_data.get('suhu')
        if val is not None and not (0.0 <= val <= 100.0):
            raise forms.ValidationError("Suhu harus dalam rentang 0 - 100 °C.")
        return val
