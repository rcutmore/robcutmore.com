"""
Contains custom templatetags for portfolio app.
"""
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Project


register = template.Library()


@register.inclusion_tag('portfolio/projects.html')
def get_project_list(page=None, tag=None):
    """Fetch projects for given page and tag.

    :param page: Page number of projects to fetch. Default is None which
        fetches the first page of projects.
    :param tag: Tag to use for filtering projects. Default is None which
        fetches all projects.
    :returns: Dictionary containing projects, tag, and whether or not
        projects are filtered for a tag.
    """
    # Filter projects if given valid tag otherwise get all projects.
    if tag:
        all_projects = Project.objects.filter(tags__title=tag)
        filtered = True
    else:
        all_projects = Project.objects.all()
        filtered = False

    # Show 5 projects per page.
    # Determine which projects to show based on given page.
    paginator = Paginator(all_projects, 5)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # page is not an integer so show the first page.
        projects = paginator.page(1)
    except EmptyPage:
        # page is higher than total number of pages so show last page.
        projects = paginator.page(paginator.num_pages)

    return {'projects': projects, 'tag': tag, 'filtered': filtered}
