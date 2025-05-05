from functools import wraps


def authenticated_only_context(func):
    @wraps(func)
    def wrapper(request):
        if request.user.is_authenticated:
            return func(request)
        return {}  # Return empty context if not authenticated
    return wrapper