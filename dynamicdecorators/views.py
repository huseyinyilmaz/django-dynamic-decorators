"""Dynamic decorators views."""
from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import redirect

from dynamicdecorators import config
from dynamicdecorators import session


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
        enabled_slugs = {d['slug']
                         for d in session.get_enabled_decorators(slug)}
        provided_decorators = config.get_provided_decorators()
        for p in provided_decorators:
            p['enabled'] = (p['slug'] in enabled_slugs)
        ctx = {'decorators': config.get_registered_decorators(),
               'provided_decorators': provided_decorators,
               'slug': slug}
        return render(request, self.template_name, ctx)


class EnableView(View):
    def get(self, request, slug, decorator):
        session.enable_decorator(slug, decorator)
        return redirect('dynamicdecorators-detail', slug=slug)


class DisableView(View):
    def get(self, request, slug, decorator):
        session.disable_decorator(slug, decorator)
        return redirect('dynamicdecorators-detail', slug=slug)
