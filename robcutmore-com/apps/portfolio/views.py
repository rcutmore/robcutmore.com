from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import Project
from .templatetags.portfolio_tags import get_project_list

def project_list(request):
    page = request.GET.get('page', '')
    context_dict = {
        'active_page': 'portfolio',
        'page': page,
    }

    return render(request, 'portfolio/project_list.html', context_dict)

def project_list_filtered(request):
    tag = request.GET.get('tag', '')
    context_dict = get_project_list(1, tag)

    return render(request, 'portfolio/projects.html', context_dict)