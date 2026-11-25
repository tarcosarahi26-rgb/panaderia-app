from datetime import date

from django import forms

from panaderia.models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["cliente", "producto", "cantidad", "estado", "fecha_entrega"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"min": "1"}),
            "fecha_entrega": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]
        if cantidad < 1:
            raise forms.ValidationError("La cantidad mínima es 1.")
        return cantidad

    def clean_fecha_entrega(self):
        fecha = self.cleaned_data["fecha_entrega"]
        if not self.instance.pk and fecha < date.today():
            raise forms.ValidationError("La fecha de entrega no puede estar en el pasado.")
        return fecha
