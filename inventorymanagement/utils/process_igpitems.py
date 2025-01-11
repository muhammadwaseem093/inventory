from django.core.exceptions import ObjectDoesNotExist
from igp.models import IGPItem 
from items.models import Item 
from unit.models import Unit 
from supplier.models import Supplier 
from type.models import Type 

def process_igp_items(request, igp, num_items=5):
    first_item_valid = False 
    for i in range(1, num_items + 1):
        item_name = request.POST.get(f'item_{i}')
        description= request.POST.get(f'description_{i}')
        unit_name=request.POST.get(f'unit_{i}')
        quantity=request.POST.get(f'quantity_{i}')
        
        if i == 1 and not any([item_name, description, unit_name, quantity]):
            return False, f"At least one field must be filled in the first item."
        
        if any([item_name, description,unit_name,quantity]):
            try:
                item=Item.objects.get(id = item_name) if item_name else None 
                unit=Unit.objects.get(id=unit_name) if unit_name else None 
                quantity = float(quantity) if quantity else None 
                
                if item and unit and quantity:
                    IGPItem.objects.create(
                        igp=igp,
                        item=item,
                        description=description or '',
                        unit = unit,
                        quantity=quantity
                    )
                else:
                    return False, f"Skipping item {i} due to incomplete data"
            except (Item.DoesNotExist, Unit.DoesNotExist, ValueError) as e:
                return False, f"Error Processing Item {i}: {str(e)}"
    return True, "Items Processed Successfully!"