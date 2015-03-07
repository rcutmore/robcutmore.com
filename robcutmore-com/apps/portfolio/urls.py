from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.project_list, name='project_list'),
    url(r'^(?P<tag>[\w\-]+)/$', views.project_list, name='project_list_filtered'),
)