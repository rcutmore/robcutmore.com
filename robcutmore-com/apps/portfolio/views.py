from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import Project
from .templatetags.portfolio_tags import get_project_list

def project_list(request, tag=''):
    page = request.GET.get('page', '')
    context_dict = {
        'active_page': 'portfolio',
        'page': page,
        'tag': tag,
    }

    return render(request, 'portfolio/project_list.html', context_dict)

def filter_project_list(request):
    tag = request.GET.get('tag', '')
    page = request.GET.get('page', 1)

    context_dict = get_project_list(page, tag)

    return render(request, 'portfolio/projects.html', context_dict)