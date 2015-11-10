"""
Contains custom templatetags for blog app.
"""
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Post


register = template.Library()


@register.inclusion_tag('blog/posts.html')
def get_post_list(page=None, tag=None):
    """Fetch posts for given page and tag.

    :param page: Page number of posts to fetch. Default is None which
        fetches the first page of posts.
    :param tag: Tag to use for filtering posts. Default is None which
        fetches all posts.
    :returns: Dictionary containing posts, tag, and whether or not
        posts are filtered for a tag.
    """
    # Filter posts if given valid tag otherwise get all posts.
    if tag:
        all_posts = Post.objects.filter(published_date__isnull=False,
                                        tags__title=tag)
        filtered = True
    else:
        all_posts = Post.objects.filter(published_date__isnull=False)
        filtered = False

    # Show 5 posts per page.
    # Determine which posts to show based on given page.
    paginator = Paginator(all_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # page is not an integer so show the first page.
        posts = paginator.page(1)
    except EmptyPage:
        # page is higher than total number of pages so show last page.
        posts = paginator.page(paginator.num_pages)

    return {'posts': posts, 'tag': tag, 'filtered': filtered}
