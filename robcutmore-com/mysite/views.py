"""
Contains main project views.
"""
from django.shortcuts import render


def about(request):
    """ Render HTML for about page.

    :param request: :class:`HttpRequest` object to generate response
        with.
    :returns: Rendered :class:`HttpResponse` object.
    """
    return render(request, 'about.html', {'active_page': 'about'})
