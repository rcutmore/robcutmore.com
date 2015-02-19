from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Post

def post_list(request):
    all_posts = Post.objects.filter(
        published_date__isnull=False).order_by('-published_date')
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