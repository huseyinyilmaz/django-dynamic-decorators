"""
Utilities for reading configuration from settings.
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# list of registered decorators.
DECORATORS = set()


PROVIDED_DECORATORS = []


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
    """Return all registered decorators"""
    return DECORATORS


def get_provided_decorators():
    # TODO: If settings does not have PROVIDED_DECORATORS assign it.
    if not PROVIDED_DECORATORS:
        for d in settings.DYNAMIC_DECORATORS:
            # Set Default vaues.
            if 'function' not in d:
                raise ImproperlyConfigured(
                    'Configuration do not have function item: %s' % d)
            if 'name' not in d:
                d['name'] = d['function']
            if 'group' not in d:
                d['group'] = ''
            if any(e for e in PROVIDED_DECORATORS
                   if d['name'] == d):
                raise ImproperlyConfigured(
                    'Duplicate name in decorator configuration: %s' % d)

            PROVIDED_DECORATORS.append(d)
    return PROVIDED_DECORATORS
