"""Dynamic decorators views."""
from django.views.generic import View
from django.shortcuts import render

from dynamicdecorators import config


class IndexView(View):

    template_name = 'dynamicdecorators/index.html'

    def get(self, request):
        ctx = {'decorators': config.get_registered_decorators()}
        return render(request, self.template_name, ctx)
