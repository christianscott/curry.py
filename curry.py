"""Utility for currying functions."""

from functools import update_wrapper
from inspect import signature, isclass


def get_arg_count(fun):
    """Return the number of parameters a function takes.

    Builtins, by default, refer to their class rather than their function call.
    Referring to their __call__ instance allows them to operate as any other
    function when curried.
    """
    if isclass(fun):
        return len(signature(fun.__call__).parameters)
    return len(signature(fun).parameters)

class _CurriedFactory:
    """Return a curried version of the supplied function."""

    def __init__(self, fun, args=None, kwargs=None):
        self.fun = fun
        self.arg_count = get_arg_count(fun)
        self.args = args if args is not None else tuple()
        self.kwargs = kwargs if kwargs is not None else dict()
        update_wrapper(self, self.fun)

    def __call__(self, *args, **kwargs):
        combined_args = self.args + args
        combined_kwargs = self.kwargs.copy()
        combined_kwargs.update(kwargs)
        if len(combined_args) + len(combined_kwargs) == self.arg_count:
            return self.fun(*combined_args, **combined_kwargs)
        else:
            return _CurriedFactory(
                self.fun, args=combined_args, kwargs=combined_kwargs
            )

curry = _CurriedFactory
