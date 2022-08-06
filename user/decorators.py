from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import redirect


def allowed_groups(allowed_groups=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Check if the user is in a group
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            # Check if the authenticated users' group is in allowed to view the page/data
            if group in allowed_groups:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED, )

        return wrapper

    return decorator
