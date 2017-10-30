**Note:** You probably shouldn't use this. This was created out of curiosity rather than necessity. I can't really imagine any scenarios where `functools.partial` isn't going to cut it. Having said that, if you find any use cases please let me know!

# curry.py

Currying/partial is cool! It helps to make the code we write much DRY-er.

As an example, let's consider a case where we want to increment each value in a sequence by a certain amount.

```python
def increment_by(by, x):
    return x + by

def increment_all(seq, by):
    return map(lambda x: increment_by(by, x), seq)
```

This is a bit more verbose than it needs to be. Wouldn't it be great if instead we could just write `map(increment_by(10), seq)`?

```python
@curry
def increment_by(by, x):
    return by + x

def increment_all(seq, by):
    return map(increment_by(by), seq)
```

This is a really trivial example but it's a lot easier to understand what's going on when we remove the noise of the `lambda`.

A more interesting example might be dependency injection (is this the right term?) when working with a database:

```python
import database

@curry
def query(connection, query_string):
    return connection.query(query_string)

def main():
    query = query(database)
    print(query('select * from users'))
```

# How does it work?

Essentially, we collect arguments until a certain number is reached, then call the function with the collected arguments.

Initially, I thought this would be possible using a closure. Assuming we have a way of knowing the number of arguments a function takes (a non-trivial question), we could try something like this (sans kwargs):

```python
def curry(func):
    args = []
    def inner(*new_args):
        args = args + new_args
        if len(args) == get_arg_count(func): # how does get_arg_count work?
            return func(*args)
        return inner
    return inner
```

Nice and simple. But also horribly wrong. Each call to the curried function will modify the same closure, resulting in this mess:

```
>>> add = curry(lambda a, b: a + b)
>>> add10 = add(10)
>>> add10(1)
11
>>> add10(2)
<function inner at 0x10a91af28>
```

Ideally, this would return 12 rather than another function. This happens because `args` now equals `[10, 1, 2]`, which is not equal to the number of args we want, so the function returns `inner` again.

We can fix this by re-currying the original function every time `inner` is called and doesn't have enough args, like this (again, sans support for kwargs to keep things simple):

```python
def curry(func, args=None):
    original_args = args if args else tuple()
    def inner(*new_args):
        next_args = original_args + new_args # no mutation!
        if len(next_args) == get_arg_count(func):
            return func(*next_args)
        return curry(func, args=next_args)
    return inner
```

(more info to come)

# Goals for the project

Features:
* [x] functions with any number of arguments
* [x] works with builtin functions
* [x] pass keyword arguments to the curried function
* [x] preserve the name of passed functions
* [ ] think of some way to tell the function to be called with the arguments it has so far. This would allow for default arguments to be used. There are two approaches that I can think of:
  * `curried(1)(2, done=True)` - has the benefit of being more flexible, can use as many of the default arguments as we like but is a bit less elegant
  * `@curry(use_default=True)` - simpler but less flexible
