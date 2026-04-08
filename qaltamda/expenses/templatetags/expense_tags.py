from django import template

register = template.Library()

@register.simple_tag
def param_replace(request, **kwargs):
    """
    Заменяет или добавляет параметры в текущий GET запрос.
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, None)
    return updated.urlencode()