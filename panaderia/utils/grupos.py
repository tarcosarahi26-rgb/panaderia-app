from django.contrib.auth.models import Group, Permission

GRUPO_ADMIN = "administradores"
GRUPO_CONSULTOR = "consultores"

MODELOS = ["categoria", "ingrediente", "producto", "pedido"]


def crear_grupos():
    """Crea los grupos y les asigna permisos. Se puede ejecutar muchas veces."""
    permisos_app = Permission.objects.filter(content_type__app_label="panaderia")

    administradores, _ = Group.objects.get_or_create(name=GRUPO_ADMIN)
    administradores.permissions.set(permisos_app)

    codenames = [f"view_{m}" for m in MODELOS] + [
        "add_producto",
        "change_producto",
        "delete_producto",
    ]
    consultores, _ = Group.objects.get_or_create(name=GRUPO_CONSULTOR)
    consultores.permissions.set(permisos_app.filter(codename__in=codenames))
    return administradores, consultores
