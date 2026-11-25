from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from panaderia.forms import CategoriaForm
from panaderia.models import Categoria


def categoria_list(request):
    categorias = Categoria.objects.all()
    page_obj = Paginator(categorias, 10).get_page(request.GET.get("page"))
    return render(request, "panaderia/categorias/lista.html", {
        "categorias": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    })


def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    productos = categoria.productos.all()
    return render(request, "panaderia/categorias/detalle.html", {
        "categoria": categoria,
        "productos": productos,
    })


@login_required
@permission_required("panaderia.add_categoria", raise_exception=True)
def categoria_create(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect(categoria)
    else:
        form = CategoriaForm()
    return render(request, "panaderia/categorias/formulario.html", {
        "form": form,
        "titulo": "Nueva categoría",
    })


@login_required
@permission_required("panaderia.change_categoria", raise_exception=True)
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente.")
            return redirect(categoria)
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "panaderia/categorias/formulario.html", {
        "form": form,
        "titulo": "Editar categoría",
    })


@login_required
@permission_required("panaderia.delete_categoria", raise_exception=True)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        try:
            categoria.delete()
        except ProtectedError:
            messages.error(
                request,
                "No se puede borrar: la categoría todavía tiene productos. "
                "Bórralos o cámbialos de categoría primero.",
            )
            return redirect(categoria)
        messages.success(request, "Categoría eliminada.")
        return redirect("panaderia:categoria_list")
    return render(request, "panaderia/categorias/confirmar_eliminar.html", {
        "categoria": categoria,
    })
