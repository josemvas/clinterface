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
        self.choices = None
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
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()
    
    def toggleradio(self):
        pass
    
    def acceptradio(self):
        return self.choices[self.pos]
    
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
        utils.forceWrite(' ' * self.indent + self.label + '\n')
        utils.forceWrite('\n' * self.shift)
        for i in range(len(self.choices)):
            self.print(i)
            utils.forceWrite('\n')
        utils.moveCursorUp(len(self.choices) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

    def set_label(self, label):
        if isinstance(label, str):
            if not label:
                raise ValueError('<label> can not be empty')
        else:
            raise ValueError('<label> must be a string')
        self.label = label

    def set_choices(self, *choices):
        if not choices:
            raise ValueError('<choices> can not be empty')
        self.choices = choices

    def set_defaults(self, *defaults):
        if not defaults:
            raise ValueError('<defaults> can not be empty')
        self.defaults = defaults

    def one(self):
        if self.label is None:
            raise ValueError('<label> must be defined')
        if self.choices is None:
            raise ValueError('<choices> must be defined')
        if self.defaults is None:
            default = self.choices[0]
        elif len(self.defaults) > 1:
            raise ValueError('There must be only one <default>')
        elif self.defaults[0] in self.choices:
            default = self.defaults[0]
        else:
            raise ValueError('<default> must be an element of <choices>')
        self.print = self.printradio
        self.toggle = self.toggleradio
        self.accept = self.acceptradio
        self.max_width = len(max(self.choices, key = len)) + self.pad_right
        self.pos = self.choices.index(default)
        return self.render()

    def some(self):
        if self.label is None:
            raise ValueError('<label> must be defined')
        if self.choices is None:
            raise ValueError('<choices> must be defined')
        if self.defaults is None:
            defaults = []
        elif all([i in self.choices for i in self.defaults]):
            defaults = self.defaults
        else:
            raise ValueError('<defaults> must be a subset of <choices>')
        self.print = self.printcheck
        self.toggle = self.togglecheck
        self.accept = self.acceptcheck
        self.max_width = len(max(self.choices, key = len)) + self.pad_right
        self.checked = [True if i in defaults else False for i in self.choices]
        self.pos = 0
        return self.render()

