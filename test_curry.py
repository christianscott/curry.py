import math
import unittest
from curry import curry

def func(a, b, *, c, d):
    return (a, b), dict(c=c, d=d)

class TestCurry(unittest.TestCase):

    def test_basic_examples(self):
        f = curry(func)
        self.assertEqual(f(1)(2)(c=10)(d=20),
                         ((1, 2), dict(c=10, d=20)))

    def test_builtins(self):
        f = curry(map)(lambda x: x + 1)
        self.assertEqual(list(f([1, 2, 3, 4])),
                                [2, 3, 4, 5])

        f = curry(math.pow)(2)
        self.assertAlmostEqual(f(4), 16)

    def test_attributes(self):
        f = curry(func)(1)(2)(c=10)

        self.assertEqual(f.fun, func)
        self.assertEqual(f.args, (1, 2))
        self.assertEqual(f.kwargs, dict(c=10))

    def test_argument_check(self):
        self.assertRaises(TypeError, curry, 1)

    def test_args_dont_persist(self):
        curried_func = curry(func)

        f = curried_func(1)(2)(c=10)
        g = curried_func('a')('b')(c='c')

        self.assertEqual(f(d=20),
                         ((1, 2), dict(c=10, d=20)))
        self.assertEqual(g(d='d'),
                         (('a', 'b'), dict(c='c', d='d')))

    def test_args_dont_persist_after_first(self):
        factory = curry(lambda a, b, c: None)
        curried = factory(1)
        given_b = curried(2)
        given_c = curried(3)
        self.assertIsNotNone(given_c)

    def test_kwargs_dont_persist(self):
        factory = curry(lambda a=None, b=None, c=None: None)
        curried = factory(a=None)
        given_b = curried(b=None)
        given_c = curried(c=None)
        self.assertIsNotNone(given_c)

    def test_mutable_args(self):
        def concat(a, b):
            ret = []
            ret.extend(a)
            ret.extend(b)
            return ret
        concat = curry(concat)
        self.assertEqual([1, 2, 3, 4], concat([1, 2])([3, 4]))

    def test_positional_kwargs(self):
        add_default = curry(lambda a, b=10: a + b)
        self.assertEqual(3, add_default(1)(2))

if __name__ == '__main__':
    unittest.main()
