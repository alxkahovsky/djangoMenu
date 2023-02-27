from django import template
from menu.models import MenuItem, Menu
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_slug):
    if context.request.GET:
        selected = context.request.GET['selected']
    else:
        selected = None
    out = ''
    # menu = Menu.objects.filter(slug=menu_slug).order_by('-id')
    out += '<ul class="menu">'
    for menu_main_items in MenuItem.objects.select_related('menu').filter(menu__slug=menu_slug, is_active=True,):
        out += '<li class="menu-item" >'
        out += f'<a href="{menu_main_items.get_absolute_url(context.request)}">{menu_main_items.title}</a>'
        if selected == menu_main_items.slug:
            out += draw_menu_parents(context, menu_main_items)
            out += draw_menu_children(context, menu_main_items)
        # out += draw_menu_children(menu_main_items, selected)
        out += '</li>'
    out += '</ul>'
    return mark_safe(out)


def draw_menu_children(context, menu_item):
    out = ''
    #drawing the sub items
    out += '<ul class="submenu">'
    for submenu_item in menu_item.children.all().order_by('-id'):
        out += '<li class="menu-item" >'
        # out += '<a href="{0}">{1}</a>'.format(submenu_item.url, submenu_item.label)
        out += f'<a href="{submenu_item.get_absolute_url(context.request)}">{submenu_item.title}</a>'
        # out += draw_menu_children(submenu_item)
        out += '</li>'
    out += '</ul>'
    return out


def draw_menu_parents(context, menu_item):
    out = ''
    # drawing the sub items
    out += '<ul class="submenu">'
    print(menu_item.slug)
    for submenu_item in MenuItem.objects.filter(children__slug=menu_item.slug):
        print(submenu_item)
        out += '<li class="menu-item" >'
        out += f'<a href="{submenu_item.get_absolute_url(context.request)}">{submenu_item.title}</a>'
        out += '</li>'
    out += '</ul>'
    return out


