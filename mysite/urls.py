from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', include('apps.blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', 'mysite.views.about', name='about'),
    url(r'^blog/', include('apps.blog.urls')),
    url(r'^portfolio/', include('apps.portfolio.urls')),
)