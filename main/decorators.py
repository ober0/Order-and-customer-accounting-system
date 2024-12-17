from functools import wraps
from urllib.parse import urlencode

from django.shortcuts import redirect


def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            current_url = request.get_full_path()
            query_string = urlencode({'next': current_url})
            login_url = f"/login/?{query_string}"
            return redirect(login_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view