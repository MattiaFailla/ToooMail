from functools import wraps
from py_modules import backend_api


def check_is_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if backend_api.get_user_info("is_logged_in") == "true":
                return "index.html"
        except TypeError:
            return "registration.html"
        return "registration.html"

    return wrapper
