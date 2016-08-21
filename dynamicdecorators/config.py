"""
Utilities for reading configuration from settings.
"""
# list of registered decorators.
DECORATORS = set()


class Decorator:
    def __init__(self, name, function):
        self.name = name
        self.fuction = function


def register(name):
    """Register a decorator.

    We want to keep a list of decorators applied because each one of them will
    have its own configuration and interface.

    Also registration should be idempotent. Because sometimes middlewares gets,
    initialized multiple times. In that case we want to use only one.
    """
    print('Register invoked')
    DECORATORS.add(name)
    return name


def get_registered_decorators():
    return DECORATORS
