"""Dynamic decorator middlewares."""
from dynamicdecorators import config
from dynamicdecorators.decorator import decorate


def dynamicdecorators_middleware(get_response):
    # One-time configuration and initialization.
    # config.register('all')

    @decorate('all')
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
    return middleware


# class DynamicDecoratorsMiddleware(object):

#     """Middleware for Dynamic Decorators"""

#     def __init__(self, *args, **kwargs):
#         config.register('all')
#         import ipdb; ipdb.set_trace()
#         print 1
#         return None

#     def process_view(self, request, view, view_args, view_kwargs):
#         return None
