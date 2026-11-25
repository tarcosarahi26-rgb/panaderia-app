from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _crear_grupos(sender, **kwargs):
    """Después de cada migrate deja listos los grupos y sus permisos."""
    from django.contrib.auth.management import create_permissions

    create_permissions(sender, verbosity=0)
    from panaderia.utils.grupos import crear_grupos

    crear_grupos()


class PanaderiaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "panaderia"
    verbose_name = "Panadería"

    def ready(self):
        post_migrate.connect(_crear_grupos, sender=self)
