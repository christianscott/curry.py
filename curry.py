"""Utility for currying functions."""

from functools import wraps
from inspect import signature, isbuiltin, isclass


def curry(func, args=None, kwargs=None, n=None, use_defaults=False):
    if use_defaults:
        return CurriedDefault(func, args, kwargs, n)

    return Curried(func, args, kwargs, n)


class Curried:
    def __init__(self, func, args=None, kwargs=None, target_arg_count=None):
        if not callable(func):
            raise TypeError('first argument must be callable')

        wraps(func)(self)

        self.func = func
        self.args = or_else(args, tuple())
        self.kwargs = or_else(kwargs, dict())
        self.target_arg_count = or_else(target_arg_count, get_target_arg_count(func))

    def __call__(self, *new_args, **new_kwargs):
        args = self.args + new_args

        kwargs = self.kwargs.copy()
        kwargs.update(new_kwargs)

        if self._have_enough_args(args, kwargs):
            return self.func(*args, **kwargs)

        return self._clone(args, kwargs)

    def _clone(self, args, kwargs):
        return Curried(self.func, args, kwargs, self.target_arg_count)

    def _have_enough_args(self, args, kwargs):
        return current_count(args, kwargs) == self.target_arg_count


class CurriedDefault(Curried):
    def _clone(self, args, kwargs):
        return CurriedDefault(self.func, args, kwargs, self.target_arg_count)

    def _have_enough_args(self, args, kwargs):
        count = current_count(args, kwargs)
        return count == self.target_arg_count or count == (self.target_arg_count - count_defaults(self.func))


def or_else(x, default):
    return x if x is not None else default


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
