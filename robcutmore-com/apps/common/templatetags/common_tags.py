"""
Contains custom project-wide templatetags.
"""
from django import template

import markdown


register = template.Library()


@register.filter
def markdownify(markdown_text):
    """Render Markdown for template.

    :param markdown_text: Markdown text to render.
    :returns: Rendered Markdown.
    """
    extensions = [
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.nl2br',
    ]
    return markdown.markdown(markdown_text, extensions=extensions)
