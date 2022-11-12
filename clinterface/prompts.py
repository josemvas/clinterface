import os
import sys
import readline
from glob import glob
from collections.abc import Iterable, Mapping
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler
from . import messages

def path_completer():
    def f(text, n):
        return [i + '/' if os.path.isdir(i) else i + ' ' for i in glob(os.path.expanduser(text) + '*')][n]
    return f

def single_choice_completer(completion_words):
    def f(text, n):
        return [i + ' ' for i in completion_words if i.startswith(text)][n]
    return f

def multiple_choice_completer(completion_words, max_completions=None):
    def f(text, n):
        completions = readline.get_line_buffer().split('&')[:-1]
        if max_completions is None or len(completions) < max_completions:
            return [i + ' & ' for i in completion_words if i.startswith(text) and i not in completions.strip()][n]
    return f

class Prompt:
    def __init__(self):
        self.message = None
        self.optkeys = None
        self.options = None
        self.truthy_options = None
        self.falsy_options = None
        self.default = None
    def set_message(self, message):
        if isinstance(message, str):
            self.message = message
        else:
            raise TypeError('Message must be a string')
    def set_binary_default(self, default):
        if default in (True, False):
            self.default = default
        else:
            raise ValueError('default must be True or False') from None
    def set_single_default(self, default):
        if self.options is None:
            raise ValueError('Options must be set before defaults') from None
        if default not in self.optkeys:
            raise ValueError('default must be an element of option keys') from None
        self.pos = self.optkeys.index(default)
    def set_multiple_defaults(self, defaults):
        if self.options is None:
            raise ValueError('Options must be set before defaults') from None
        if isinstance(defaults, (list, tuple)):
            if any([i not in self.optkeys for i in defaults]):
                raise ValueError('default list must be a subset of option keys')
            self.checked = [True if i in defaults else False for i in self.optkeys]
        else:
            raise ValueError('default must be a list or tuple')
    def set_options(self, options):
        if isinstance(options, Iterable):
            if not options:
                raise ValueError('Options can not be empty')
            self.optkeys = []
            self.options = []
            if isinstance(options, Mapping):
                for key, value in options.items():
                    self.optkeys.append(key)
                    self.options.append(value)
            else:
                for item in options:
                    self.optkeys.append(item)
                    self.options.append(item)
        else:
            raise TypeError('Options must be a list, tuple or dict')
        self.pos = 0
        self.checked = [False]*len(options)
    def set_truthy_options(self, options):
        if isinstance(options, (list, tuple)):
            if not options:
                raise ValueError('Options can not be empty')
            self.truthy_options = options
        else:
            raise TypeError('Options must be a list or tuple')
    def set_falsy_options(self, options):
        if isinstance(options, (list, tuple)):
            if not options:
                raise ValueError('Options can not be empty')
            self.falsy_options = options
        else:
            raise TypeError('Options must be a list or tuple')

class Completer(Prompt):
    def file_path(self):
        if self.message is None:
            raise ValueError('Message is not set')
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(path_completer())
        while True:
            print(self.message + ':')
            path = input('').rstrip()
            if path:
                if os.path.isfile(path):
                    return os.path.normpath(path)
                elif os.path.exists(path):
                    print('Path "{}" is not a file, try again'.format(path))
                else:
                    print('File "{}" does not exist, try again'.format(path))
    def directory_path(self):
        if self.message is None:
            raise ValueError('Message is not set')
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(path_completer())
        while True:
            print(self.message + ':')
            path = input('').rstrip()
            if path:
                if os.path.isdir(path):
                    return os.path.normpath(path)
                elif os.path.exists(path):
                    print('Path "{}" is not a directory, try again'.format(path))
                else:
                    print('Directory "{}" does not exist, try again'.format(path))
    def binary_choice(self):
        if self.message is None:
            raise ValueError('Message is not set')
        if self.truthy_options is None:
            raise ValueError('Truthy options are not set')
        if self.truthy_options is None:
            raise ValueError('Falsy options are not set')
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(single_choice_completer(self.truthy_options + self.falsy_options))
        while True:
            print(self.message, end='')
            choice = input(' ').rstrip()
            if choice:
                if choice in self.truthy_options:
                    return True
                elif choice in self.falsy_options:
                    return False
                else:
                    print('Invalid choice, type {} to accept or {} to reject'.format(
                        '/'.join(self.truthy_options), '/'.join(self.falsy_options)))
            elif self.default is not None:
                return self.default
    def single_choice(self):
        if self.message is None:
            raise ValueError('Message is not set')
        if self.options is None:
            raise ValueError('Options are not set')
        readline.set_completer_delims('\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(single_choice_completer(self.options))
        print(self.message)
        for option in self.options:
            print(' '*2 + option)
        message = 'Single choice (press TAB to autocomplete): '
        choice = input(message).rstrip()
        while True:
            if choice not in self.options:
                messages.warning('Invalid choice, try again')
            else:
                return self.optkeys[self.options.index(choice)]
    def multiple_choices(self):
        if self.message is None:
            raise ValueError('Message is not set')
        if self.options is None:
            raise ValueError('Options are not set')
        readline.set_completer_delims(' \t\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(multiple_choice_completer(self.options))
        print(self.message)
        for option in self.options:
            print(' '*2 + option)
        message = 'Multiple choice (press TAB to autocomplete): '
        choices = input(message).split('&')
        while True:
            if any([i.strip() not in self.options for i in choices]):
                messages.warning('Invalid choices, try again')
            else:
                return [self.optkeys[self.options.index(i.strip())] for i in choices]

@keyhandler.init
class Selector(Prompt):
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
        self.message = None
        self.optkeys = None
        self.options = None
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
        utils.cprint(self.options[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.options[idx])), on = back_color, end = '')
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
        utils.cprint(self.options[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.options[idx])), on = back_color, end = '')
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
        if self.pos + 1 >= len(self.options):
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
        utils.moveCursorDown(len(self.options) - self.pos)
        return self.accept()
    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.options) - self.pos)
        raise KeyboardInterrupt
    def render(self):
        if self.message is None:
            raise ValueError('Message is not set')
        if self.options is None:
            raise ValueError('Options are not set')
        utils.forceWrite(' ' * self.indent + self.message + '\n')
        utils.forceWrite('\n' * self.shift)
        for i in range(len(self.options)):
            self.print(i)
            utils.forceWrite('\n')
        utils.moveCursorUp(len(self.options) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret
    def single_choice(self):
        self.print = self.printradio
        self.toggle = self.toggleradio
        self.accept = self.acceptradio
        self.max_width = len(max(self.options, key = len)) + self.pad_right
        return self.render()
    def multiple_choices(self):
        self.print = self.printcheck
        self.toggle = self.togglecheck
        self.accept = self.acceptcheck
        self.max_width = len(max(self.options, key = len)) + self.pad_right
        return self.render()
