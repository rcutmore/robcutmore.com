"""
Contains main project URLs.
"""
from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
    # This is the main page which is an about page.
    url(r'^$',
        views.about,
        name='about'),

    # All admin URLs.
    url(r'^admin/',
        include(admin.site.urls)),

    # All blog app URLs.
    url(r'^blog/',
        include('apps.blog.urls', namespace='blog')),

    # All portfolio app URLs.
    url(r'^portfolio/',
        include('apps.portfolio.urls', namespace='portfolio')),
]
