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
            prompt                    = None,
            default                   = None,
            choices                   = [],
        ):

        if not isinstance(choices, (list, tuple)):
            raise ValueError('<choices> must be a list or tuple')

        if not choices:
            raise ValueError('<choices> can not be empty')

        self.prompt = prompt
        self.default = default
        self.choices = choices
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

    def printbullet(self, idx):
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
    
    def printcheck(self, idx):
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
        self.printcheck(self.pos)
    
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
            self.print(old_pos)
            utils.moveCursorUp(1)
            self.print(self.pos)

    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.choices):
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
        utils.moveCursorDown(len(self.choices) - self.pos)
        return self.accept()

    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        raise KeyboardInterrupt

    def render(self):
        for i in range(len(self.choices)):
            self.print(i)
            utils.forceWrite('\n')
            
    def one(self):
        if self.prompt:
            utils.forceWrite(' ' * self.indent + self.prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if self.default is None:
            self.default = self.choices[0]
        elif not self.default in self.choices:
            raise ValueError('<default> should be an element of <choices>')
        self.print = self.printbullet
        self.toggle = self.togglebullet
        self.accept = self.acceptbullet
        self.max_width = len(max(self.choices, key = len)) + self.pad_right
        self.pos = self.choices.index(self.default)
        self.render()
        utils.moveCursorUp(len(self.choices) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

    def some(self):
        if self.prompt:
            utils.forceWrite(' ' * self.indent + self.prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if self.default is None:
            self.default = []
        elif self.default isinstance(self.default, (list, tuple)):
            if not all([i in self.choices for i in self.default]):
                raise ValueError('<default> must be a subset of <choices>')
        else:
            raise ValueError('<default> must be a list or tuple')
        self.print = self.printcheck
        self.toggle = self.togglecheck
        self.accept = self.acceptcheck
        self.max_width = len(max(self.choices, key = len)) + self.pad_right
        self.checked = [True if i in self.default else False for i in self.choices]
        self.pos = 0
        self.render()
        utils.moveCursorUp(len(self.choices))
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

