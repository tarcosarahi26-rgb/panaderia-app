from django.urls import path

from panaderia import views

# Las rutas fijas (nueva/) van antes que las dinámicas (<int:pk>/).
urlpatterns = [
    path("categorias/", views.categoria_list, name="categoria_list"),
    path("categorias/nueva/", views.categoria_create, name="categoria_create"),
    path("categorias/<int:pk>/", views.categoria_detail, name="categoria_detail"),
    path("categorias/<int:pk>/editar/", views.categoria_update, name="categoria_update"),
    path("categorias/<int:pk>/borrar/", views.categoria_delete, name="categoria_delete"),
]
