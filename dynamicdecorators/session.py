"""Module for session manipulation."""
from contextlib import contextmanager
from dynamicdecorators import config


CACHE = {'request': None,
         'dynamic_decorators': {},
         'is_changed': False}

# {DYNAMIC_DECORATOR: [SOURCE_DECORATORS]}
SESSION_KEY = 'DYNAMIC_DECORATORS'


def set_request(request):
    """Set current request."""
    CACHE.update({'request': request,
                  'dynamic_decorators': request.session.get(SESSION_KEY, {}),
                  'is_changed': False})


def clear_request(request):
    """Remove current request."""
    if CACHE['is_changed']:
        request.session[SESSION_KEY] = CACHE['dynamic_decorators']
    CACHE.update({'request': None,
                  'dynamic_decorators': {},
                  'is_changed': False})


def enable_decorator(dynamic_decorator, source_decorator):
    """Add given pipe to given pipeline."""
    dynamic_decorators = CACHE['dynamic_decorators']
    sources = dynamic_decorators.setdefault(dynamic_decorator, [])
    if source_decorator not in sources:
        sources.append(source_decorator)
        CACHE['is_changed'] = True


def disable_decorator(dynamic_decorator, source_decorator):
    """Remove given pipe from given pipeline."""
    dynamic_decorators = CACHE['dynamic_decorators']
    sources = dynamic_decorators.setdefault(dynamic_decorator, [])
    if source_decorator in sources:
        sources.remove(source_decorator)
        CACHE['is_changed'] = True


@contextmanager
def request_store_manager(request):
    """Context manager that holds a request during execution.

    That request will be used in all the decorators. That way we will be
    able to use decorators in every function.
    """
    try:
        set_request(request)
        yield request
    finally:
        clear_request(request)


def request_store(f):
    """Decorator that stores request during execution."""
    def __wrapper__(request, *args, **kwargs):
        with request_store_manager(request):
            return f(request, *args, **kwargs)
    return __wrapper__


def get_enabled_decorators(slug):
    """Get list of enabled decorators from session."""
    decorators = config.get_pipes()
    enabled_slugs = CACHE['dynamic_decorators'].get(slug, [])
    return [d for d in decorators if d.slug in enabled_slugs]
