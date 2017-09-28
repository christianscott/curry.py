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

Features:
* [ ] functions with any number of arguments
* [ ] works with builtin functions
* [ ] pass keyword arguments
* [ ] preserve the name of passed functions
