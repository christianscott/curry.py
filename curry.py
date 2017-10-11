"""Utility for currying functions."""

from functools import update_wrapper
from inspect import signature, isclass


class _CurriedFactory:
    """Return a curried version of the supplied function."""

    def __init__(self, fun, args=None, kwargs=None):
        if not callable(fun):
            raise TypeError('first argument must be callable')

        self.fun = fun

        self.args = args if args is not None else tuple()
        self.kwargs = kwargs if kwargs is not None else dict()

        update_wrapper(self, self.fun)

    def __call__(self, *new_args, **new_kwargs):
        next_curried = self.create_next_curried(new_args, new_kwargs)

        if next_curried.has_enough_args():
            return next_curried.call_with_arguments()
        else:
            return next_curried

    def create_next_curried(self, new_args, new_kwargs):
        next_args = self.args + new_args

        next_kwargs = self.kwargs.copy()
        next_kwargs.update(new_kwargs)

        return _CurriedFactory(self.fun, args=next_args, kwargs=next_kwargs)

    def has_enough_args(self):
        current_arg_count = len(self.args) + len(self.kwargs)
        return current_arg_count == self.get_target_arg_count()

    def get_target_arg_count(self):
        callable_ = self.fun

        if isclass(callable_):
            # builtins, e.g. `map`, refer to class rather than fn
            callable_ = callable_.__call__

        sig = signature(callable_)
        return len(sig.parameters)

    def call_with_arguments(self):
        return self.fun(*self.args, **self.kwargs)

curry = _CurriedFactory

