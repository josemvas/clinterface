__all__ = (
    'complete_filepath',
    'complete_dirpath',
    'complete_binary_choice',
    'complete_choices',
)

import readline
from sys import stdout
from string import whitespace
from os import path, scandir
from .colors import YELLOW
from .utils import cprint

def make_split_escaped(delimiters):
    def split_escaped(text):
        result = []
        current_substring = ""
        escaped = False
        for char in text:
            if char == '\\':
                escaped = True
            elif char in delimiters:
                if escaped:
                    current_substring += char
                    escaped = False
                elif current_substring:  # Only add non-empty substrings
                    result.append(current_substring)
                    current_substring = ""
            else:
                if escaped:
                    current_substring += '\\' + char
                    escaped = False
                else:
                    current_substring += char
        if escaped:
            current_substring += '\\'
        return result, current_substring
    return split_escaped

def make_escaped_string(delimiters):
    def escaped_string(path):
        escape_map = {ord(char): f"\\{char}" for char in delimiters}
        return str(path).translate(str.maketrans(escape_map))
    return escaped_string

split_escaped = make_split_escaped(whitespace)
escaped_string = make_escaped_string(whitespace)
readline.set_completer_delims(whitespace)
readline.parse_and_bind('tab: complete')

class FilePathCompleter:
    def __init__(self):
        self.matches = []
    def __call__(self, input_text, state):
        line_buffer = readline.get_line_buffer()
        completed, completing = split_escaped(line_buffer)
        if not completed:
            if state == 0:
                input_path = path.expanduser(completing)
                if path.isdir(input_path) and completing.endswith('/'):
                    self.matches = list(scandir(input_path))
                else:
                    parent_dir = path.dirname(input_path) or '.'
                    basename = path.basename(input_path)
                    self.matches = [entry for entry in scandir(parent_dir) if entry.name.startswith(basename)]
            if state < len(self.matches):
                start = len(completing) - len(input_text)
                entry = self.matches[state]
                if entry.is_dir():
                    return escaped_string(entry.path[start:]) + '/'
                else:
                    return escaped_string(entry.path[start:]) + ' '
        return None

class DirPathCompleter:
    def __init__(self):
        self.matches = []
    def __call__(self, input_text, state):
        line_buffer = readline.get_line_buffer()
        completed, completing = split_escaped(line_buffer)
        if not completed:
            if state == 0:
                input_path = path.expanduser(completing)
                if path.isdir(input_path) and completing.endswith('/'):
                    self.matches = [entry for entry in scandir(input_path) if entry.is_dir()]
                else:
                    parent_dir = path.dirname(input_path) or '.'
                    basename = path.basename(input_path)
                    self.matches = [entry for entry in scandir(parent_dir) if entry.name.startswith(basename) and entry.is_dir()]
            if state < len(self.matches):
                start = len(completing) - len(input_text)
                entry = self.matches[state]
                return escaped_string(entry.path[start:]) + '/'
        return None

def make_option_completer(options, max_completions=None):
    def completer(input_text, state):
        completed, completing = split_escaped(readline.get_line_buffer())
        if max_completions is None or len(completed) < max_completions:
            return [escaped_string(x) + ' ' for x in options if x.startswith(input_text) and x not in completed][state]
        return None
    return completer

def complete_filepath(prompt):
    completer = FilePathCompleter()
    readline.set_completer(completer)
    while True:
        stdout.write(prompt)
        completed, completing = split_escaped(input('\n'))
        if completing:
            completed.append(completing)
        if completed:
            if len(completed) == 1:
                return completed[0]
            else:
                cprint(f'Type only one path', YELLOW)

def complete_dirpath(prompt):
    completer = DirPathCompleter()
    readline.set_completer(completer)
    while True:
        stdout.write(prompt)
        completed, completing = split_escaped(input('\n'))
        if completing:
            completed.append(completing)
        if completed:
            if len(completed) == 1:
                return completed[0]
            else:
                cprint(f'Type only one path', YELLOW)

def complete_binary_choice(prompt, truthy_options, falsy_options, default=None):
    if default not in (None, True, False):
        raise ValueError('default must be True or False') from None
    truthy_options_help = '/'.join(truthy_options)
    falsy_options_help = '/'.join(falsy_options)
    completer = make_option_completer(truthy_options + falsy_options, max_completions=1)
    readline.set_completer(completer)
    while True:
        stdout.write(prompt)
        completed, completing = split_escaped(input(' '))
        if completing:
            completed.append(completing)
        if not completed:
            if default is not None:
                return default
            cprint(f'Type {truthy_options_help} to accept or {falsy_options_help} to reject', YELLOW)
        elif len(completed) > 1:
            cprint('Type only one choice', YELLOW)
        elif completed[0] in truthy_options:
            return True
        elif completed[0] in falsy_options:
            return False
        else:
            cprint(f'Type "{truthy_options_help}" to accept or "{falsy_options_help}" to reject', YELLOW)

def complete_choices(prompt, options, num_choices=None):
    """Complete multiple choices from a list and return their indices."""
    if num_choices is not None and num_choices > len(options):
        raise ValueError(f"num_choices ({num_choices}) cannot exceed options count")
    completer = make_option_completer(options, max_completions=num_choices)
    readline.set_completer(completer)
    cprint('Available options:')
    for option in options:
        cprint(' '*2 + option)
    while True:
        stdout.write(prompt)
        completed, completing = split_escaped(input('\n'))
        if completing:
            completed.append(completing)
        if completed:
            if num_choices is None or len(completed) == num_choices:
                try:
                    return completed
                except KeyError:
                    cprint(f'Type only valid choices', YELLOW)
            else:
                cprint(f'Type exactly {num_choices} choice(s)', YELLOW)
