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
        self.assertEqual(2, add(1)(1))

    def test_three_args(self):
        add3 = curry(lambda a, b, c: a + b + c)
        self.assertEqual(3, add3(1)(1)(1))

    def test_positional_kwargs(self):
        add_default = curry(lambda a, b=10: a + b)
        self.assertEqual(2, add_default(1)(1))

    def test_kwargs(self):
        add_default = curry(lambda a, b=10: a + b, default=True)
        self.assertEqual(12, add_default(2))

if __name__ == '__main__':
    unittest.main()

