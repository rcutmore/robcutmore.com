from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Project

register = template.Library()

@register.inclusion_tag('portfolio/projects.html')
def get_project_list(page=None, tag=None):
    if tag:
        all_projects = Project.objects.filter(tags__title=tag)
        filtered = True
    else:
        all_projects = Project.objects.all()
        filtered = False

    paginator = Paginator(all_projects, 5)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # page is not an integer so show the first page.
        projects = paginator.page(1)
    except EmptyPage:
        # page is higher than total number of pages so show last page.
        projects = paginator.page(paginator.num_pages)

    return {'projects': projects, 'filtered': filtered}