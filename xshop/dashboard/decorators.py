from django.core.exceptions import PermissionDenied


def allowed_users(allowed_roles: list = []):
    """Limit view access based on user's role/type"""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            for role in allowed_roles:
                if role.upper() in request.user.type:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied("You're not allowed to view this page")

        return wrapper

    return decorator
