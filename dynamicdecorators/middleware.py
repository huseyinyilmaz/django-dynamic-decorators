"""Dynamic decorator middlewares."""
# from dynamicdecorators import config
# from dynamicdecorators import decorators
from dynamicdecorators import decorate
from dynamicdecorators import session


def dynamicdecorators_middleware(get_response):
    @session.request_store
    @decorate(name='all', slug='dynamic_decorators_middleware')
    def middleware(request):
        return get_response(request)
    return middleware
