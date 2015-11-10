"""
Contains views for portfolio app.
"""
from django.shortcuts import render

from .templatetags.portfolio_tags import get_project_list


def project_list(request, tag=''):
    """Render HTML for page containing portfolio project list.

    Uses GET request parameter to determine which page number to
    display.

    :param request: :class:`HttpRequest` object to generate response
        with.
    :param tag: Tag to use for filtering projects. Default is empty
        string which displays all projects.
    :returns: Rendered :class:`HttpResponse` object.
    """
    page = request.GET.get('page', '')
    context_dict = {
        'active_page': 'portfolio',
        'page': page,
        'tag': tag,
    }
    return render(request, 'portfolio/project_list.html', context_dict)


def filter_project_list(request):
    """Render HTML only for portfolio project list (not entire page).

    Uses GET request parameters to determine tag to filter projects for
    and page number to display.

    :param request: :class:`HttpRequest` object to generate response
        with.
    :returns: Rendered :class:`HttpResponse` object.
    """
    tag = request.GET.get('tag', '')
    page = request.GET.get('page', 1)
    context_dict = get_project_list(page, tag)
    return render(request, 'portfolio/projects.html', context_dict)
