from django.db import models
from django.utils import timezone
from items.models import Item
from supplier.models import Supplier
from type.models import Type
from unit.models import Unit


class IGP(models.Model):
    igp_number = models.CharField(max_length=20, unique=True)
    messer = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    vehicle_number = models.CharField(max_length=20, blank=True , default='Nill')
    vehicle_type = models.CharField(max_length=50, blank=True, default='Nill')
    driver_name = models.CharField(max_length=50, blank=True, default='Nill')
    driver_contact = models.CharField(max_length=15, blank=True, default='Nill')
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    address = models.CharField(max_length=100 , default="supplier address")

    def __str__(self):
        return f"IGP {self.igp_number} - {self.messer}"


class IGPItem(models.Model):
    igp = models.ForeignKey(IGP, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def clean_item(self):
        item_id = self.cleaned_data.get('item')
        if not Item.objects.filter(id=item_id).exists():
            raise forms.ValidationError("Item does not exist.")
        return item_id

    def clean_unit(self):
        unit_name = self.cleaned_data.get('unit')
        try:
            unit = Unit.objects.get(name=unit_name)
        except Unit.DoesNotExist:
            raise ValidationError(f"The unit '{unit_name}' does not exist.")
        return unit
    
    
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0")
        return quantity

    def __str__(self):
        return f"{self.igp} - {self.item} - {self.quantity} {self.unit}"
