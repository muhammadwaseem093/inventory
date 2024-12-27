from .models import Type 
from django import forms

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'description']
        
        