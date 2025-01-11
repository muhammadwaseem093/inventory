
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import IGP, IGPItem
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q 
from items.models import Item
from supplier.models import Supplier
from type.models import Type
from unit.models import Unit
from utils.decorators import role_required
from .forms import IGPForm, IGPItemForm
from django.http import JsonResponse




# Helper functions for role-based permissions
def is_staff(user):
    return user.is_staff
 
def is_admin(user):
    return user.is_superuser

@login_required
@role_required('staff')
def dashboard(request):
    supplier_count = Supplier.objects.count()
    vendor_count= Vendor.objects.count()
    items_count=Item.objects.count()
    igp_count = IGP.objects.count()
    return render(request, 'dashboards/staff.html',{'supplier_count':supplier_count,
        'vendor_count':vendor_count,
        'igp_count':igp_count, "items_count":items_count})



@login_required
@role_required('admin', 'staff')
def igp_entry(request):
    suppliers = Supplier.objects.all()
    types = Type.objects.all()
    context = {
        'suppliers': suppliers,
        'types': types,
        'items': Item.objects.all(),
        'units': Unit.objects.all(),
    }
    return render(request, 'igp/create_igp.html', context)

@login_required
@role_required('admin', 'staff')
def process_create_igp(request):
    suppliers = Supplier.objects.all()
    types = Type.objects.all()
    if request.method == 'POST':
        igp_form = IGPForm(request.POST)
        if igp_form.is_valid():
            igp = igp_form.save()
            igp_number = igp.igp_number
            return redirect(reverse('process_igp_item')+ f'?igp_number={igp_number}')
        else:
            messages.error(request, "invalid")
            print("error in forms")
            return redirect('igp_entry')
    else:
        igp_form = IGPForm()
    return render(request, 'igp/create_igp.html', {'igp':igp_form})
    
    
@login_required
@role_required('admin', 'staff')
def process_igp_item(request):
    # Debugging: Check if igp_number is being fetched properly
    igp_number = request.GET.get('igp_number') or request.POST.get('igp_number')
    if not igp_number:
        return JsonResponse({'success': False, 'message': 'No IGP Number Provided.'})

    igp = get_object_or_404(IGP, igp_number=igp_number)
    
    items = Item.objects.all()
    units = Unit.objects.all()
    
    if request.method == 'POST':
        print("POST request received.")  # Debugging: Check if we are ijnside POST block
        
        num_items = 6
        item_forms = []

        # Debugging: Check the loop start and iterating over items
        for i in range(1, num_items + 1):
            item_key = f'item_{i}'
            description_key = f"description_{i}"
            unit_key = f'unit_{i}'
            quantity_key = f"quantity_{i}"
            
            # Fetching values from POST data
            item_id = request.POST.get(item_key)
            description = request.POST.get(description_key, '')
            unit = request.POST.get(unit_key)
            quantity = request.POST.get(quantity_key)

            if item_id:
                data = {
                    'item': item_id,
                    'description': description,
                    'unit': unit,
                    'quantity': quantity
                }
                
                form = IGPItemForm(data)
                if form.is_valid():
                    igp_item = form.save(commit=False)
                    igp_item.igp = igp
                    igp_item.save()
                else:
                    for field, errors in form.errors.items():
                        print(f"Field: {field} - Errors: {errors}")
                    item_forms.append(form)
                    return JsonResponse({"success": False, "message": 'Invalid data for {i}. Errors: {form.errors}'}, status=400)

        return redirect('view_igp')
        
    else:
        form = IGPItemForm()

    return render(request, 'igp/item_form_row.html', {
        "form": form,
        'range': range(1, 7),
        'items': items,
        'units': units,
        'igp_number': igp_number
    })






@login_required
@role_required('admin','staff')
def view_igp(request):
    query =Q()
    igp_number = request.GET.get('igp_number', '').strip()
    messer = request.GET.get('messer','').strip()
    
    if igp_number or messer:
        if igp_number:
            query &= Q(igp_number__icontains=igp_number)
        if messer:
            query &= Q(messer__name__icontains=messer)
        igp_records = IGP.objects.filter(query).order_by('-date')
    else:
        igp_records = IGP.objects.all().order_by('-igp_number')

        
        
    paginator = Paginator(igp_records, 10)
    page_number = request.GET.get('page')
    igp_list = paginator.get_page(page_number)
    
    
    return render(request, 'igp/view_igp.html', {'igp_list': igp_list,'search_active': bool(igp_number or messer)})

@login_required
@role_required('admin','staff')
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
@role_required('admin', 'staff')
def delete_igp(request, pk):
    try:
        igp = IGP.objects.get(id=pk)
    except IGP.DoesNotExist:
        raise Http404("IGP not found")

    if request.method == 'POST':
        igp.delete()
        messages.success(request, 'IGP deleted successfully!')
        return redirect('view_igp') 

    return render(request, 'igp/delete_igp.html', {'igp': igp})

@login_required
@role_required('admin', 'staff')
def delete_selected_igps(request):
    if request.method =='POST':
        selected_igps = request.POST.getlist('selected_igps')
        IGP.objects.filter(id__in=selected_igps).delete()
        return redirect('view_igp')
    return HttpResponse('Invalid Requst', status=400)