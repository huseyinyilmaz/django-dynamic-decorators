def get_name(func):
    """Gets name of a function.

    If name cannot be generated returns None
    """
    if hasattr(func, '__name__') and hasattr(func, '__module__'):
        return '{0}.{1}:{2}'.format(func.__module__,
                                    func.__name__,
                                    func.func_code.co_firstlineno)
    else:
        return None
