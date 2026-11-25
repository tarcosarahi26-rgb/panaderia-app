from django.db import models
from django.urls import reverse


class Ingrediente(models.Model):
    class Unidad(models.TextChoices):
        KILOGRAMO = "KG", "Kilogramo"
        LITRO = "L", "Litro"
        UNIDAD = "U", "Unidad"

    nombre = models.CharField(max_length=80, unique=True)
    unidad = models.CharField(
        max_length=2, choices=Unidad.choices, default=Unidad.KILOGRAMO
    )
    stock = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha_caducidad = models.DateField("fecha de caducidad", null=True, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "ingrediente"
        verbose_name_plural = "ingredientes"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("panaderia:ingrediente_detail", kwargs={"pk": self.pk})
