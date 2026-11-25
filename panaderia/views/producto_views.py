from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render

from panaderia.forms import ProductoForm
from panaderia.models import Categoria, Producto
from panaderia.utils.permisos import puede_editar, puede_eliminar


def producto_list(request):
    productos = Producto.objects.select_related("categoria")

    # Filtros opcionales por query string: ?categoria=<id>&q=texto
    categoria_id = request.GET.get("categoria", "")
    if categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)
    q = request.GET.get("q", "").strip()
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    page_obj = Paginator(productos, 10).get_page(request.GET.get("page"))
    return render(request, "panaderia/productos/lista.html", {
        "productos": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "categorias": Categoria.objects.all(),
        "categoria_id": categoria_id,
        "q": q,
    })


def producto_detail(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria", "creado_por"), pk=pk
    )
    return render(request, "panaderia/productos/detalle.html", {
        "producto": producto,
        "ingredientes": producto.ingredientes.all(),
        "pedidos": producto.pedidos.all(),
    })


@login_required
@permission_required("panaderia.add_producto", raise_exception=True)
def producto_create(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado_por = request.user
            producto.save()
            form.save_m2m()  # necesario por el ManyToMany de ingredientes
            messages.success(request, "Producto creado exitosamente.")
            return redirect(producto)
    else:
        form = ProductoForm()
    return render(request, "panaderia/productos/formulario.html", {
        "form": form,
        "titulo": "Nuevo producto",
    })


@login_required
@permission_required("panaderia.change_producto", raise_exception=True)
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    # Regla de propiedad: solo el creador (o un administrador) puede editar.
    if not puede_editar(request.user, producto):
        raise PermissionDenied
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente.")
            return redirect(producto)
    else:
        form = ProductoForm(instance=producto)
    return render(request, "panaderia/productos/formulario.html", {
        "form": form,
        "titulo": "Editar producto",
    })


@login_required
@permission_required("panaderia.delete_producto", raise_exception=True)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if not puede_eliminar(request.user, producto):
        raise PermissionDenied
    if request.method == "POST":
        try:
            producto.delete()
        except ProtectedError:
            messages.error(
                request,
                "No se puede borrar: el producto tiene pedidos registrados.",
            )
            return redirect(producto)
        messages.success(request, "Producto eliminado.")
        return redirect("panaderia:producto_list")
    return render(request, "panaderia/productos/confirmar_eliminar.html", {
        "producto": producto,
    })
