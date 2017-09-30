"""Utility for currying functions."""

import sys
from functools import wraps
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


def curry(fun):
    """Return a curried version of the supplied function."""
    arg_count = get_arg_count(fun)

    @wraps(fun)
    def curried_factory(*initial_args, **initial_kwargs):
        args_store = list(initial_args)
        kwargs_store = initial_kwargs

        @wraps(fun)
        def curried(*args, **kwargs):
            nonlocal args_store, kwargs_store
            kwargs_store.update(kwargs)

            args_store = args_store + list(args)

            if len(args_store) + len(kwargs_store) == arg_count:
                return fun(*args_store, **kwargs_store)
            else:
                return curried

        if len(args_store) + len(kwargs_store) == arg_count:
            return fun(*args_store, **kwargs_store)

        return curried
    return curried_factory
