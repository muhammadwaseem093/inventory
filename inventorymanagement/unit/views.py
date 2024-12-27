from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UnitForm
from .models import Unit
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
# Create your views here.

@login_required
@role_required('admin')
def create_unit(request):
    return render(request, 'unit/create_unit.html')


@login_required
@role_required('admin')
def process_unit_creation(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Unit created successfully')
            return redirect('unit_list')  
        else:
            messages.error(request, 'Unit creation failed. Please correct the errors.')
    else:
        form = UnitForm()

    context = {
        'form': form
    }
    return render(request, 'unit/create_unit.html', context)




def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'unit/unit_list.html', {'units': units})


@login_required
@role_required('admin')
def edit_unit(request, unit_id):
    unit = Unit.objects.get(id=unit_id)
    return render(request, 'unit/edit_unit.html', {'unit': unit})

@login_required
@role_required('admin')
def process_unit_edit(request, unit_id):
    unit = Unit.objects.get(id=unit_id)
    if request.method == "POST":
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit updated successfully')
            return redirect('unit_list')
        else:
            messages.error(request, 'Unit update failed')
            return redirect('edit_unit', unit_id)
    else:
        form = UnitForm(instance=unit)
    return render(request, 'unit/edit_unit.html', {'form': form, 'unit': unit})

@login_required
@role_required('admin')
def delete_unit(request, unit_id):
    unit = Unit.objects.get(id=unit_id)
    unit.delete()
    messages.success(request, 'Unit deleted successfully')
    return redirect('unit_list')

