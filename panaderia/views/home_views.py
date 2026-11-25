from django.shortcuts import render

from panaderia.models import Categoria, Ingrediente, Pedido, Producto


def home(request):
    contexto = {
        "total_categorias": Categoria.objects.count(),
        "total_ingredientes": Ingrediente.objects.count(),
        "total_productos": Producto.objects.count(),
        "disponibles": Producto.objects.filter(disponible=True).count(),
        "pedidos_pendientes": Pedido.objects.exclude(estado=Pedido.Estado.ENTREGADO).count(),
        "ultimos_productos": Producto.objects.select_related("categoria").order_by("-creado_en")[:5],
        "categorias": Categoria.objects.prefetch_related("productos"),
    }
    return render(request, "panaderia/home.html", contexto)
