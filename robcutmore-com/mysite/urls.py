from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.about', name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^portfolio/', include('apps.portfolio.urls', namespace='portfolio')),
)