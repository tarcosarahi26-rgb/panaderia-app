from django.contrib import admin

from panaderia.models import Categoria, Ingrediente, Pedido, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    list_filter = ("nombre",)


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "unidad", "stock", "fecha_caducidad")
    list_filter = ("unidad", "fecha_caducidad")
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "tipo_venta", "precio", "disponible", "creado_por")
    list_filter = ("categoria", "tipo_venta", "disponible")
    search_fields = ("nombre", "descripcion")
    filter_horizontal = ("ingredientes",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "producto", "cantidad", "estado", "fecha_entrega")
    list_filter = ("estado", "fecha_entrega")
    search_fields = ("cliente", "producto__nombre")
