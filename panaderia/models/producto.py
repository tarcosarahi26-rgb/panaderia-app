from datetime import date

from django.conf import settings
from django.db import models
from django.urls import reverse


class Producto(models.Model):
    class TipoVenta(models.TextChoices):
        UNIDAD = "UNIDAD", "Por unidad"
        DOCENA = "DOCENA", "Por docena"
        PORCION = "PORCION", "Por porción"

    nombre = models.CharField(max_length=80)
    descripcion = models.TextField("descripción", blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    tipo_venta = models.CharField(
        "tipo de venta",
        max_length=10,
        choices=TipoVenta.choices,
        default=TipoVenta.UNIDAD,
    )
    fecha_elaboracion = models.DateField("fecha de elaboración", default=date.today)
    disponible = models.BooleanField(default=True)
    # PROTECT: no se puede borrar una categoría mientras tenga productos.
    categoria = models.ForeignKey(
        "panaderia.Categoria",
        on_delete=models.PROTECT,
        related_name="productos",
    )
    # Un producto lleva varios ingredientes y un ingrediente está en varios productos.
    ingredientes = models.ManyToManyField(
        "panaderia.Ingrediente",
        related_name="productos",
        blank=True,
    )
    # SET_NULL: si se borra el usuario, el producto sigue existiendo.
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos_creados",
    )
    creado_en = models.DateTimeField("creado en", auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_venta_display()})"

    def get_absolute_url(self):
        return reverse("panaderia:producto_detail", kwargs={"pk": self.pk})
