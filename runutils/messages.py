# -*- coding: utf-8 -*-
import sys
from . import colors

def success(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    print(colors.foreground['green'] + message + colors.foreground['default'])

def warning(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    print(colors.foreground['yellow'] + message + colors.foreground['default'])

def failure(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    print(colors.foreground['red'] + message + colors.foreground['default'])

def error(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    sys.exit(colors.foreground['red'] + message + colors.foreground['default'])

def unknown_error(message):
    fcode = sys._getframe(1).f_code
    sys.exit(colors.foreground['red'] + '{}:{} {}'.format(fcode.co_filename, fcode.co_name, message) + colors.foreground['default'])

