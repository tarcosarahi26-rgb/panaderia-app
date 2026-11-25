from datetime import date

from django.conf import settings
from django.db import models
from django.urls import reverse


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        EN_HORNO = "EN_HORNO", "En el horno"
        LISTO = "LISTO", "Listo para entregar"
        ENTREGADO = "ENTREGADO", "Entregado"

    cliente = models.CharField(max_length=100)
    # PROTECT: un producto con pedidos registrados no se puede borrar.
    producto = models.ForeignKey(
        "panaderia.Producto",
        on_delete=models.PROTECT,
        related_name="pedidos",
    )
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(
        max_length=10, choices=Estado.choices, default=Estado.PENDIENTE
    )
    fecha_pedido = models.DateField("fecha del pedido", default=date.today)
    fecha_entrega = models.DateField("fecha de entrega")
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos_creados",
    )

    class Meta:
        ordering = ["-fecha_pedido", "-id"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return f"Pedido #{self.pk} de {self.cliente}"

    @property
    def total(self):
        return self.producto.precio * self.cantidad

    def get_absolute_url(self):
        return reverse("panaderia:pedido_detail", kwargs={"pk": self.pk})
