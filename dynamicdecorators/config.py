"""
Utilities for reading configuration from settings.
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import slugify

try:
    from django.utils.module_loading import import_string
except ImportError:
    # django < 1.7
    from django.utils.module_loading import import_by_path as import_string


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


# TODO add memoize
def get_provided_decorators():
    # TODO: In settings we should be able to provide only path
    #       and system should be able to create dict structure.
    # TODO: If settings does not have PROVIDED_DECORATORS assign it.
    #       we should return
    provided_decorators = []
    for d in settings.DYNAMIC_DECORATORS:
        # Set Default vaues.
        if 'function' not in d:
            raise ImproperlyConfigured(
                'Configuration do not have function item: %s' % d)
        if 'name' not in d:
            d['name'] = d['function']
        if 'group' not in d:
            d['group'] = ''
        d['slug'] = slugify(d['name'])
        d['loaded_function'] = import_string(d['function'])
        if any(e for e in PROVIDED_DECORATORS
               if d['slug'] == e['slug']):
            raise ImproperlyConfigured(
                'Duplicate name in decorator configuration: %s' % d)
        provided_decorators.append(d)
    return provided_decorators
