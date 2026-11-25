from panaderia.views.home_views import home
from panaderia.views.auth_views import login_view, logout_view, registro_view
from panaderia.views.categoria_views import (
    categoria_list,
    categoria_detail,
    categoria_create,
    categoria_update,
    categoria_delete,
)
from panaderia.views.ingrediente_views import (
    ingrediente_list,
    ingrediente_detail,
    ingrediente_create,
    ingrediente_update,
    ingrediente_delete,
)
from panaderia.views.producto_views import (
    producto_list,
    producto_detail,
    producto_create,
    producto_update,
    producto_delete,
)
from panaderia.views.pedido_views import (
    pedido_list,
    pedido_detail,
    pedido_create,
    pedido_update,
    pedido_delete,
)
