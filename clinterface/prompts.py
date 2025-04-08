import os
import sys
import readline
from pathlib import Path
from collections.abc import Iterable, Mapping
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler

def new_path_completer():
    matches = {}
    def completer(input_text, state):
        input_path = Path(input_text).expanduser().resolve()
        if input_text not in matches:
            if input_path.is_dir() and input_text.endswith('/'):
                parent_dir = input_path
                pattern = '*'
            else:
                parent_dir = input_path.parent
                pattern = input_path.name + '*'
            matches[input_text] = [str(i) + '/' if i.is_dir() else str(i) + ' ' for i in parent_dir.glob(pattern)]
        return matches[input_text][state]
    return completer

def new_singlechoice_completer(completion_words):
    matches = {}
    def completer(input_text, state):
        if input_text not in matches:
            matches[input_text] = [i + ' ' for i in completion_words if i.startswith(input_text)]
        return matches[input_text][state]
    return completer

def new_multiplechoice_completer(completion_words, max_completions=None):
    matches = {}
    def completer(input_text, state):
        completions = readline.get_line_buffer().split('&')[:-1]
        if max_completions is None or len(completions) < max_completions:
            if input_text not in matches:
                matches[input_text] = [i + ' & ' for i in completion_words if i.startswith(input_text) and i not in completions.strip()]
            return matches[input_text][state]
    return completer

class Completer:
    def file_path(self, prompt):
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        path_completer = new_path_completer()
        readline.set_completer(path_completer)
        while True:
            print(prompt)
            path = input('').rstrip()
            if path:
                if os.path.isfile(path):
                    return os.path.normpath(path)
                elif os.path.exists(path):
                    print('Path "{}" is not a file, try again'.format(path))
                else:
                    print('File "{}" does not exist, try again'.format(path))
    def directory_path(self, prompt):
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        path_completer = new_path_completer()
        readline.set_completer(path_completer)
        while True:
            print(prompt)
            path = input('').rstrip()
            if path:
                if os.path.isdir(path):
                    return os.path.normpath(path)
                elif os.path.exists(path):
                    print('Path "{}" is not a directory, try again'.format(path))
                else:
                    print('Directory "{}" does not exist, try again'.format(path))
    def binary_choice(self, prompt, truthy_options, falsy_options, default=None):
        if all(default is x for x in (None, True, False)):
            raise ValueError('default must be None, True or False') from None
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        singlechoice_completer = new_singlechoice_completer(truthy_options + falsy_options)
        readline.set_completer(singlechoice_completer)
        while True:
            print(prompt, end='')
            choice = input(' ').rstrip()
            if choice:
                if choice in truthy_options:
                    return True
                elif choice in falsy_options:
                    return False
                else:
                    print('Invalid choice, type {} to accept or {} to reject'.format('/'.join(truthy_options), '/'.join(falsy_options)))
            elif default is not None:
                return default
    def single_choice(self, prompt, options, optkeys):
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        singlechoice_completer = new_singlechoice_completer(options)
        readline.set_completer(singlechoice_completer)
        print('Options:')
        for option in options:
            print(' '*2 + option)
        print(message)
        choice = input('').rstrip()
        while True:
            if choice not in options:
                print('Invalid choice, try again')
            else:
                return optkeys[soptions.index(choice)]
    def multiple_choices(self, prompt, options, optkeys):
        readline.set_completer_delims(' \t\n')
        readline.parse_and_bind('tab: complete')
        multiplechoice_completer = new_multiplechoice_completer(options)
        readline.set_completer(multiplechoice_completer)
        print('Options:')
        for option in options:
            print(' '*2 + option)
        print(message)
        choices = input('').split('&')
        while True:
            if any([i.strip() not in options for i in choices]):
                print('Invalid choices, try again')
            else:
                return [optkeys[options.index(i.strip())] for i in choices]

@keyhandler.init
class Selector:
    def __init__(
            self, 
            shift                     = 0,
            align                     = 0,
            indent                    = 0,
            margin                    = 1,
            pad_left                  = 1,
            pad_right                 = 1,
            radiobullet               = '>',
            checkbullet               = 'X',
            bullet_color              = colors.foreground['default'],
            bullet_on_switch          = colors.REVERSE,
            word_color                = colors.foreground['default'],
            word_on_switch            = colors.REVERSE,
            background_color          = colors.background['default'],
            background_on_switch      = colors.REVERSE,
        ):
        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch
        self.bullet_color = bullet_color
        self.bullet_on_switch = bullet_on_switch
        self.align = max(int(align), 0)
        self.shift = max(int(shift), 0)
        self.indent = max(int(indent), 0)
        self.margin = max(int(margin), 0)
        self.pad_left = max(int(pad_left), 0)
        self.pad_right = max(int(pad_right), 0)
        self.radiobullet = ' ' if radiobullet is None else radiobullet
        self.checkbullet = ' ' if checkbullet is None else checkbullet
        self.prompt = None
        self.options = None
        self.optkeys = None
        self.opt_values = None
        self.pos = 0
        self.checked = None
    def printradio(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        bullet_color = self.bullet_on_switch if idx == self.pos else self.bullet_color
        utils.cprint(' ' * self.pad_left, on = back_color, end = '')
        if idx == self.pos:
            utils.cprint(self.radiobullet + ' ' * self.margin, bullet_color, back_color, end = '')
        else:
            utils.cprint(' ' * (len(self.radiobullet) + self.margin), bullet_color, back_color, end = '')
        utils.cprint(self.opt_values[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.opt_values[idx])), on = back_color, end = '')
        utils.moveCursorHead()
    def toggleradio(self):
        pass
    def acceptradio(self):
        return self.optkeys[self.pos]
    def printcheck(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        bullet_color = self.bullet_on_switch if idx == self.pos else self.bullet_color
        utils.cprint(' ' * self.pad_left, on = back_color, end = '')
        if self.checked[idx]:
            utils.cprint(self.checkbullet + ' ' * self.margin, bullet_color, back_color, end = '')
        else:
            utils.cprint(' ' * (len(self.checkbullet) + self.margin), bullet_color, back_color, end = '')
        utils.cprint(self.opt_values[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.opt_values[idx])), on = back_color, end = '')
        utils.moveCursorHead()
    def togglecheck(self):
        self.checked[self.pos] = not self.checked[self.pos]
        self.printcheck(self.pos)
    def acceptcheck(self):
        return [self.optkeys[i] for i, x in enumerate(self.checked) if x]
    @keyhandler.register(SPACE_CHAR)
    def toggle(self):
        self.toggle()
    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        if self.pos - 1 < 0:
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos -= 1
            self.print(old_pos)
            utils.moveCursorUp(1)
            self.print(self.pos)
    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.optkeys):
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            self.print(old_pos)
            utils.moveCursorDown(1)
            self.print(self.pos)
    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        utils.moveCursorDown(len(self.optkeys) - self.pos)
        return self.accept()
    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.optkeys) - self.pos)
        raise KeyboardInterrupt
    def render(self):
        if self.prompt is None:
            raise ValueError('Message is not set')
        if self.options is None:
            raise ValueError('Options are not set')
        utils.forceWrite(' ' * self.indent + self.prompt + '\n')
        utils.forceWrite('\n' * self.shift)
        for i in range(len(self.optkeys)):
            self.print(i)
            utils.forceWrite('\n')
        utils.moveCursorUp(len(self.optkeys) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret
    def single_choice(self, prompt, options, default=None):
        """
        Display a selector for choosing a single option
        Args:
            prompt: The prompt to display
            options: A dictionary mapping option keys to display values, or an iterable of options
            default: The default option key to select (must be one of the option keys)
        Returns:
            The selected option key
        """
        self.prompt = prompt
        # Convert options to a dictionary if it's not already
        if not isinstance(options, Mapping):
            self.options = {item: item for item in options}
        else:
            self.options = options
        # Get the sorted keys and values for display
        self.optkeys = list(self.options.keys())
        self.opt_values = list(self.options.values())
        # Set default position
        self.pos = 0
        if default is not None:
            if default not in self.optkeys:
                raise ValueError('default must be an element of option keys')
            self.pos = self.optkeys.index(default)
        # Set up rendering functions
        self.print = self.printradio
        self.toggle = self.toggleradio
        self.accept = self.acceptradio
        self.max_width = len(max(self.opt_values, key=len)) + self.pad_right
        return self.render()
    def multiple_choices(self, prompt, options, defaults=None):
        """
        Display a selector for choosing multiple options
        Args:
            prompt: The prompt to display
            options: A dictionary mapping option keys to display values, or an iterable of options
            defaults: A list of default option keys to select (must be a subset of option keys)
        Returns:
            A list of selected option keys
        """
        self.prompt = prompt
        # Convert options to a dictionary if it's not already
        if not isinstance(options, Mapping):
            self.options = {item: item for item in options}
        else:
            self.options = options
        # Get the sorted keys and values for display
        self.optkeys = list(self.options.keys())
        self.opt_values = list(self.options.values())
        # Initialize checked status
        self.checked = [False] * len(self.optkeys)
        # Set defaults
        if defaults is not None:
            if isinstance(defaults, (list, tuple)):
                if any(i not in self.optkeys for i in defaults):
                    raise ValueError('defaults list must be a subset of option keys')
                self.checked = [True if i in defaults else False for i in self.optkeys]
            else:
                raise ValueError('defaults must be a list or tuple')
        # Set default position
        self.pos = 0
        # Set up rendering functions
        self.print = self.printcheck
        self.toggle = self.togglecheck
        self.accept = self.acceptcheck
        self.max_width = len(max(self.opt_values, key=len)) + self.pad_right
        return self.render()
