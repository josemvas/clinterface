import sys
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler
import readline
import re

    
@keyhandler.init
class Choose:
    def __init__(
            self, 
            shift                     = 0,
            align                     = 0,
            indent                    = 0,
            margin                    = 1,
            pad_left                  = 1,
            pad_right                 = 1,
            check                     = '>', 
            nocheck                   = None, 
            check_color               = colors.foreground['default'],
            check_on_switch           = colors.REVERSE,
            word_color                = colors.foreground['default'],
            word_on_switch            = colors.REVERSE,
            background_color          = colors.background['default'],
            background_on_switch      = colors.REVERSE,
        ):

        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch
        self.check_color = check_color
        self.check_on_switch = check_on_switch

        self.align = max(int(align), 0)
        self.shift = max(int(shift), 0)
        self.indent = max(int(indent), 0)
        self.margin = max(int(margin), 0)
        self.pad_left = max(int(pad_left), 0)
        self.pad_right = max(int(pad_right), 0)
        self.check = str(check) if check is not None else ' '
        self.nocheck = str(nocheck) if nocheck is not None else ' '

    def printrbullet(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        check_color = self.check_on_switch if idx == self.pos else self.check_color
        utils.cprint(' ' * self.pad_left, on = back_color, end = '')
        if idx == self.pos:
            utils.cprint('{}'.format(self.check) + ' ' * self.margin, check_color, back_color, end = '')
        else:
            utils.cprint('{}'.format(self.nocheck) + ' ' * self.margin, check_color, back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()
    
    def togglebullet(self):
        pass
    
    def acceptbullet(self):
        return self.choices[self.pos]
    
    def printrcheck(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        check_color = self.check_on_switch if idx == self.pos else self.check_color
        utils.cprint(' ' * self.pad_left, on = back_color, end = '')
        if self.checked[idx]:
            utils.cprint('{}'.format(self.check) + ' ' * self.margin, check_color, back_color, end = '')
        else:
            utils.cprint('{}'.format(self.nocheck) + ' ' * self.margin, check_color, back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()
    
    def togglecheck(self):
        self.checked[self.pos] = not self.checked[self.pos]
        self.printrcheck(self.pos)
    
    def acceptcheck(self):
        return [self.choices[i] for i in range(len(self.choices)) if self.checked[i]]
    
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
            self.printr(old_pos)
            utils.moveCursorUp(1)
            self.printr(self.pos)

    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.choices):
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            self.printr(old_pos)
            utils.moveCursorDown(1)
            self.printr(self.pos)

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        return self.accept()

    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        raise KeyboardInterrupt

    def render(self):
        for i in range(len(self.choices)):
            self.printr(i)
            utils.forceWrite('\n')
            
    def one(self, prompt='', choices=[], default=None):
        if not choices:
            raise ValueError('Choices can not be empty!')
        if prompt:
            utils.forceWrite(' ' * self.indent + prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if default is None:
            default = choices[0]
        else:
            if not default in choices:
                raise ValueError('<default> should be an element of <choices>!')
        self.choices = choices
        self.printr = self.printrbullet
        self.toggle = self.togglebullet
        self.accept = self.acceptbullet
        self.max_width = len(max(choices, key = len)) + self.pad_right
        self.pos = choices.index(default)
        self.render()
        utils.moveCursorUp(len(self.choices) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

    def some(self, prompt='', choices=[], default=None):
        if not choices:
            raise ValueError('Choices can not be empty!')
        if prompt:
            utils.forceWrite(' ' * self.indent + prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if default is None:
            default = []
        else:
            if not type(default).__name__ == 'list':
                raise TypeError('<default> should be a list!')
            if not all([i in choices for i in default]):
                raise ValueError('<default> should be a subset of <choices>!')
        self.choices = choices
        self.printr = self.printrcheck
        self.toggle = self.togglecheck
        self.accept = self.acceptcheck
        self.max_width = len(max(choices, key = len)) + self.pad_right
        self.checked = [ True if i in default else False for i in choices ]
        self.pos = 0
        self.render()
        utils.moveCursorUp(len(self.choices))
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret


