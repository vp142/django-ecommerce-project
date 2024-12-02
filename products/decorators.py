from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            # Redirect non-admin users to the home page
            return redirect('home')  # Replace 'home' with the name of your home page URL
        return view_func(request, *args, **kwargs)
    return wrapper