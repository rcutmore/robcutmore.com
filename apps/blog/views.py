from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.filter(
        published_date__isnull=False).order_by('published_date')
    context_dict = {'posts': posts, 'active_page': 'blog'}

    return render(request, 'blog/post_list.html', context_dict)