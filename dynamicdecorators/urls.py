"""Dynamic decorators url configuration."""
from django.conf.urls import url
from dynamicdecorators import views
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='dynamicdecorators-index'),
    url(r'^(?P<slug>[\w-]+)/$', views.DetailView.as_view(),
        name="dynamicdecorators-detail"),
    url(r'^(?P<slug>[\w-]+)/enable/(?P<decorator>[\w-]+)$',
        views.EnableView.as_view(),
        name="dynamicdecorators-enable"),
    url(r'^(?P<slug>[\w-]+)/disable/(?P<decorator>[\w-]+)$',
        views.DisableView.as_view(),
        name="dynamicdecorators-disable"),
]
