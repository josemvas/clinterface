__all__ = (
    'print_success',
    'print_failure',
    'print_warning',
    'print_error_and_exit',
)

from .colors import GREEN, YELLOW, RED
from .utils import cprint

# Create a dict subclass that tracks accessed keys and returns 
# the format key when key is missing
class TrackingDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.used_keys = set()
    def __getitem__(self, key):
        self.used_keys.add(key)
        if key not in self:
            return '*****'
        return super().__getitem__(key)

def format_message(func):
    def wrapper(message, **kwargs):
        tracking_dict = TrackingDict(kwargs)
        formatted_message = message.format_map(tracking_dict)
        # Get unused kwargs
        unused_kwargs = {k: v for k, v in kwargs.items() 
                        if k not in tracking_dict.used_keys}
        # If there are unused kwargs, append them to the message
        if unused_kwargs:
            unused_str = ", ".join(f"{k}={v}" for k, v in unused_kwargs.items())
            formatted_message = f"{formatted_message} ({unused_str})"
        return func(formatted_message)
    return wrapper

@format_message
def print_success(message):
    cprint(message, GREEN)

@format_message
def print_failure(message):
    cprint(message, RED)

@format_message
def print_warning(message):
    cprint(f'WARNING: {message}', YELLOW)

@format_message
def print_error_and_exit(message):
    cprint(f'ERROR: {message}', RED)
    raise SystemExit
