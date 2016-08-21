from functools import partial
# from functools import wraps

import six

from dynamicdecorators import utils
from dynamicdecorators import config


def _dynamic_decorator(f=None, name=None):
    if name is None:
        name = utils.get_name(f)
    # if no name is provided and
    if name is None:
        raise Exception(
            'No name is provided for dynamic decorator and we cannot '
            'generate a name for given function %s please provide a name '
            'for it as argument to decorator like so: '
            '@dynamicdecorator.decorate(name="my-func-name")' % repr(f))
    config.register(name)
    return f


def decorate(name):
    if isinstance(name, six.string_types):
        return partial(_dynamic_decorator, name=name)
    else:
        return _dynamic_decorator(name)
