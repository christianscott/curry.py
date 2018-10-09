"""Utility for currying functions."""

from functools import wraps
from inspect import signature, isbuiltin, isclass

def curry(func, args=None, kwargs=None, n=None):
    if not callable(func):
        raise TypeError('first argument must be callable')

    args = args if args is not None else tuple()
    kwargs = kwargs if kwargs is not None else dict()

    @wraps(func)
    def curried(*new_args, **new_kwargs):
        next_args = args + new_args

        next_kwargs = kwargs.copy()
        next_kwargs.update(new_kwargs)

        target_arg_count = n if n is not None else get_target_arg_count(func)

        if current_count(next_args, next_kwargs) == target_arg_count:
            return func(*next_args, **next_kwargs)

        return curry(func, args=next_args, kwargs=next_kwargs, n=n)

    return curried

def curry_default(func, args=None, kwargs=None, n=None):
    if not callable(func):
        raise TypeError('first argument must be callable')

    args = args if args is not None else tuple()
    kwargs = kwargs if kwargs is not None else dict()

    @wraps(func)
    def curried(*new_args, **new_kwargs):
        next_args = args + new_args

        next_kwargs = kwargs.copy()
        next_kwargs.update(new_kwargs)

        target_arg_count = n if n is not None else get_target_arg_count(func)
        default_count = count_defaults(func)

        if current_count(next_args, next_kwargs) == target_arg_count:
            return func(*next_args, **next_kwargs)
        elif current_count(next_args, next_kwargs) == target_arg_count - default_count:
            return func(*next_args, **next_kwargs)

        return curry_default(func, args=next_args, kwargs=next_kwargs, n=n)

    return curried

def current_count(next_args, next_kwargs):
    return len(next_args) + len(next_kwargs)

def count_defaults(func):
    length = 0
    if func.__defaults__ is not None:
        length += len(func.__defaults__)
    if func.__kwdefaults__ is not None:
        length += len(func.__kwdefaults__)
    return length

def get_target_arg_count(func):
    if isclass(func) or isbuiltin(func):
        # builtins, e.g. `map`, refer to class rather than fn
        func = func.__call__

    sig = signature(func)
    return len(sig.parameters)
