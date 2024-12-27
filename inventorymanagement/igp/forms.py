from django import forms 
from .models import IGP, Item

class IGPForm(forms.ModelForm):
    class Meta:
        model = IGP
        fields = ['igp_number', 'messer', 'date', 'vehicle_number', 'vehicle_type', 'driver_name', 'driver_cnic', 'type', 'address']
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [ 'description', 'unit', 'quantity']