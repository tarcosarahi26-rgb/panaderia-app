from django.urls import path

from panaderia import views

# Las rutas fijas (nueva/) van antes que las dinámicas (<int:pk>/).
urlpatterns = [
    path("ingredientes/", views.ingrediente_list, name="ingrediente_list"),
    path("ingredientes/nueva/", views.ingrediente_create, name="ingrediente_create"),
    path("ingredientes/<int:pk>/", views.ingrediente_detail, name="ingrediente_detail"),
    path("ingredientes/<int:pk>/editar/", views.ingrediente_update, name="ingrediente_update"),
    path("ingredientes/<int:pk>/borrar/", views.ingrediente_delete, name="ingrediente_delete"),
]
