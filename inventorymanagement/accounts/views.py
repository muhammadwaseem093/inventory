from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, AuthenticationForm
from utils.decorators import role_required
from supplier.models import Supplier
from vendor.models import Vendor
from items.models import Item
from igp.models import IGP
from ogp.models import OGP
# from ogp.models import OGP
from accounts.utils import log_activity
from datetime import datetime, timedelta

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role.name == 'super_admin':
                    return redirect('super_admin_dashboard')
                elif user.role.name == 'admin':
                    return redirect('admin_dashboard')
                elif user.role.name == 'staff':
                    return redirect('staff_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')




# super admin Dashboard
@login_required
@role_required('super_admin')
def super_admin_dashboard(request):
    activity_logs = ActivityLog.objects.order_by('-created_at')[:50]
    return render(request, 'dashboards/super_admin.html', {'activity_logs':activity_logs})

#admin dashboard
@login_required
@role_required('admin')
def admin_dashboard(request):
    supplier_count = Supplier.objects.count()
    vendor_count= Vendor.objects.count()
    igp_count = IGP.objects.count()
    # ogp_count = OGP.objects.count()
    return render(
        request,
        'dashboards/admin.html',
        {'supplier_count':supplier_count,
        'vendor_count':vendor_count,
        'igp_count':igp_count,
        # 'ogp_count':ogp_count
        })

# clerk Dashboard
@login_required
@role_required('staff')
def staff_dashboard(request):
    supplier_count = Supplier.objects.count()
    vendor_count= Vendor.objects.count()
    items_count=Item.objects.count()
    igp_count = IGP.objects.count()
    ogp_count=OGP.objects.count()
    
    # Trends Data for chart
    last_month = datetime.now() - timedelta(days=30)
    igps = IGP.objects.filter(date__gte=last_month)
    ogps= OGP.objects.filter(date__gte=last_month)
    trends_igp_lbls = [igp.date.strftime('%Y-%m-%d') for igp in igps]
    trends_ogp_lbls = [ogp.date.strftime('%y-%m-%d') for ogp in ogps]
    trends_igp = [1 for igp in igps]
    trends_ogp = [1 for ogp in ogps]
    
    supplier_igp_count = Supplier.objects.count()
    vendor_ogp_count = Vendor.objects.count()
    
    context = {
        'supplier_count': supplier_count,
        'vendor_count': vendor_count,
        'items_count': items_count,
        'igp_count': igp_count,
        'trends_igp_lbls': trends_igp_lbls,
        'trends_ogp_lbls':trends_ogp_lbls,
        'trends_igp': trends_igp,
        'trends_ogp': trends_ogp,
        'supplier_igp_count': supplier_igp_count,
        'vendor_ogp_count': vendor_ogp_count,
    }
    return render(request, 'dashboards/staff.html', context)



