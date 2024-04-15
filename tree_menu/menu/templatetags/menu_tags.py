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
    request = context['request']
    path_parts = request.path.strip('/').split('/')

    items = MenuItem.objects.filter(menu_name=menu_name)

    """
       Раз уж нам надо ограничиться одним запросом к бд на одно меню, то мы не сможем работать с дочерними
       элементами через obj.children.all(), так как это новый запрос к бд, поэтому будем выгружать все
       записи, и формировать свое дерево уже в голом питоне
   """

    menu_items = {item.id: Menu(item.id, item.name, item.url, item.menu_name, item.parent_id) for item in items}
    for item in items:
        if item.parent_id:
            parent = menu_items.get(item.parent_id)
            if parent:
                parent.childrens.append(menu_items[item.id])

    root_items = [item for item in menu_items.values() if item.parent_id is None]
    return mark_safe(render_menu_items(root_items, path_parts))


# Клон модели

class Menu:
    def __init__(self, id, name, url, menu_name, parent_id=None):
        self.id = id
        self.name = name
        self.url = url
        self.menu_name = menu_name
        self.parent_id = parent_id
        self.childrens = []

    def get_absolute_url(self):
        return reverse('menu', kwargs={"menu_path": self.url})

    def __repr__(self):
        return f"{self.name}"
