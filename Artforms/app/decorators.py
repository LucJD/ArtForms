from django.http import HttpResponse
from django.shortcuts import redirect

# unauthenticated user
# decorator called when login is checked
# if user is authenticated, redirect to home
# else, go to loginPage as normal
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("base-home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# allowed users


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = "admin"
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("logout")

        return wrapper_func

    return decorator


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login")

    return wrapper_func
