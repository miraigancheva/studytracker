from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def letter_badge(percentage):
    p = float(percentage)
    if p >= 90:
        return mark_safe('<span class="badge bg-success">A</span>')
    elif p >= 75:
        return mark_safe('<span class="badge bg-success">B</span>')
    elif p >= 60:
        return mark_safe('<span class="badge bg-warning text-dark">C</span>')
    elif p >= 50:
        return mark_safe('<span class="badge bg-warning text-dark">D</span>')
    return mark_safe('<span class="badge bg-danger">F</span>')


@register.filter
def passed_label(passed):
    if passed:
        return mark_safe('<span class="text-success">Passed</span>')
    return mark_safe('<span class="text-danger">Failed</span>')
