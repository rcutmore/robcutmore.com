"""
Contains views for blog app.
"""
from datetime import date

from django.shortcuts import get_object_or_404, render

from .models import Post
from .templatetags.blog_tags import get_post_list


def post_list(request, tag=''):
    """Render HTML for page containing blog post list.

    Uses GET request parameter to determine which page number to
    display.

    :param request: :class:`HttpRequest` object to generate response
        with.
    :param tag: Tag to use for filtering posts. Default is empty string
        which displays all posts.
    :returns: Rendered :class:`HttpResponse` object.
    """
    page = request.GET.get('page', '')
    context_dict = {
        'active_page': 'blog',
        'page': page,
        'tag': tag,
    }
    return render(request, 'blog/post_list.html', context_dict)


def post_detail(request, post_month, post_day, post_year, post_slug):
    """Render HTML for page containing single blog post.

    :param request: :class:`HttpRequest` object to generate response
        with.
    :param post_month: Month of post.
    :param post_day: Day of post.
    :param post_year: Year of post.
    :param post_slug: Post's slug.
    :returns: Rendered :class:`HttpResponse` object.
    """
    published_date = date(int(post_year), int(post_month), int(post_day))
    post = get_object_or_404(
        Post, slug=post_slug, published_date__contains=published_date)
    context_dict = {'post': post, 'active_page': 'blog'}
    return render(request, 'blog/post_detail.html', context_dict)


def filter_post_list(request):
    """Render HTML only for blog post list (not entire page).

    Uses GET request parameters to determine tag to filter posts for and
    page number to display.

    :param request: :class:`HttpRequest` object to generate response
        with.
    :returns: Rendered :class:`HttpResponse` object.
    """
    tag = request.GET.get('tag', '')
    page = request.GET.get('page', 1)
    context_dict = get_post_list(page, tag)
    return render(request, 'blog/posts.html', context_dict)
