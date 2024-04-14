from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from menu.models import MenuItem

register = template.Library()


def render_menu_items(items, path_parts):
    menu_html = '<ul>'
    for item in items:
        menu_html += f'<li><a href="{item.get_absolute_url()}">{item.name}</a>'
        if item.name in path_parts:
            child_items = item.childrens
            if child_items:
                menu_html += render_menu_items(child_items, path_parts)
        menu_html += '</li>'
    menu_html += '</ul>'
    return menu_html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    """
    Раз уж нам надо ограничиться одним запросом к бд на одно меню, то мы не сможем работать с дочерними
    элементами через obj.children.all(), так как это новый запрос к бд, поэтому будем выгружать все
    записи, и формировать свое дерево уже в голом питоне
    """

    objects = {item.name: Menu(item.name, item.url, item.menu_name) for item in items if item.parent is None}
    for item in items:
        if item.parent is not None:
            if item.parent.name in objects:
                parent = objects[item.parent.name]
                obj = Menu(item.name, item.url, item.menu_name, parent=parent)
                parent.childrens.append(obj)
                objects.update({item.name: obj})

    queryset = [obj for obj in objects.values() if obj.parent is None]

    request = context['request']
    path_parts = request.path.strip('/').split('/')
    return mark_safe(render_menu_items(queryset, path_parts))


# Класс-копия нашей модели. Если вдруг мы сможем вернутья к возможности работы через бд,
# рефакторинг кода не займет много времени

class Menu:
    def __init__(self, name, url, menu_name, parent=None):
        self.name = name
        self.url = url
        self.menu_name = menu_name
        self.parent = parent
        self.childrens = []

    def get_absolute_url(self):
        return reverse('menu', kwargs={"menu_path": self.url})

    def __repr__(self):
        return f"{self.name}"
