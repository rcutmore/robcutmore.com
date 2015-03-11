from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/posts.html')
def get_post_list(page=None, tag=None):
    if tag:
        all_posts = Post.objects.filter(published_date__isnull=False, tags__title=tag)
        filtered = True
    else:
        all_posts = Post.objects.filter(published_date__isnull=False)
        filtered = False

    paginator = Paginator(all_posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # page is not an integer so show the first page.
        posts = paginator.page(1)
    except EmptyPage:
        # page is higher than total number of pages so show last page.
        posts = paginator.page(paginator.num_pages)

    return {'posts': posts, 'filtered': filtered}