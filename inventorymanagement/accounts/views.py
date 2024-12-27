from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, AuthenticationForm
from utils.decorators import role_required

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
    return redirect('login')




# super admin Dashboard
@login_required
@role_required('super_admin')
def super_admin_dashboard(request):
    return render(request, 'dashboards/super_admin.html')

#admin dashboard
@login_required
@role_required('admin')
def admin_dashboard(request):
    return render(request, 'dashboards/admin.html')

# clerk Dashboard
@login_required
@role_required('staff')
def staff_dashboard(request):
    return render(request, 'dashboards/staff.html')