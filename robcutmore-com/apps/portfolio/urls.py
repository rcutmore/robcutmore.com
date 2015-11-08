from django.conf.urls import url

from . import views


urlpatterns = [
    # Ex: /portfolio/
    # This lists all portfolio projects.
    url(r'^$',
        views.project_list,
        name='project_list'),

    # Ex: /portfolio/filter/
    # Used by Ajax calls to filter/unfilter list of portfolio projects.
    url(r'^filter/$',
        views.filter_project_list,
        name='filter_project_list'),

    # Ex: /portfolio/python/
    # This would list all portfolio projects with the "python" tag.
    url(r'^(?P<tag>[\w\-]+)/$',
        views.project_list,
        name='project_list_filtered'),
]
