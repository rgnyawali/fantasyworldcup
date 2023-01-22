from django import forms
from .models import Match



class AdminForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'
