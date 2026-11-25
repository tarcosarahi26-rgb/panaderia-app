from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from panaderia.forms import IngredienteForm
from panaderia.models import Ingrediente


def ingrediente_list(request):
    ingredientes = Ingrediente.objects.all()
    page_obj = Paginator(ingredientes, 10).get_page(request.GET.get("page"))
    return render(request, "panaderia/ingredientes/lista.html", {
        "ingredientes": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    })


def ingrediente_detail(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    return render(request, "panaderia/ingredientes/detalle.html", {
        "ingrediente": ingrediente,
        "productos": ingrediente.productos.select_related("categoria"),
    })


@login_required
@permission_required("panaderia.add_ingrediente", raise_exception=True)
def ingrediente_create(request):
    if request.method == "POST":
        form = IngredienteForm(request.POST)
        if form.is_valid():
            ingrediente = form.save()
            messages.success(request, "Ingrediente creado exitosamente.")
            return redirect(ingrediente)
    else:
        form = IngredienteForm()
    return render(request, "panaderia/ingredientes/formulario.html", {
        "form": form,
        "titulo": "Nuevo ingrediente",
    })


@login_required
@permission_required("panaderia.change_ingrediente", raise_exception=True)
def ingrediente_update(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    if request.method == "POST":
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingrediente actualizado exitosamente.")
            return redirect(ingrediente)
    else:
        form = IngredienteForm(instance=ingrediente)
    return render(request, "panaderia/ingredientes/formulario.html", {
        "form": form,
        "titulo": "Editar ingrediente",
    })


@login_required
@permission_required("panaderia.delete_ingrediente", raise_exception=True)
def ingrediente_delete(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    if request.method == "POST":
        ingrediente.delete()
        messages.success(request, "Ingrediente eliminado.")
        return redirect("panaderia:ingrediente_list")
    return render(request, "panaderia/ingredientes/confirmar_eliminar.html", {
        "ingrediente": ingrediente,
    })
