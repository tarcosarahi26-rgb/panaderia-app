from panaderia.utils.grupos import GRUPO_ADMIN


def es_administrador(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=GRUPO_ADMIN).exists()
    )


def _tiene_permiso(user, accion, obj):
    return user.has_perm(f"{obj._meta.app_label}.{accion}_{obj._meta.model_name}")


def es_propietario(user, obj):
    return getattr(obj, "creado_por_id", None) == user.id


def puede_editar(user, obj):
    """Permiso change_* + regla de propiedad (los administradores se saltan la regla)."""
    if not user.is_authenticated or not _tiene_permiso(user, "change", obj):
        return False
    return es_administrador(user) or es_propietario(user, obj)


def puede_eliminar(user, obj):
    if not user.is_authenticated or not _tiene_permiso(user, "delete", obj):
        return False
    return es_administrador(user) or es_propietario(user, obj)
