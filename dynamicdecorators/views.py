"""Dynamic decorators views."""
from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import redirect

from dynamicdecorators import config
from dynamicdecorators import session
from operator import attrgetter


def get_general_context():
    """Get base template context for all views."""
    return {'pipelines': [(d, len(session.get_enabled_decorators(d.slug)))
                          for d in sorted(config.get_pipelines(),
                                          key=attrgetter('slug'))],
            }


class IndexView(View):
    """Index view."""

    template_name = 'dynamicdecorators/index.html'

    def get(self, request):
        """Get index view."""
        ctx = get_general_context()
        return render(request, self.template_name, ctx)


class DetailView(View):
    """Detail for pipeline."""

    template_name = 'dynamicdecorators/detail.html'

    def get(self, request, slug):
        """Get detail for pipeline."""
        pipeline = config.get_pipeline_by_slug(slug)
        enabled_slugs = {d.slug for d in session.get_enabled_decorators(slug)}
        pipes = config.filter_pipes(pipeline, config.get_pipes())
        for p in pipes:
            p.enabled = p.slug in enabled_slugs
        ctx = get_general_context()
        ctx.update({'slug': slug,
                    'pipes': pipes,
                    'pipeline': pipeline})
        print('-' * 80)
        print('ctx')
        print(ctx)
        print('-' * 80)
        print('enabled_slugs')
        print(enabled_slugs)
        print('-' * 80)
        print('pipes')
        print(pipes)
        print('-' * 80)

        return render(request, self.template_name, ctx)


class EnableView(View):
    """Enable given pipe for given pipeline."""

    def get(self, request, slug, decorator):
        """Get method."""
        session.enable_decorator(slug, decorator)
        return redirect('dynamicdecorators-detail', slug=slug)


class DisableView(View):
    """Disable given pipe for given pipeline."""

    def get(self, request, slug, decorator):
        """Get method."""
        session.disable_decorator(slug, decorator)
        return redirect('dynamicdecorators-detail', slug=slug)
