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

The 'curry' function takes an input object and calls the 'get_arg_count' function. This function checks if the input it receives is a function or a class definition. And based on that, it returns the number of parameters required by the input function/class to execute.

Now, we use @wraps(fun) to prevent loss of meta data of the function. When a decorator function decorates a decorated function, properties such as __name__ and DocString of the decorated function gets replaced with that of the decorator function. This is less than helpful. To prevent this, we use the @wraps(fun).

This lambda function takes 3 inputs and finds the sum of the three. Our curried function should be able to run 3 times, taking one input at each time.

```python
def curry(fun):
    '''
    gets the number of arguments to run the function
    '''
    arg_count = get_arg_count(fun)

    @wraps(fun)
    def curried_factory(*initial_args, **initial_kwargs):
        '''
        When the curried function is called for the very first time, it creates a list to store the
        positional arguments and similarly a key-valued structure for the keyword arguments.
        '''

        args_store = list(initial_args)
        kwargs_store = initial_kwargs

        @wraps(fun)
        def curried(*args, **kwargs):
            '''
            On subsequent calls to the curried function, we store the new incoming arguments along
            with our initial arguments. And since the initial storage is neither in the local nor the
            global scope we instruct python about the scope using the nonlocal keyword.
            '''

            nonlocal args_store, kwargs_store

            '''
            At this point, we update the initial storage with the new inputs we obtain and we keep doing this
            until we have enough inputs to actually execute the function.
            '''
            kwargs_store.update(kwargs)
            args_store = args_store + list(args)

            if len(args_store) + len(kwargs_store) == arg_count:
                '''
                If we have enough arguments to run the function, the function gets executed
                '''
                return fun(*args_store, **kwargs_store)
            else:
                '''
                else, we repeat the argument collection process until we have enough arguments
                '''
                return curried

        return curried

    return curried_factory
 ```

# Goals for the project

Features:
* [x] functions with any number of arguments
* [ ] works with builtin functions
* [ ] pass keyword arguments to the curried function
* [x] preserve the name of passed functions
* [ ] think of some way to tell the function to be called with the arguments it has so far. This would allow for default arguments to be used. There are two approaches that I can think of:
  * `curried(1)(2, done=True)` - has the benefit of being more flexible, can use as many of the default arguments as we like but is a bit less elegant
  * `@curry(use_default=True)` - simpler but less flexible
