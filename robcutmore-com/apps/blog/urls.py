from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.post_list, name='post_list'),
    url(r'^filter/$', views.post_list_filtered, name='post_list_filtered'),
    url(r'^(?P<post_year>[\d]+)/(?P<post_month>[\d]+)/(?P<post_day>[\d]+)/(?P<post_slug>[\w\-]+)/$', views.post_detail, name='post_detail'),
)