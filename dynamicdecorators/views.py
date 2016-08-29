"""Dynamic decorators views."""
from django.views.generic import View
from django.shortcuts import render

from dynamicdecorators import config


class IndexView(View):

    template_name = 'dynamicdecorators/index.html'

    def get(self, request):
        ctx = {'decorators': config.get_registered_decorators(),
               'provided_decorators': config.get_provided_decorators(),
               }
        return render(request, self.template_name, ctx)


class DetailView(View):

    template_name = 'dynamicdecorators/detail.html'

    def get(self, request, slug):
        ctx = {'decorators': config.get_registered_decorators(),
               'provided_decorators': config.get_provided_decorators(),
               'slug': slug}
        return render(request, self.template_name, ctx)
