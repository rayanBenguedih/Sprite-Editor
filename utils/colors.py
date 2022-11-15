_colors = {
    'header':  '\033[95m',
    'blue':    '\033[94m',
    'cyan':    '\033[96m',
    'green':   '\033[92m',
    'warning': '\033[93m',
    'fail':    '\033[91m',
    'end':     '\033[0m',
}

class _meta(type):
    @staticmethod
    def __getattribute__(attr):
        assert attr in _colors, f'{attr} is not supported as a color.'
        return (lambda text: f"{_colors.get(attr)}{text}{_colors.get('end')}")

class _c(metaclass=_meta):
    pass
from sys import modules
modules['utils.colors'] = _c
