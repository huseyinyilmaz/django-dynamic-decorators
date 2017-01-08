"""Decorators to register a dynamic decorator.

Dynamic decorators should not reach the session in initialization time because
dynamic decorator middleware also registers itself as a decorator but we do
not have session data when register middleware.
"""
import logging
from functools import partial
from functools import wraps

# import six
from django.utils.text import slugify

from dynamicdecorators import utils
from dynamicdecorators import config
from dynamicdecorators import session

logger = logging.getLogger(__name__)


def _dynamic_decorator(f=None, name=None, slug=None, meta=None):
    if meta is None:
        meta = {}
    # If name is not provided try to get name from function.
    if name is None:
        name = utils.get_name(f)
    # if there is still no name raise an error.
    if name is None:
        # TODO Check if this exception is raised correctly.
        raise Exception(
            'No name is provided for dynamic decorator and we cannot '
            'generate a name for given function %s please provide a name '
            'for it as argument to decorator like so: '
            '@dynamicdecorators.decorators.my_func_name' % repr(f))
    if slug is None:
        slug = slugify(name)
    config.register_pipeline(slug, name, meta)

    @wraps(f)
    def _wrapper(*args, **kwargs):
        decorators = session.get_enabled_decorators(slug)
        if decorators:
            logger.debug('Apply_decorators %s' % decorators)
            func = utils.compose(*(utils.import_function(m.function)
                                   for m in decorators))(f)
        else:
            func = f
        return func(*args, **kwargs)

    return _wrapper


def decorate(f=None, name=None, slug=None, **kwargs):
    """Decorate given function."""
    if f is None:
        return partial(_dynamic_decorator, name=name, slug=slug, meta=kwargs)
    else:
        return _dynamic_decorator(f, name=name, slug=slug, meta=kwargs)


class Decorators:
    """Alternative interface for decorator function."""

    def __getattr__(self, attr_name):
        """Call decorate function with attr name as name."""
        return partial(decorate, name=attr_name)
