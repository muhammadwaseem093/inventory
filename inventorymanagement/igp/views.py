from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from asgiref.sync import sync_to_async
from django.db import transaction
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import IGP, Item
from utils.decorators import role_required
from .forms import IGPForm, ItemForm

# Helper functions for role-based permissions
def is_staff(user):
    return user.is_staff

def is_admin(user):
    return user.is_superuser


@login_required
@role_required('admin')
def igp_entry(request):
    return render(request, 'igp/create_igp.html')

@login_required
@role_required('admin')
def process_create_igp(request):
    if request.method == 'POST':
        # Initialize the form
        igp_form = IGPForm(request.POST)
        
        # Safely handle 'items_num' to avoid TypeError
        try:
            items_num = int(request.POST.get('items_num', 0))  # Default to 0 if not found
        except (ValueError, TypeError):
            messages.error(request, "Invalid number of items.")
            return redirect('igp_entry')

        # Check if the form is valid
        if igp_form.is_valid():
            igp = igp_form.save()
            
            items = []
            for i in range(1, items_num + 1):
                # Collect item data
                item_data = {
                    'description': request.POST.get(f'description_{i}'),
                    'unit': request.POST.get(f'unit_{i}'),
                    'quantity': request.POST.get(f'quantity_{i}'),
                }
                
                # Check if all item data is present
                if all(item_data.values()):
                    item = Item(igp=igp, **item_data)
                    item.save()
                    item.igp.add(igp)
                    items.append(item)
                else:
                    messages.error(request, f'Item {i} is incomplete.')
                    return redirect('igp_entry')
                
            # If everything is successful
            messages.success(request, 'IGP created successfully')
            return redirect('view_igp')
        else:
            messages.error(request, 'IGP creation failed due to invalid data')
            return redirect('igp_entry')
    
    return HttpResponse('Invalid request')

                    
    
    
    
    
@login_required
@user_passes_test(is_staff)
@user_passes_test(is_admin)
def view_igp(request):
    igp = IGP.objects.all()
    return render(request, 'igp/view_igp.html', {'igp': igp})

@login_required
@user_passes_test(is_admin)
def update_igp(request, pk):
    igp = get_object_or_404(IGP, pk=pk)
    if request.method == 'POST':
        igp.igp_number = request.POST.get('igp_number')
        igp.date = request.POST.get('date')
        igp.type = request.POST.get('type')
        igp.unit = request.POST.get('unit')
        igp.description = request.POST.get('description')
        igp.quantity = request.POST.get('quantity')
        igp.messer = request.POST.get('messer')
        igp.save()
        messages.success(request, 'IGP updated successfully')
        return redirect('view_igp')
    return render(request, 'igp/update_igp.html', {'igp': igp})

@login_required
@user_passes_test(is_admin)
def delete_igp(request, pk):
    igp = get_object_or_404(IGP, pk=pk)
    igp.delete()
    return redirect('view_igp')
