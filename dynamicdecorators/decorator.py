"""Decorators to register a dynamic decorator.

Dynamic decorators should not reach the session in initialization time because
dynamic decorator middleware also registers itself as a decorator but we do
not have session data when register middleware.
"""
from functools import partial
from functools import wraps

import six

from dynamicdecorators import utils
from dynamicdecorators import config
from dynamicdecorators import session


def _dynamic_decorator(f=None, name=None):
    # If name is not provided try to get name from function.
    if name is None:
        name = utils.get_name(f)
    # if there is still no name raise an error and for
    if name is None:
        raise Exception(
            'No name is provided for dynamic decorator and we cannot '
            'generate a name for given function %s please provide a name '
            'for it as argument to decorator like so: '
            '@dynamicdecorators.decorators.my_func_name' % repr(f))
    config.register(name)

    @wraps(f)
    def _wrapper(*args, **kwargs):
        session.get_enabled_decorators(slug)
        mocks = []
        if mocks:
            func = utils.compose(*mocks)(f)
        else:
            func = f
        return func(*args, **kwargs)

    return _wrapper


def decorate(name):
    if isinstance(name, six.string_types):
        return partial(_dynamic_decorator, name=name)
    else:
        return _dynamic_decorator(name)


class Decorators:
    def __getattr__(self, attr_name):
        return decorate(attr_name)
