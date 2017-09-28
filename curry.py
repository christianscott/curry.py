from inspect import signature
import sys
import unittest


def curry(fun):
    arg_count = len(signature(fun).parameters)
    args = []

    def curried(arg):
        args.append(arg)

        if len(args) == arg_count:
            return fun(*args)
        else:
            return curried
        
    return curried


class CurryTest(unittest.TestCase):
    def test_two_args(self):
        add = curry(lambda a, b: a + b)
        self.assertEqual(3, add(1)(2))

    def test_three_args(self):
        add3 = curry(lambda a, b, c: a + b + c)
        self.assertEqual(6, add3(1)(2)(3))

    def test_mutable_args(self):
        concat = curry(lambda a, b: a.extend(b))
        self.assertEqual([1, 2, 3, 4], concat([1, 2])([3, 4]))

    def test_builtin(self):
        add_1_to_each = curry(map)(lambda x: x + 1)
        self.assertEqual([2, 3, 4, 5], 
                         list(add_1_to_each([1, 2, 3, 4])))

    def test_positional_kwargs(self):
        add_default = curry(lambda a, b=10: a + b)
        self.assertEqual(3, add_default(1)(2))

    def test_kwargs(self):
        add_default = curry(lambda a, b=10: a + b, default=True)
        self.assertEqual(12, add_default(2))

    def test_preserve_name(self):
        def add(a, b): return a + b
        add = curry(add)
        self.assertEqual('add', add.__name__)

if __name__ == '__main__':
    unittest.main()

