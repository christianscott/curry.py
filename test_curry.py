import unittest
from curry import curry


class CurryTest(unittest.TestCase):

    def test_one_args(self):
        id = curry(lambda a: a)
        self.assertEqual(1, id(1))

    def test_two_args(self):
        add = curry(lambda a, b: a + b)
        self.assertEqual(3, add(1)(2))

    def test_three_args(self):
        add3 = curry(lambda a, b, c: a + b + c)
        self.assertEqual(6, add3(1)(2)(3))
    def test_argument_check(self):
        self.assertRaises(TypeError, curry, 1)

    def test_args_dont_persist(self):
        add = curry(lambda a, b: a + b)
        add1 = add(1)
        add2 = add(2)
        self.assertEqual(2, add1(1))
        self.assertEqual(3, add2(1))

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
        def add(a, b):
            return a + b
        add = curry(add)
        self.assertEqual('add', add.__name__)
        self.assertEqual('add', add(1).__name__)

if __name__ == '__main__':
    unittest.main()
