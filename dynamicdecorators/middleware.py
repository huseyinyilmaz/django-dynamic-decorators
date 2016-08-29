"""Dynamic decorator middlewares."""
# from dynamicdecorators import config
from dynamicdecorators import decorators
from dynamicdecorators import session


def dynamicdecorators_middleware(get_response):
    # One-time configuration and initialization.
    # config.register('all')

    @session.request_store
    @decorators.dynamic_decorators_middleware
    def middleware(request):
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
