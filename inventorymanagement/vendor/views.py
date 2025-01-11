from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.http import Http404 
from .forms import VendorForm
from .models import Vendor
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required


@login_required
@role_required('admin','staff')
def create_vendor(request):
    return render(request, 'vendor/create_vendor.html')

@login_required
@role_required('admin','staff')
def process_vendor_creation(request):
    if request.method =='POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor Created Successfully!')
            return redirect('vendor_list')
        else:
            messages.error(request, 'Vendor Creation Failed.')
            return render(request, 'vendor/create_vendor.html', {'form':form})
    else:
        form = VendorForm()
    return render(request, 'vendor/create_vendor.html', {'form':form})


@login_required
@role_required('admin','staff')
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {"vendors":vendors})


@login_required
@role_required('admin','staff')
def edit_vendor(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    return render(request, 'vendor/edit_vendor.html', {'vendor':vendor})


@login_required
@role_required('admin','staff')
def process_vendor_edit(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor Updated Successfully!')
            return redirect('vendor_list')
        else:
            messages.error(request, 'Vendor Update Failed')
            return redirect('edit_vendor', vendor_id)
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor/edit_vendor.html', {'form':form , 'vendor':vendor})


@login_required
@role_required('admin')
def delete_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        raise Http404('Vendor Does Not exist')
    
    if request.method =='POST':
        vendor.delete()
        messages.success(request, 'Vendor Deleted Successfully!')
        return redirect('vendor_list')
    return render(request, 'vendor/delete_vendor.html', {"vendor":vendor})