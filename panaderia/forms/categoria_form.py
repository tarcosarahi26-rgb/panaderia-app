from django import forms

from panaderia.models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 letras.")
        return nombre.capitalize()
