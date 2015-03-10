from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.project_list, name='project_list'),
    url(r'^filter/$', views.project_list_filtered, name='project_list_filtered'),
)