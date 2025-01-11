# forms.py
from django import forms
from .models import IGP, IGPItem
from items.models import Item
from supplier.models import Supplier
from type.models import Type
from unit.models import Unit

class IGPForm(forms.ModelForm):
    class Meta:
        model = IGP
        fields = ['igp_number', 'messer', 'date', 'vehicle_number', 'vehicle_type', 'driver_name', 'driver_contact', 'type', 'address']

class IGPItemForm(forms.ModelForm):
    class Meta:
        model = IGPItem
        fields = ['item', 'description', 'unit', 'quantity']
        
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label="Select a unit")
    

