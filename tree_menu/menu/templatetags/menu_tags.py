from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from menu.models import MenuItem

register = template.Library()


def render_menu_items(items, path_parts):
    menu_html = '<ul>'
    for item in items:
        menu_html += f'<li><a href="{item.get_absolute_url()}">{item.name}</a>'
        # Если текущий пункт меню присутствует в пути, рекурсивно рендерим его дочерние элементы
        if item.name in path_parts:
            child_items = item.children.all()
            if child_items:
                menu_html += render_menu_items(child_items, path_parts)
        menu_html += '</li>'
    menu_html += '</ul>'
    return menu_html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    items = MenuItem.objects.filter(menu_name=menu_name, parent=None).select_related('parent')
    request = context['request']
    path_parts = request.path.strip('/').split('/')
    return mark_safe(render_menu_items(items, path_parts))
