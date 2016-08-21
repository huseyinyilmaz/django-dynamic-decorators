"""Dynamic decorators url configuration."""
from django.conf.urls import url
from dynamicdecorators import views
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='dynamicdecorators-index'),
]
