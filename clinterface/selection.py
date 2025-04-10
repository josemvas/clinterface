__all__ = (
    'Selector',
    'select_option',
    'select_options',
)

from collections.abc import Mapping, Iterable
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler

@keyhandler.init
class Selector:
    def __init__(self, shift=0, align=0, indent=0, margin=1, pad_left=1, pad_right=1, 
                 radiobullet='*', checkbullet='*', bullet_color=colors.foreground['default'],
                 bullet_on_switch=colors.REVERSE, word_color=colors.foreground['default'],
                 word_on_switch=colors.REVERSE, background_color=colors.background['default'],
                 background_on_switch=colors.REVERSE):
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
        self.pos = 0
        self.checked = None
        self.max_width = 0
        self.bullet = None
        self.get_bullet = lambda idx: ''
        self.get_bullet_length = lambda: 0
        self.num_choices = None
    def print_option(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        bullet_color = self.bullet_on_switch if idx == self.pos else self.bullet_color
        utils.cprint(' ' * self.pad_left, on=back_color, end='')
        bullet = self.get_bullet(idx)
        utils.cprint(bullet + ' ' * self.margin if bullet else ' ' * (len(self.bullet) + self.margin), 
                    bullet_color, back_color, end='')
        utils.cprint(self.options[idx], word_color, back_color, end='')
        utils.cprint(' ' * (self.max_width - len(self.options[idx])), on=back_color, end='')
        utils.moveCursorHead()
    def toggle_current_option(self):
        if self.num_choices is not None:
            # If we've already selected max choices and trying to check another, prevent it
            if not self.checked[self.pos] and sum(self.checked) >= self.num_choices:
                return
        self.checked[self.pos] = not self.checked[self.pos]
        self.print_option(self.pos)
    def finish_selection(self):
        utils.moveCursorDown(len(self.options) - self.pos)
        return self.pos
    def finish_multiple_selection(self):
        # If num_choices is set, check that exactly that many options are selected
        if self.num_choices is not None and sum(self.checked) != self.num_choices:
            # Don't allow finishing the selection until the right number of choices are made
            return None
        utils.moveCursorDown(len(self.options) - self.pos)
        return [i for i, x in enumerate(self.checked) if x]
    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        utils.clearLine()
        old_pos = self.pos
        if self.pos - 1 < 0:
            self.pos = len(self.options) - 1  # Go to the last element
        else:
            self.pos -= 1
        self.print_option(old_pos)
        # Move cursor appropriately
        if old_pos == 0 and self.pos == len(self.options) - 1:
            # If we go from first element to last
            utils.moveCursorDown(len(self.options) - 1)
        else:
            utils.moveCursorUp(1)
        self.print_option(self.pos)
    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        utils.clearLine()
        old_pos = self.pos
        if self.pos + 1 >= len(self.options):
            self.pos = 0  # Go to the first element
        else:
            self.pos += 1
        self.print_option(old_pos)
        # Move cursor appropriately
        if old_pos == len(self.options) - 1 and self.pos == 0:
            # If we go from last element to first
            utils.moveCursorUp(len(self.options) - 1)
        else:
            utils.moveCursorDown(1)
        self.print_option(self.pos)
    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.options) - self.pos)
        raise KeyboardInterrupt
    def render(self):
        if self.prompt is None:
            raise ValueError('Message is not set')
        if self.options is None:
            raise ValueError('Options are not set')
        utils.forceWrite(' ' * self.indent + self.prompt + '\n')
        utils.forceWrite('\n' * self.shift)
        for i in range(len(self.options)):
            self.print_option(i)
            utils.forceWrite('\n')
        utils.moveCursorUp(len(self.options) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

_DEFAULT_SELECTOR = Selector()

def unpack_single(func):
    """Decorator for functions that handle a single option selection."""
    def wrapper(prompt, options, default=None, *args, **kwargs):
        # Validate and process options by type
        if isinstance(options, Mapping):
            keys = list(options.keys())
            options_list = [str(options[k]) for k in keys]
            index_to_key = {i: key for i, key in enumerate(keys)}
            original_list = keys
        elif isinstance(options, Iterable) and not isinstance(options, (str, bytes)):
            original_list = list(options)
            options_list = [str(opt) for opt in original_list]
            index_to_key = {i: item for i, item in enumerate(original_list)}
        else:
            raise TypeError("Options must be a mapping or a non-string iterable")
        # Check for emptiness and uniqueness
        if not options_list:
            raise ValueError("Options cannot be empty")
        if len(options_list) > len(set(options_list)):
            raise ValueError("Options must have unique string representations")
        default_index = original_list.index(default) if default is not None else None
        result_index = func(prompt, options_list, default=default_index, *args, **kwargs)
        return index_to_key[result_index]
    return wrapper

def unpack_multiple(func):
    """Decorator for functions that handle multiple option selections."""
    def wrapper(prompt, options, defaults=None, *args, **kwargs):
        # Validate and process options by type
        if isinstance(options, Mapping):
            keys = list(options.keys())
            options_list = [str(options[k]) for k in keys]
            index_to_key = {i: key for i, key in enumerate(keys)}
            original_list = keys
        elif isinstance(options, Iterable) and not isinstance(options, (str, bytes)):
            original_list = list(options)
            options_list = [str(opt) for opt in original_list]
            index_to_key = {i: item for i, item in enumerate(original_list)}
        else:
            raise TypeError("Options must be a mapping or a non-string iterable")
        # Check for emptiness and uniqueness
        if not options_list:
            raise ValueError("Options cannot be empty")
        if len(options_list) > len(set(options_list)):
            raise ValueError("Options must have unique string representations")
        default_indices = [original_list.index(d) for d in defaults] if defaults else None
        result_indices = func(prompt, options_list, defaults=default_indices, *args, **kwargs)
        return [index_to_key[i] for i in result_indices]
    return wrapper

@unpack_single
def select_option(prompt, options, default=None, selector=None):
    """Select a single option from a list and return its index."""
    if selector is None:
        selector = _DEFAULT_SELECTOR
    selector.pos = 0 if default is None else default
    selector.prompt = prompt
    selector.options = options
    selector.bullet = selector.radiobullet
    selector.get_bullet = lambda idx: selector.bullet if idx == selector.pos else ''
    selector._key_handler[SPACE_CHAR] = lambda self: None
    selector._key_handler[NEWLINE_KEY] = lambda self: self.finish_selection()
    selector.max_width = len(max(options, key=len)) + selector.pad_right
    return selector.render()

@unpack_multiple
def select_options(prompt, options, defaults=None, selector=None, num_choices=None):
    """Select multiple options from a list and return their indices."""
    if selector is None:
        selector = _DEFAULT_SELECTOR
    if num_choices is not None and num_choices > len(options):
        raise ValueError(f"num_choices ({num_choices}) cannot exceed options count")
    selector.pos = 0
    selector.checked = [False for x in options]
    if defaults is not None:
        selector.pos = defaults[0]
        for idx in defaults:
            selector.checked[idx] = True
    selector.num_choices = num_choices
    selector.prompt = prompt
    selector.options = options
    selector.bullet = selector.checkbullet
    selector.get_bullet = lambda idx: selector.bullet if selector.checked[idx] else ''
    selector._key_handler[SPACE_CHAR] = lambda self: self.toggle_current_option()
    selector._key_handler[NEWLINE_KEY] = lambda self: self.finish_multiple_selection()
    selector.max_width = len(max(options, key=len)) + selector.pad_right
    return selector.render()
