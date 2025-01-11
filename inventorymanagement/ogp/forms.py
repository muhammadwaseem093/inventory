from django import forms 
from .models import OGP, OGPItem 
from items.models import Item 
from supplier.models import Supplier 
from type.models import Type 
from unit.models import Unit 

class OGPForm(forms.ModelForm):
    class Meta:
        model = OGP
        fields = ['ogp_number', 'messer', 'date','vehicle_number', 'vehicle_type', 'driver_name', 'driver_contact', 'type', 'address']
        
class OGPItemForm(forms.ModelForm):
    class Meta:
        model = OGPItem
        fields = ['item', 'description', 'unit','quantity']
        
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label='Select a Unit')