from django.urls import path

from panaderia import views

# Las rutas fijas (nueva/) van antes que las dinámicas (<int:pk>/).
urlpatterns = [
    path("pedidos/", views.pedido_list, name="pedido_list"),
    path("pedidos/nueva/", views.pedido_create, name="pedido_create"),
    path("pedidos/<int:pk>/", views.pedido_detail, name="pedido_detail"),
    path("pedidos/<int:pk>/editar/", views.pedido_update, name="pedido_update"),
    path("pedidos/<int:pk>/borrar/", views.pedido_delete, name="pedido_delete"),
]
