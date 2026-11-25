from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from panaderia.forms import PedidoForm
from panaderia.models import Pedido
from panaderia.utils.permisos import puede_editar, puede_eliminar


def pedido_list(request):
    pedidos = Pedido.objects.select_related("producto", "producto__categoria")
    estado = request.GET.get("estado", "")
    if estado in Pedido.Estado.values:
        pedidos = pedidos.filter(estado=estado)
    page_obj = Paginator(pedidos, 10).get_page(request.GET.get("page"))
    return render(request, "panaderia/pedidos/lista.html", {
        "pedidos": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "estados": Pedido.Estado.choices,
        "estado": estado,
    })


def pedido_detail(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("producto", "producto__categoria", "creado_por"),
        pk=pk,
    )
    return render(request, "panaderia/pedidos/detalle.html", {"pedido": pedido})


@login_required
@permission_required("panaderia.add_pedido", raise_exception=True)
def pedido_create(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.creado_por = request.user
            pedido.save()
            messages.success(request, "Pedido creado exitosamente.")
            return redirect(pedido)
    else:
        form = PedidoForm()
    return render(request, "panaderia/pedidos/formulario.html", {
        "form": form,
        "titulo": "Nuevo pedido",
    })


@login_required
@permission_required("panaderia.change_pedido", raise_exception=True)
def pedido_update(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if not puede_editar(request.user, pedido):
        raise PermissionDenied
    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido actualizado exitosamente.")
            return redirect(pedido)
    else:
        form = PedidoForm(instance=pedido)
    return render(request, "panaderia/pedidos/formulario.html", {
        "form": form,
        "titulo": "Editar pedido",
    })


@login_required
@permission_required("panaderia.delete_pedido", raise_exception=True)
def pedido_delete(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if not puede_eliminar(request.user, pedido):
        raise PermissionDenied
    if request.method == "POST":
        pedido.delete()
        messages.success(request, "Pedido eliminado.")
        return redirect("panaderia:pedido_list")
    return render(request, "panaderia/pedidos/confirmar_eliminar.html", {"pedido": pedido})
