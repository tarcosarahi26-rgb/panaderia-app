from datetime import date

from django import forms

from panaderia.models import Ingrediente


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ["nombre", "unidad", "stock", "fecha_caducidad"]
        widgets = {
            "stock": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "fecha_caducidad": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }

    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock

    def clean_fecha_caducidad(self):
        fecha = self.cleaned_data["fecha_caducidad"]
        if fecha and fecha < date.today():
            raise forms.ValidationError("El ingrediente ya está caducado.")
        return fecha
