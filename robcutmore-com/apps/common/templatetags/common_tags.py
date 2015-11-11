"""
Contains custom project-wide templatetags.
"""
from django import template

from markdown import markdown


register = template.Library()


@register.filter
def markdownify(markdown_text):
    """Render Markdown for template.

    :param markdown_text: Markdown text to render.
    :returns: Rendered Markdown.
    """
    return markdown(markdown_text)
