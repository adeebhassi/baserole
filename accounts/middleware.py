# accounts/middleware.py
from django.shortcuts import redirect,render
from django.http import HttpResponseForbidden

from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def role_permission(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            
            # If user is not authenticated, redirect to login page (or any other page)
            if not user.is_authenticated:
                return redirect('login')  # Replace 'login' with your login view name

            # If user has an active role and the role matches one of the allowed roles
            if user.active_role and user.active_role.lower() in [role.lower() for role in allowed_roles]:
                return view_func(request, *args, **kwargs)

            # If the user doesn't have permission, return a forbidden response
            return render(request, 'access_denied.html', status=403)
        
        return _wrapped_view
    return decorator

