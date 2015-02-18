from django import template

from markdown import markdown

register = template.Library()

@register.filter
def markdownify(markdown_text):
    """Render markdown_text for template."""
    return markdown(markdown_text)