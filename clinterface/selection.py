from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler

__all__ = (
    'Selector',
    'select_option',
    'select_options',
)


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
        self.options = None          # list of display strings
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
        utils.cprint(
            bullet + ' ' * self.margin if bullet else ' ' * (len(self.bullet) + self.margin),
            bullet_color,
            back_color,
            end=''
        )
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


def _normalize_options(options):
    """
    Returns (keys, display_strings).
    """
    if isinstance(options, dict):
        keys = list(options.keys())
        if not keys:
            raise ValueError("Options cannot be empty")
        values = [options[k] for k in keys]
    else:
        if not isinstance(options, (list, tuple)):
            raise TypeError("Options must be a dictionary or a list/tuple")
        if not options:
            raise ValueError("Options cannot be empty")
        keys = options
        values = options

    display_strings = [str(k) for k in keys]
    if len(display_strings) != len(set(display_strings)):
        raise ValueError("Options must have unique string representations")

    return values, display_strings


def select_option(prompt, options, default=None, selector=None):
    """
    Select a single option and return its index/key).
    """
    values, display_strings = _normalize_options(options)

    if default is not None:
        try:
            default_index = values.index(default)
        except ValueError:
            raise ValueError("Default must be one of the options") from None
    else:
        default_index = None

    selector = Selector() if selector is None else selector

    selector.num_choices = None
    selector.checked = None
    selector.pos = 0 if default_index is None else default_index
    selector.prompt = prompt
    selector.options = display_strings
    selector.bullet = selector.radiobullet
    selector.get_bullet = lambda idx: selector.bullet if idx == selector.pos else ''
    selector._key_handler[SPACE_CHAR] = lambda self: None
    selector._key_handler[NEWLINE_KEY] = lambda self: self.finish_selection()
    selector.max_width = max(len(s) for s in display_strings) + selector.pad_right

    index = selector.render()
    return values[index]


def select_options(prompt, options, defaults=None, selector=None, num_choices=None):
    """
    Select multiple options and return their indices/keys.
    """
    values, display_strings = _normalize_options(options)

    if num_choices is not None and num_choices > len(display_strings):
        raise ValueError(f"num_choices ({num_choices}) cannot exceed options count")

    default_indices = []
    if defaults:
        for d in defaults:
            try:
                default_indices.append(values.index(d))
            except ValueError:
                raise ValueError("Each default must be one of the options") from None

    selector = Selector() if selector is None else selector

    selector.num_choices = num_choices
    selector.checked = [False] * len(display_strings)
    if default_indices:
        selector.pos = default_indices[0]
        for idx in default_indices:
            selector.checked[idx] = True
    else:
        selector.pos = 0

    selector.prompt = prompt
    selector.options = display_strings
    selector.bullet = selector.checkbullet
    selector.get_bullet = lambda idx: selector.bullet if selector.checked[idx] else ''
    selector._key_handler[SPACE_CHAR] = lambda self: self.toggle_current_option()
    selector._key_handler[NEWLINE_KEY] = lambda self: self.finish_multiple_selection()
    selector.max_width = max(len(s) for s in display_strings) + selector.pad_right

    indices = selector.render()
    return [values[i] for i in indices]
