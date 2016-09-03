"""Dynamic decorators views."""
from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import redirect

from dynamicdecorators import config
from dynamicdecorators import session


def get_general_context():
    return {'decorators': [(d, len(session.get_enabled_decorators(d)))
                           for d in config.get_registered_decorators()],
    }


class IndexView(View):

    template_name = 'dynamicdecorators/index.html'

    def get(self, request):
        ctx = get_general_context()
        return render(request, self.template_name, ctx)


class DetailView(View):

    template_name = 'dynamicdecorators/detail.html'

    def get(self, request, slug):
        enabled_slugs = {d['slug']
                         for d in session.get_enabled_decorators(slug)}
        provided_decorators = config.get_provided_decorators()
        for p in provided_decorators:
            p['enabled'] = (p['slug'] in enabled_slugs)
        ctx = get_general_context()
        ctx.update({'slug': slug,
                    'generic_keys': ['function', 'enabled', 'name', 'slug'],
                    'provided_decorators': provided_decorators,
        })
        print '-' * 80
        print 'ctx'
        print ctx
        print '-' * 80
        print 'enabled_slugs'
        print enabled_slugs
        print '-' * 80
        print 'provided_decorators'
        print provided_decorators
        print '-' * 80

        return render(request, self.template_name, ctx)


class EnableView(View):
    def get(self, request, slug, decorator):
        session.enable_decorator(slug, decorator)
        return redirect('dynamicdecorators-detail', slug=slug)


class DisableView(View):
    def get(self, request, slug, decorator):
        session.disable_decorator(slug, decorator)
        return redirect('dynamicdecorators-detail', slug=slug)
