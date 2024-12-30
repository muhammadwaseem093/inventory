from django.shortcuts import render , redirect 
from django.http import Http404
from django.contrib import messages 
from .forms import ItemForm
from .models import Item 
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required

@login_required
@role_required('admin')
def create_item(request):
    return render(request, 'items/create_item.html')

@login_required
@role_required('admin')
def process_item_creation(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Item Created Successfully!')
            return redirect('item_list')
        else:
            messages.error(request, 'Item Creation Fialed. Please Correct the Error!')
    else:
        form = ItemForm()
    return render(request, 'items/create_item.html', {'form':form})

@login_required
@role_required('admin')
def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html',{'items':items})


@login_required
@role_required('admin')
def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'items/edit_item.html', {'item':item})

@login_required
@role_required('admin')
def process_item_edit(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method =='POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item UPdated Successfully!')
            return redirect('item_list')
        else:
            messages.error(request, 'Item Update Failed!')
            return redirect('edit_item', item_id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/edit_item.html', {'form':form , 'item':item})


@login_required
@role_required('admin')  # Ensure only admin can delete
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise Http404("Item not found")

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('item_list') 

    return render(request, 'items/delete_item.html', {'item': item})

