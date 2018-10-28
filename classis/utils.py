# -*- coding: utf-8 -*-

from json import dumps
from random import choice
from string import ascii_letters
from re import match


def generate_response(fun):
    def wrapper(*args, **kwargs):
        err = None
        res = fun(*args, **kwargs)
        if isinstance(res, tuple):
            res, err = res
        return dumps({
            'response': res,
            'error': err or '',
        })
    wrapper.__name__ = ''.join([choice(ascii_letters) for i in range(20)])
    return wrapper


def is_valid_name(name: str) -> bool:
    res = match(r'(^\w[\w\s\w]+\w+$)|(\w+)', name)
    return res is not None and res[0] == name and '  ' not in name and not (name.startswith(' ') or name.endswith(' '))


def integer_try_parse(value, default=None):
    try:
        return int(value)
    except ValueError:
        pass
    except TypeError:
        pass
    return default
