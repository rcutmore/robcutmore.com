from datetime import date

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render

from .models import Post

def post_list(request):
    all_posts = Post.objects.filter(published_date__isnull=False)
    paginator = Paginator(all_posts, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # page is not an integer so show the first page.
        posts = paginator.page(1)
    except EmptyPage:
        # page is higher than total number of pages so show last page.
        posts = paginator.page(paginator.num_pages)

    context_dict = {'posts': posts, 'active_page': 'blog'}

    return render(request, 'blog/post_list.html', context_dict)

def post_detail(request, post_month, post_day, post_year, post_slug):
    published_date = date(int(post_year), int(post_month), int(post_day))
    post = get_object_or_404(
        Post, slug=post_slug, published_date__contains=published_date)

    context_dict = {'post': post, 'active_page': 'blog'}

    return render(request, 'blog/post_detail.html', context_dict)