from django.db import models
from vendor.models import Vendor
from items.models import Item 
from unit.models import Unit 
from type.models import Type


class OGP(models.Model):
    ogp_number = models.CharField(max_length=50,unique=True)
    messer= models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date =models.DateField()
    vehicle_number = models.CharField(max_length=50, null=True, blank=True)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    driver_name=models.CharField(max_length=100, blank=True, null=True)
    driver_contact=models.CharField(max_length=15, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    address=models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"OGP {self.ogp_number} - {self.messer}"
    
    
class OGPItem(models.Model):
    ogp = models.ForeignKey(OGP, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description=models.CharField(max_length=100, blank=False , null=False)
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=10, decimal_places=2)
    
    def clean_item(self):
        item_id = self.cleaned_data.get('item')
        if not Item.objects.filter(id=item_id).exists():
            raise forms.ValidationError('Item does not exist.')
        return item_id
    
    def clean_unit(self):
        unit_name = self.cleaned_data.get('unit')
        try:
            unit = Unit.objects.get(name=unit_name)
        except Unit.DoesNotExist:
            raise ValidationError(f"The Unit ' {unit_name}' does not exist")
        return unit
        
    
    
    def clean_quantity(self):
        quantity=self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than 0')
        return quantity
    
    
    def __str__(self):
        return f"{self.ogp} - {self.item} - {self.quantity} - {self.unit}"