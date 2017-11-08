"""Utility for currying functions."""

from functools import wraps
from inspect import signature, isbuiltin, isclass


def curry(func, args=None, kwargs=None):
    if not callable(func):
        raise TypeError('first argument must be callable')

    args = args if args is not None else tuple()
    kwargs = kwargs if kwargs is not None else dict()

    @wraps(func)
    def curried(*new_args, **new_kwargs):
        next_args = args + new_args
        
        next_kwargs = kwargs.copy()
        next_kwargs.update(new_kwargs)

        if have_enough_args(func, next_args, next_kwargs):
            return func(*next_args, **next_kwargs)
        return curry(func, args=next_args, kwargs=next_kwargs)
    
    return curried


def have_enough_args(func, next_args, next_kwargs):
    current_arg_count = len(next_args) + len(next_kwargs)
    return current_arg_count == get_target_arg_count(func)


def get_target_arg_count(func):
    if isclass(func) or isbuiltin(func):
        # builtins, e.g. `map`, refer to class rather than fn
        func = func.__call__

    sig = signature(func)
    return len(sig.parameters)

