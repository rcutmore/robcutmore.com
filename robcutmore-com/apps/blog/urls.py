from django.conf.urls import url

from . import views


urlpatterns = [
    # Ex: /blog/
    # This lists all blog posts.
    url(r'^$',
        views.post_list,
        name='post_list'),

    # Ex: /blog/filter/
    # Used by Ajax calls to filter/unfilter list of blog posts.
    url(r'^filter/$',
        views.filter_post_list,
        name='filter_post_list'),

    # Ex: /blog/python/
    # This would list all blog posts with the "python" tag.
    url(r'^(?P<tag>[\w\-]+)/$',
        views.post_list,
        name='post_list_filtered'),

    # Ex: /blog/2015/8/27/example-blog-post/
    # This would show a particular blog post that was posted 2015/8/27.
    url(r'^(?P<post_year>[\d]+)/(?P<post_month>[\d]+)/(?P<post_day>[\d]+)/(?P<post_slug>[\w\-]+)/$',
        views.post_detail,
        name='post_detail'),
]
