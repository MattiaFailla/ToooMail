from functools import wraps
from py_modules import backend_api


def check_is_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        status = {
            0: "registration.html",
            1: "index.html",
        }

        try:
            return status[backend_api.get_user_info("is_logged_in")]
        except TypeError:
            return "registration.html"
            
    return wrapper
