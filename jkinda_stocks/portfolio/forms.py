from django import forms 
from .models import Portfolio

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
                  'name', 
                  'description',
                  'type',
                  ]
        type = forms.ChoiceField(choices=Portfolio.TYPES)