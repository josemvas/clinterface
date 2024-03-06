import sys
from string import Template
from .colors import DEFAULT, GREEN, YELLOW, RED

def success(message, details=None):
    if details:
        print(GREEN + "{} ({})".format(message, details) + DEFAULT)
    else:
        print(GREEN + message + DEFAULT)

def failure(message, details=None):
    if details:
        print(RED + "{} ({})".format(message, details) + DEFAULT)
    else:
        print(RED + message + DEFAULT)

def warning(message, details=None):
    if details:
        print(YELLOW + "Warning: {} ({})".format(message, details) + DEFAULT)
    else:
        print(YELLOW + 'Warning: {}'.format(message) + DEFAULT)

def error(message, details=None):
    if details:
        raise SystemExit(RED + "Error: {} ({})".format(message, details) + DEFAULT)
    else:
        raise SystemExit(RED + 'Error: {}'.format(message) + DEFAULT)

def unknown_error(message):
    fcode = sys._getframe(1).f_code
    raise SystemExit(RED + '{}:{} {}'.format(fcode.co_filename, fcode.co_name, message) + DEFAULT)
