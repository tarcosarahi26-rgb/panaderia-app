from django import template

from panaderia.utils import permisos

register = template.Library()


@register.filter
def puede_editar(obj, user):
    return permisos.puede_editar(user, obj)


@register.filter
def puede_eliminar(obj, user):
    return permisos.puede_eliminar(user, obj)
