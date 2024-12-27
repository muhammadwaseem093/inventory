from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import TypeForm
from .models import Type
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
# Create your views here.

@login_required
@role_required('admin')
def create_type(request):
    return render(request, 'type/create_type.html')

@login_required
@role_required('admin')
def process_type_creation(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type created successfully')
            return redirect('type_list')
        else:
            messages.error(request, 'Type creation failed. Please correct the errors.')
    else:
        form = TypeForm()
        
    
    context = {
        'form': form
    }
    return render(request, 'type/create_type.html', context)


@login_required
@role_required('admin')
def type_list(request):
    types = Type.objects.all()
    return render(request, 'type/type_list.html', {'types': types})

@login_required
@role_required('admin')
def edit_type(request, type_id):
    type = Type.objects.get(id=type_id)
    return render(request, 'type/edit_type.html', {'type': type})

@login_required
@role_required('admin')
def process_type_update(request, type_id):
    type = Type.objects.get(id=type_id)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type updated successfully')
            return redirect('type_list')
        else:
            messages.error(request, 'Type update failed. Please correct the errors.')
            return redirect('edit_type', type_id)
    else:
        form = TypeForm(instance=type)
    return render(request, 'type/edit_type.html', {'form': form, 'type': type})

@login_required
@role_required('admin')
def delete_type(request, type_id):
    type = Type.objects.get(id=type_id)
    type.delete()
    messages.success(request, 'Type deleted successfully')
    return redirect('type_list')

