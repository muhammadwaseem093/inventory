from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import OGP, OGPItem
from django.urls import reverse 
from django.core.paginator import Paginator
from django.db.models import Q 
from items.models import Item 
from vendor.models import Vendor
from type.models import Type 
from unit.models import Unit 
from utils.decorators import role_required
from .forms import OGPForm, OGPItemForm
from django.http import JsonResponse

def is_staff(user):
    return user.is_staff
def is_admin(user):
    return user.is_superuser

#create ogp 
@login_required
@role_required('admin', 'staff')
def ogp_entry(request):
    vendors = Vendor.objects.all()
    types = Type.objects.all()
    items = Item.objects.all()
    units = Unit.objects.all()
    context = {
        'vendors':vendors,
        'types':types,
        'items':items,
        'units':units
    }
    return render(request, 'ogp/create_ogp.html', context)


@login_required
@role_required('admin','staff')
def process_create_ogp(request):
    vendors = Vendor.objects.all()
    types = Type.objects.all()
    if request.method == 'POST':
        form = OGPForm(request.POST)
        if form.is_valid():
            ogp = form.save()
            ogp_number = ogp.ogp_number
            return redirect(reverse('process_ogp_item')+f'?ogp_number={ogp_number}')
        else:
            messages.error(request, "Invalid OGP Number")
            return redirect('ogp_entry')
    else:
        ogp_form = OGPForm()
    return render(request, 'ogp/create_ogp.html', {'ogp_form':ogp_form})



@login_required
@role_required('admin','staff')
def process_ogp_item(request):
    ogp_number = request.GET.get('ogp_number') or request.POST.get('ogp_number')
    if not ogp_number:
        return JsonResponse({'success':False, 'Message':'No OGP Number Provided'})
    
    ogp = get_object_or_404(OGP, ogp_number=ogp_number)
    
    items  = Item.objects.all()
    units = Unit.objects.all()
    
    if request.method =='POST':
        num_items = 6
        item_forms = []
        
        for i in range(1 , num_items + 1 ):
            item_key = f'item_{i}'
            description_key = f'description_{i}'
            unit_key = f'unit_{i}'
            quantity_key = f'quantity_{i}'
            
            # fetching value from POST data
            item_id = request.POST.get(item_key)
            description = request.POST.get(description_key,'')
            unit = request.POST.get(unit_key)
            quantity=request.POST.get(quantity_key)
            
            if item_id:
                data = {
                    'item':item_id,
                    'description':description,
                    'unit':unit,
                    'quantity':quantity
                }
                
                form = OGPItemForm(data)
                
                if form.is_valid():
                    ogp_item = form.save(commit=False)
                    ogp_item.ogp = ogp
                    ogp_item.save()
                else:
                    for field, error in form.errors.items():
                        print(f"Field: {field} - Errors: {errors}")
                    item_forms.append(form)
                    return JsonResponse({"success":False, "message":'Invalid data for {i}. Error: {form.errors}'}, status=400)
        return redirect('view_ogp')
    else:
        form = OGPItemForm()
    return render(request, 'ogp/item_form_row.html', {
        'form':form,
        'range': range(1, 7),
        'items':items,
        'units':units,
        'ogp_number':ogp_number
    })


@login_required
@role_required('admin', 'staff')
def view_ogp(request):
    query = Q()
    ogp_number = request.GET.get('ogp_number','').strip()
    messer = request.GET.get('messer', '').strip()
    
    if ogp_number or messer:
        if ogp_number:
            query &= Q(ogp_number__icontains=ogp_number)
        if messer:
            query &= Q(messer__name__icontains=messer)
        ogp_records = OGP.objects.filter(query).order_by('-date')
    else:
        ogp_records = OGP.objects.all().order_by('-ogp_number')
        
        
    paginator = Paginator(ogp_records,10)
    page_number = request.GET.get('page')
    ogp_list = paginator.get_page(page_number)
    
    return render(request, 'ogp/view_ogp.html', {'ogp_list':ogp_list, 'search_activate':bool(ogp_number or messer )})


@login_required
@role_required('admin', 'staff')
def update_ogp(request, pk):
    pass


@login_required
@role_required('admin', 'staff')
def delete_ogp(request, pk):
    try:
        ogp = OGP.objects.get(id=pk)
    except OGP.DoesNotExist:
        raise Http404('IGP Not Found')
    
    if request.method == 'POST':
        igp.delete()
        messages.success(request, ' OGP Deleted Successfully! ')
        return redirect('view_ogp')
    return render(request, 'ogp/delete_ogp.html', {'ogp':ogp})



@login_required
@role_required('admin', 'staff') 
def get_filtered_data(request):
    filter_type = request.GET.get('filter', 'daily')
    if filter_type == 'daily':
        date_filter = datetime.now() - timedelta(days=1)
    elif filter_type == 'weekly':
        date_filter = datetime.now() - timedelta(weeks=1)
    elif filter_type == 'monthly':
        date_filter = datetime.now() - timedelta(days=30)
    else:
        date_filter = datetime.now() - timedelta(days=365)

    igps = IGP.objects.filter(date__gte=date_filter)
    trends_labels = [igp.date.strftime('%Y-%m-%d') for igp in igps]
    trends_igp = [1 for igp in igps]
    trends_ogp = [1 for igp in igps]

    data = {
        'trends_labels': trends_labels,
        'trends_igp': trends_igp,
        'trends_ogp': trends_ogp,
    }
    return JsonResponse(data)
    