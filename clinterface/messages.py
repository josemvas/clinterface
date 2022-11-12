import sys
from .colors import DEFAULT, GREEN, YELLOW, RED

def join_args(f):
    def wrapper(*args, **kwargs):
        return f(' '.join(args), ', '.join('{}={}'.format(k, v) for k, v in kwargs.items()))
    return wrapper

@join_args
def success(message, details):
    if details:
        formatted_message = '{} ({})'.format(message, details)
    else:
        formatted_message = message
    print(GREEN + formatted_message + DEFAULT)

@join_args
def warning(message, details):
    if details:
        formatted_message = 'Warning: {} ({})'.format(message, details)
    else:
        formatted_message = 'Warning: {}'.format(message)
    print(YELLOW + formatted_message + DEFAULT)

@join_args
def failure(message, details):
    if details:
        formatted_message = 'Failure: {} ({})'.format(message, details)
    else:
        formatted_message = 'Failure: {}'.format(message)
    print(RED + formatted_message + DEFAULT)

@join_args
def error(message, details):
    if details:
        formatted_message = '{} ({})'.format(message, details)
    else:
        formatted_message = message
    raise SystemExit(RED + formatted_message + DEFAULT)

@join_args
def unknown_error(message):
    fcode = sys._getframe(1).f_code
    raise SystemExit(RED + '{}:{} {}'.format(fcode.co_filename, fcode.co_name, message) + DEFAULT)
