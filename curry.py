"""Utility for currying functions."""

from functools import wraps
from inspect import signature, isclass
import sys
import unittest


def get_arg_count(fun):
    """Return the number of parameters a function takes.

    Builtins, by default, refer to their class rather than their function call.
    Referring to their __call__ instance allows them to operate as any other
    function when curried.
    """
    if isclass(fun):
        return len(signature(fun.__call__).parameters)
    else:
        return len(signature(fun).parameters)


def curry(fun):
    """Return a curried version of the supplied function."""
    arg_count = get_arg_count(fun)

    @wraps(fun)
    def curried_factory(*initial_args, **initial_kwargs):
        args_store = list(initial_args)
        kwargs_store = initial_kwargs

        def done_eval():
            """
            If done_keyword is present in kwargs_store, removes it 
            from kwargs_store and returns it otherwise returns False.
            """
            done_keyword = "done"
            done_evaluation = False
            if done_keyword in kwargs_store:
                done_evaluation = kwargs_store.pop(done_keyword,False)
            return done_evaluation

        @wraps(fun)
        def curried(*args, **kwargs):
            nonlocal args_store, kwargs_store
            kwargs_store.update(kwargs)
            args_store = args_store + list(args)

            if done_eval():
                return fun(*args_store, **kwargs_store)
            if len(args_store) + len(kwargs_store) == arg_count:
                return fun(*args_store, **kwargs_store)
            else:
                return curried

        if done_eval():
            return fun(*args_store, **kwargs_store)
        if len(args_store) + len(kwargs_store) == arg_count:
            return fun(*args_store, **kwargs_store)
        
        return curried

    return curried_factory

class CurryTest(unittest.TestCase):
    def test_two_args(self):
        add = curry(lambda a, b: a + b)
        self.assertEqual(3, add(1)(2))

    def test_three_args(self):
        add3 = curry(lambda a, b, c: a + b + c)
        self.assertEqual(6, add3(1)(2)(3))

    def test_args_dont_persist(self):
        add = curry(lambda a, b: a + b)
        add1 = add(1)
        add2 = add(2)
        self.assertEqual(2, add1(1))
        self.assertEqual(3, add2(1))

    def test_mutable_args(self):
        def concat(a, b):
            ret = []
            ret.extend(a)
            ret.extend(b)
            return ret
        concat = curry(concat)
        self.assertEqual([1, 2, 3, 4], concat([1, 2])([3, 4]))

    def test_builtin(self):
        add_1_to_each = curry(map)(lambda x: x + 1)
        self.assertEqual([2, 3, 4, 5],
                         list(add_1_to_each([1, 2, 3, 4])))

    def test_positional_kwargs(self):
        add_default = curry(lambda a, b=10: a + b)
        self.assertEqual(3, add_default(1)(2))

    def test_kwargs(self):
        @curry
        def add(a, *, b):
            return a + b
        self.assertEqual(12, add(2)(b=10))

    def test_preserve_name(self):
        def add(a, b): return a + b
        add = curry(add)
        self.assertEqual('add', add.__name__)
        self.assertEqual('add', add(1).__name__)

if __name__ == '__main__':
    unittest.main()


