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

The idea is to return a function that keeps accepting arguments (one at a time) until it has enough of them to call the wrapped function. Currently, this is done by storing each of the arguments in a list, then calling the wrapped function with all of those args once the length of the list reaches the number of arguments the wrapped function takes.

The list of arguments is preserved using a concept called a _closure_. This is kind of like a tiny, encapsulated bit of state. I'm not exactly sure how the updates to the state are preserved when `curried` returns itself, but I think this is because args (and therefore the closure) is being mutated.

My solution in its' current form isn't able to handle keyword arguments being passed to it. They work as postional arguments, 

# Goals for the project

Features:
* [x] functions with any number of arguments
* [ ] works with builtin functions
* [ ] pass keyword arguments to the curried function
* [x] preserve the name of passed functions
* [ ] think of some way to tell the function to be called with the arguments it has so far. This would allow for default arguments to be used. There are two approaches that I can think of:
  * `curried(1)(2, done=True)` - has the benefit of being more flexible, can use as many of the default arguments as we like but is a bit less elegant
  * `@curry(use_default=True)` - simpler but less flexible
