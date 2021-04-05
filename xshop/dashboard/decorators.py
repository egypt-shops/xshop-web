from django.core.exceptions import PermissionDenied


def allowed_groups(groups: list = []):
    """Limit view access based on user's role/type"""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            for role in groups:
                if request.user.groups.filter(name=role).exists():
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied("You're not allowed to view this page")

        return wrapper

    return decorator
