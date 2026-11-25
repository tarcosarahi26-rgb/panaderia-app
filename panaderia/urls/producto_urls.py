from django.urls import path

from panaderia import views

# Las rutas fijas (nueva/) van antes que las dinámicas (<int:pk>/).
urlpatterns = [
    path("productos/", views.producto_list, name="producto_list"),
    path("productos/nueva/", views.producto_create, name="producto_create"),
    path("productos/<int:pk>/", views.producto_detail, name="producto_detail"),
    path("productos/<int:pk>/editar/", views.producto_update, name="producto_update"),
    path("productos/<int:pk>/borrar/", views.producto_delete, name="producto_delete"),
]
