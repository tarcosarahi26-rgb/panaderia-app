from django import forms

from panaderia.models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "categoria",
            "nombre",
            "descripcion",
            "precio",
            "tipo_venta",
            "ingredientes",
            "fecha_elaboracion",
            "disponible",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "precio": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "ingredientes": forms.CheckboxSelectMultiple(),
            "fecha_elaboracion": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio
