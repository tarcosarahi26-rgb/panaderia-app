from django.urls import path

from panaderia import views
from panaderia.urls.categoria_urls import urlpatterns as categoria_urls
from panaderia.urls.ingrediente_urls import urlpatterns as ingrediente_urls
from panaderia.urls.producto_urls import urlpatterns as producto_urls
from panaderia.urls.pedido_urls import urlpatterns as pedido_urls
from panaderia.urls.auth_urls import urlpatterns as auth_urls

app_name = "panaderia"

urlpatterns = (
    [path("", views.home, name="home")]
    + auth_urls
    + categoria_urls
    + ingrediente_urls
    + producto_urls
    + pedido_urls
)
