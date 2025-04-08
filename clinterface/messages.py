from string import Template
from collections import defaultdict
from .colors import DEFAULT, GREEN, YELLOW, RED

class TrackingDict(defaultdict):
# Subclase de defaultdict que registra las claves accedidas durante las operaciones
    def __init__(self, *args, **kwargs):
        self.used_keys = set()
        super().__init__(*args, **kwargs)
    def __getitem__(self, key):
        self.used_keys.add(key)
        return super().__getitem__(key)

def template_substitution(func):
    def wrapper(message, **kwargs):
        # Crear un diccionario de seguimiento que registrará las claves utilizadas
        tracking_dict = TrackingDict(str)
        # Inicializar con los valores proporcionados
        tracking_dict.update(kwargs)
        # Crear el template y realizar la sustitución
        template = Template(message)
        substituted_message = template.safe_substitute(tracking_dict)
        # Identificar las claves no utilizadas
        unused_kwargs = {k: v for k, v in kwargs.items() if k not in tracking_dict.used_keys}
        # Si hay kwargs no utilizados, añadirlos al final del mensaje
        if unused_kwargs:
            unused_str = ", ".join(f"{k}={v}" for k, v in unused_kwargs.items())
            substituted_message = f"{substituted_message} ({unused_str})"
        # Llamar a la función decorada con el mensaje modificado
        return func(substituted_message)
    return wrapper

def color_print(text, color):
    print(color + text + DEFAULT)

@template_substitution
def success(message):
    color_print(message, GREEN)

@template_substitution
def failure(message):
    color_print(message, RED)

@template_substitution
def error(message):
    color_print(f'ERROR: {message}', RED)
    raise SystemExit

@template_substitution
def warning(message):
    color_print(f'WARNING: {message}', YELLOW)
