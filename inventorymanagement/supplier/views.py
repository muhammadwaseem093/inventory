from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http import Http404 
from .forms import SupplierForm
from .models import Supplier
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required

@login_required
@role_required('admin','staff')
def create_supplier(request):
    return render(request, 'supplier/create_supplier.html')


@login_required
@role_required('admin','staff')
def process_supplier_creation(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.save()
            messages.success(request, 'Supplier Creation Successfully!')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Supplier creation failed')
            return redirect('create_supplier')
            
    else:
        form = SupplierForm()
    return render(request, 'supplier/create_supplier.html', {'form':form})


@login_required
@role_required('admin','staff')
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/supplier_list.html', {'suppliers':suppliers})


@login_required
@role_required('admin','staff')
def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    return render(request, 'supplier/edit_supplier.html', {'supplier':supplier})

@login_required
@role_required('admin','staff')
def process_supplier_edit(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier Updated Successfully')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Supplier creation Fialed')
            return redirect('edit_supplier', supplier_id)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier/edit_supplier.html', {'form':form , 'supplier':supplier})    


@login_required
@role_required('admin')
def delete_supplier(request, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
    except Supplier.DoesNotExist:
        raise Http404('Supplier does Not Exists')
    
    if request.method =='POST':
        supplier.delete()
        messages.success(request, 'Supplier Deleted Successfully!')
        return redirect('supplier_list')
    return render(request, 'supplier/delete_supplier.html', {'supplier':supplier})

