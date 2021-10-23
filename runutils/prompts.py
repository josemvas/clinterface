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

def check_label(label):
    if label is None:
        raise ValueError('label must be defined')
    elif isinstance(label, str):
        if not label:
            raise ValueError('label string can not be null')
    else:
        raise ValueError('label must be a string')

def check_optionlist(options):
    if options is None:
        raise ValueError('options must be defined')
    elif isinstance(options, (list, tuple)):
        if not options:
            raise ValueError('options list can not be empty')
    else:
        raise ValueError('options must be a list or tuple')

def check_optiondict(options):
    if options is None:
        raise ValueError('options must be defined')
    elif isinstance(options, (dict, OrderedDict)):
        if not options:
            raise ValueError('options dict can not be empty')
    else:
        raise ValueError('options must be a dict or ordered dict')

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
        self.label = None
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
        utils.forceWrite(' ' * self.indent + self.label + '\n')
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
    def singlechoice(self):
        check_label(self.label)
        check_optionlist(self.options)
        if self.default is None:
            self.pos = 0
        elif isinstance(default, str):
            if default:
                try:
                    self.pos = self.options.index(self.default)
                except ValueError:
                    raise ValueError('default must be an element of options') from None
            else:
                raise ValueError('default string can not be null')
        else:
            raise ValueError('default must be a string')
        self.print = self.printradio
        self.toggle = self.toggleradio
        self.accept = self.acceptradio
        self.max_width = len(max(self.options, key = len)) + self.pad_right
        return self.render()
    def multiplechoice(self):
        check_label(self.label)
        check_optionlist(self.options)
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

class Completer(object):
    def __init__(self, delims=' \t\n'):
        readline.set_completer_delims(delims)
        readline.parse_and_bind('tab: complete')
        self.label = None
        self.options = None
        self.default = None
    def path_completer(self):
        def completer(text, n):
            return [i + '/' if os.path.isdir(i) else i + ' ' for i in glob(os.path.expanduser(text) + '*')][n]
        return completer
    def choice_completer(self, max_completions=None):
        def completer(text, n):
            completions = readline.get_line_buffer().split()[:-1]
            if not max_completions or len(completions) < max_completions:
                return [i + ' ' for i in self.options if i.startswith(text) and i not in completions][n]
        return completer
    def path(self, check=lambda _:True):
        check_label(self.label)
        while True:
            readline.set_completer(self.path_completer())
            print(self.label + ': ', end='')
            answer = input('').strip()
            if answer:
                if check(answer):
                    return answer
                else:
                    print('Por favor indique una ruta válida')
            else:
                print('Por favor indique una ruta')
    def singlechoice(self):
        check_label(self.label)
        check_optionlist(self.options)
        readline.set_completer(self.choice_completer(1))
        print(self.label)
        for option in self.options:
            print(' '*2 + option);
        while True:
            option = input('Elección (TAB para autocompletar): ').strip()
            if option in self.options:
                return option
            else:
                messages.warning('Elección inválida, intente de nuevo')
    def multiplechoice(self):
        check_label(self.label)
        check_optionlist(self.options)
        readline.set_completer(self.choice_completer(len(self.options)))
        print(self.label)
        for option in self.options:
            print(' '*2 + option);
        while True:
            option = input('Selección (TAB para autocompletar): ').strip().split()
            if set(option) <= set(self.options):
                return option
            else:
                messages.warning('Selección inválida, intente de nuevo')
    def binarychoice(self):
        check_label(self.label)
        check_optiondict(self.options)
        while True:
            readline.set_completer(self.choice_completer(1))
            print(self.label, end='')
            answer = input(' ').strip()
            if answer:
                if answer == self.options[True]:
                    return True
                elif answer == self.options[False]:
                    return False
                else:
                    print('Por favor responda "{}" para confirmar o "{}" para cancelar:'.format(self.options[True], self.options[False]))
            elif self.default in (True, False):
                return self.default

