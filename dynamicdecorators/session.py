from contextlib import contextmanager
from dynamicdecorators.config import get_registered_decorators

CACHE = {'request': None,
         'is_changed': False}
# {DYNAMIC_DECORATOR: [SOURCE_DECORATORS]}
SESSION_KEY = 'DYNAMIC_DECORATORS'


def set_request(request):
    CACHE.update({'request': request,
                  'dynamic_decorators': request.session.get(SESSION_KEY, {}),
                  'is_changed': False})


def clear_request(request):
    CACHE.update({'request': None,
                  'dynamic_decorators': None,
                  'is_changed': False})
    del CACHE['request']


def enable_decorator(dynamic_decorator, source_decorator):
    dynamic_decorators = CACHE['dynamic_decorators']
    sources = dynamic_decorators.set_default(dynamic_decorator, [])
    if source_decorator not in sources:
        source_decorator.append(source_decorator)
        CACHE['is_changed'] = True


def disable_decorator(dynamic_decorator, source_decorator):
    dynamic_decorators = CACHE['dynamic_decorators']
    sources = dynamic_decorators.set_default(dynamic_decorator, [])
    if source_decorator in sources:
        source_decorator.remove(source_decorator)
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
