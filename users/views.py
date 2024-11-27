from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from .decorators import role_required
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on role
                if user.is_admin:
                    return redirect('/admin/')  # Redirect admins to the admin panel
                elif user.is_seller:
                    return redirect('products:seller_dashboard')  # Redirect sellers to their dashboard
                else:
                    return redirect('products:all_products')  # Redirect regular users to all products
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('users:login')

# @login_required
# def user_dashboard(request):
#     """Dashboard for regular users."""
#     return render(request, 'users/user_dashboard.html')
