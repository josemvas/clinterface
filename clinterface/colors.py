BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
DEFAULT = "\u001b[39m"

foreground = {
    "black"  : "\u001b[30m",
    "red"    : "\u001b[31m",
    "green"  : "\u001b[32m",
    "yellow" : "\u001b[33m",
    "blue"   : "\u001b[34m",
    "magenta" : "\u001b[35m",
    "cyan"   : "\u001b[36m",
    "white"  : "\u001b[37m",
    "default"  : "\u001b[39m",
}

background = {
    "black"  : "\u001b[40m",
    "red"    : "\u001b[41m",
    "green"  : "\u001b[42m",
    "yellow" : "\u001b[43m",
    "blue"   : "\u001b[44m",
    "magenta" : "\u001b[45m",
    "cyan"   : "\u001b[46m",
    "white"  : "\u001b[47m",
    "default"  : "\u001b[49m",
}

REVERSE = "\u001b[7m"
RESET_REVERSE = "\u001b[27m"

RESET = "\u001b[0m"
    
def bright(color):
    return color[:-1] + ";1m"
