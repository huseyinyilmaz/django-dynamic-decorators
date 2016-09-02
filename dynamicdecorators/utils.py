def compose(*fs):
    """compose(*functions) -> function.

    Compose several functions into one.
    When called, the composed function passes its arguments to the last function
    in `fs`, then its return value to the one before it and so on.
    compose(f, g, h)(arg) == f(g(h(arg)))

    Source: https://github.com/clsr/fun.py/blob/98b7a420ed6bde883bd740643960510cd2e2a6b0/fun.py#L5-L18  # noqa
"""
    fs = fs[::-1]

    def composed(*args):
        for fn in fs:
            args = (fn(*args),)
        return args[0]
    return composed


KWARG_MARK = (object(),)   # separates positional and keyword args


def memoize(func):
    """Memoize given function."""
    cache = {}

    def _wrapper(*args, **kwargs):
        # serialize argument list to a string key
        key = repr(args + KWARG_MARK + tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return _wrapper


def get_name(func):
    """Gets name of a function.

    If name cannot be generated returns None
    """
    # TODO make a hook on function so people could set manual names to
    # functions if they want to.
    if hasattr(func, '__name__') and hasattr(func, '__module__'):
        return '{0}.{1}:{2}'.format(func.__module__,
                                    func.__name__,
                                    func.func_code.co_firstlineno)
    else:
        return None
