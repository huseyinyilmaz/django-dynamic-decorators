from contextlib import contextmanager
from dynamicdecorators import config


CACHE = {'request': None,
         'dynamic_decorators': {},
         'is_changed': False}

# {DYNAMIC_DECORATOR: [SOURCE_DECORATORS]}
SESSION_KEY = 'DYNAMIC_DECORATORS'


def set_request(request):
    CACHE.update({'request': request,
                  'dynamic_decorators': request.session.get(SESSION_KEY, {}),
                  'is_changed': False})


def clear_request(request):
    if CACHE['is_changed']:
        request.session[SESSION_KEY] = CACHE['dynamic_decorators']
    CACHE.update({'request': None,
                  'dynamic_decorators': {},
                  'is_changed': False})


def enable_decorator(dynamic_decorator, source_decorator):
    dynamic_decorators = CACHE['dynamic_decorators']
    sources = dynamic_decorators.setdefault(dynamic_decorator, [])
    if source_decorator not in sources:
        sources.append(source_decorator)
        CACHE['is_changed'] = True


def disable_decorator(dynamic_decorator, source_decorator):
    dynamic_decorators = CACHE['dynamic_decorators']
    sources = dynamic_decorators.setdefault(dynamic_decorator, [])
    if source_decorator in sources:
        sources.remove(source_decorator)
        CACHE['is_changed'] = True


@contextmanager
def request_store_manager(request):
    try:
        set_request(request)
        yield request
    finally:
        clear_request(request)


def request_store(f):
    def __wrapper__(request, *args, **kwargs):
        with request_store_manager(request):
            return f(request, *args, **kwargs)
    return __wrapper__


def get_enabled_decorators(slug):
    decorators = config.Decorator.get_provided_decorators()
    enabled_slugs = CACHE['dynamic_decorators'].get(slug, [])
    return [d for d in decorators
            if d['slug'] in enabled_slugs]
