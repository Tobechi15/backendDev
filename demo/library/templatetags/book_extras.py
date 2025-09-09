from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="truncate_with_toggle")
def truncate_with_toggle(value, arg=20):
    """
    Truncates the text to 'arg' characters and adds a Read more/less toggle.
    Usage: {{ book.description|truncate_with_toggle:200 }}
    """
    if not value:
        return ""

    if len(value) <= int(arg):
        return value

    short_text = value[:int(arg)] + "..."
    full_text = value

    html = f"""
    <span class="short-text">{short_text}</span>
    <span class="full-text hidden opacity-0 transition-opacity duration-300 ease-in-out">{full_text}</span>
    <button class="read-more text-black-500  ml-1">Read more</button>
    """

    return mark_safe(html)
