from datetime import date

from django.shortcuts import get_object_or_404, render

from .models import Post
from .templatetags.blog_tags import get_post_list

def post_list(request, tag=''):
    page = request.GET.get('page', '')
    context_dict = {
        'active_page': 'blog',
        'page': page,
        'tag': tag,
    }
    
    return render(request, 'blog/post_list.html', context_dict)

def post_detail(request, post_month, post_day, post_year, post_slug):
    published_date = date(int(post_year), int(post_month), int(post_day))
    post = get_object_or_404(
        Post, slug=post_slug, published_date__contains=published_date)

    context_dict = {'post': post, 'active_page': 'blog'}

    return render(request, 'blog/post_detail.html', context_dict)

def filter_post_list(request):
    tag = request.GET.get('tag', '')
    page = request.GET.get('page', 1)
    
    context_dict = get_post_list(page, tag)

    return render(request, 'blog/posts.html', context_dict)