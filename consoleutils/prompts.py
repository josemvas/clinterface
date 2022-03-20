import os
import sys
import readline
from glob import glob
from collections import OrderedDict
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler
from . import messages


def check_options(options):
    if isinstance(options, (list, tuple)):
        if not options:
            raise ValueError('Options can not be empty')
    else:
        raise ValueError('Options must be a list or tuple')

class Completer:
    def __init__(self, delims=' \t\n'):
        readline.set_completer_delims(delims)
        readline.parse_and_bind('tab: complete')
        self.message = None
        self.options = None
        self.default = None
    def file_path_completer(self):
        def completer(text, n):
            return [i + '/' if os.path.isdir(i) else i + ' ' for i in glob(os.path.expanduser(text) + '*')][n]
        return completer
    def directory_path_completer(self):
        def completer(text, n):
            return [i + '/' for i in glob(os.path.expanduser(text) + '*') if os.path.isdir(i)][n]
        return completer
    def choice_completer(self, max_completions=None):
        def completer(text, n):
            completions = readline.get_line_buffer().split()[:-1]
            if not max_completions or len(completions) < max_completions:
                return [i + ' ' for i in self.autocomplete if i.startswith(text) and i not in completions][n]
        return completer
    def file_path(self):
        while True:
            readline.set_completer(self.file_path_completer())
            print(self.message + ':')
            answer = os.path.normpath(input(''))
            if answer:
                if os.path.isfile(answer):
                    return answer
                elif os.path.exists(answer):
                    print('Path exists but is not a file, try again')
                else:
                    print('File does not exist, try again')
    def directory_path(self):
        while True:
            readline.set_completer(self.directory_path_completer())
            print(self.message + ':')
            answer = os.path.normpath(input(''))
            if answer:
                if os.path.isdir(answer):
                    return answer
                elif os.path.exists(answer):
                    print('Path exists but is not a directory, try again')
                else:
                    print('Directory does not exist, try again')
    def single_choice(self):
        check_options(self.options)
        self.autocomplete = self.options
        readline.set_completer(self.choice_completer(1))
        print(self.message)
        for option in self.options:
            print(' '*2 + option);
        while True:
            option = input('Single choice (press TAB to autocomplete): ').strip()
            if option in self.options:
                return option
            else:
                messages.warning('Invalid choice, try again')
    def multiple_choice(self):
        check_options(self.options)
        readline.set_completer(self.choice_completer(len(self.options)))
        self.autocomplete = self.options
        print(self.message)
        for option in self.options:
            print(' '*2 + option);
        while True:
            option = input('Multiple choice (press TAB to autocomplete): ').strip().split()
            if set(option) <= set(self.options):
                return option
            else:
                messages.warning('Invalid choice, try again')
    def binary_choice(self):
        check_options(self.options[True])
        check_options(self.options[False])
        self.autocomplete = self.options[True] + self.options[False]
        while True:
            readline.set_completer(self.choice_completer(1))
            print(self.message, end='')
            answer = input(' ').strip()
            if answer:
                if answer in self.options[True]:
                    return True
                elif answer in self.options[False]:
                    return False
                else:
                    print('Invalid choice, type {} to accept or {} to reject'.format('/'.join(self.options[True]), '/'.join(self.options[False])))
            elif self.default in (True, False):
                return self.default

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
        self.message = None
        self.options = None
        self.default = None
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
        return self.options[self.pos]
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
        return [self.options[i] for i in range(len(self.options)) if self.checked[i]]
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
        check_options(self.options)
        if self.default is None:
            self.pos = 0
        else:
            try:
                self.pos = self.options.index(self.default)
            except ValueError:
                raise ValueError('default must be an element of options') from None
        self.print = self.printradio
        self.toggle = self.toggleradio
        self.accept = self.acceptradio
        self.max_width = len(max(self.options, key = len)) + self.pad_right
        return self.render()
    def multiple_choice(self):
        check_options(self.options)
        if self.default is None:
            self.checked = [False for i in self.options]
        elif isinstance(self.default, (list, tuple)):
            if any([i not in self.options for i in self.default]):
                raise ValueError('default list must be a subset of options')
            self.checked = [True if i in self.default else False for i in self.options]
        else:
            raise ValueError('default must be a list or tuple')
        self.print = self.printcheck
        self.toggle = self.togglecheck
        self.accept = self.acceptcheck
        self.max_width = len(max(self.options, key = len)) + self.pad_right
        self.pos = 0
        return self.render()

