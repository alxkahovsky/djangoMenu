from django import template
from menu.models import MenuItem, Menu
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_slug):
    menu_items = MenuItem.objects.filter(menu__slug=menu_slug)
    menu_parents = menu_items.filter(parent=None)
    if context.request.GET:
        print(context.request.GET)
        selected = context.request.GET['selected']
        selected_item = menu_items.get(slug=selected)
        branch_path = list(reversed(get_grandparents(selected_item, context)))
    else:
        selected = None
    out = ''
    out += f'<h2>{menu_slug}:</h2>'
    out += '<ul class="menu">'
    for menu_parent_item in menu_parents:
        if selected:
            if menu_parent_item == branch_path[0]:
                out += draw_branch(branch_path, context)
            else:
                out += '<li class="menu-item">'
                out += f'<a href="{menu_parent_item.get_absolute_url(context.request)}">{menu_parent_item.title}</a>'
        else:
            out += '<li class="menu-item">'
            out += f'<a href="{menu_parent_item.get_absolute_url(context.request)}">{menu_parent_item.title}</a>'
    return mark_safe(out)


def draw_menu_children(context, menu_item):
    out = ''
    out += '<ul class="submenu">'
    for submenu_item in menu_item.children.all().order_by('id'):
        out += '<li class="menu-item" >'
        out += f'<a href="{submenu_item.get_absolute_url(context.request)}">{submenu_item.title}</a>'
        out += '</li>'
    return out


def get_grandparents(selected_item, context):
    result = [selected_item]
    if selected_item.parent:
        result.extend(get_grandparents(selected_item.parent, context))
    return result


def draw_branch(path, context):
    out = f"""<li class="menu-item"><a href="{path[0].get_absolute_url(context.request)}">{path[0].title}</a>"""
    for p in path[1:]:
        out += '<ul class="submenu">'
        out += '<li class="menu-item" >'
        out += f'<a href="{p.get_absolute_url(context.request)}">{p.title}</a>'
    out += draw_menu_children(context, path[-1])
    out += len(path)*'</ul>'
    return out
