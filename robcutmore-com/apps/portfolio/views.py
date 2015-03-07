from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import Project

def project_list(request, tag=None):
    if tag:
        all_projects = Project.objects.filter(tags__title=tag)
    else:
        all_projects = Project.objects.all()
    paginator = Paginator(all_projects, 5)

    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # page is not an integer so show the first page.
        projects = paginator.page(1)
    except EmptyPage:
        # page is higher than total number of pages so show last page.
        projects = paginator.page(paginator.num_pages)

    context_dict = {'projects': projects, 'active_page': 'portfolio'}

    return render(request, 'portfolio/project_list.html', context_dict)