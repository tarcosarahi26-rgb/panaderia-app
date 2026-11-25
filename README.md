# panaderia-app

Proyecto Django individual — **Programación II**
Estudiante: Aracely Sarahi Tarco Yuquilema · Universidad UTE · Desarrollo de Software
**Tema asignado:** Panadería

Aplicación web en Django con 4 tablas relacionadas, CRUD con vistas de función, autenticación de usuarios y control de acceso por grupos.

## Modelo de datos

```
Categoria 1 ───────< N Producto N >───────< N Ingrediente      (ManyToMany: Producto.ingredientes)
                         │ 1
                         │
                         ▼ N
                       Pedido

User 1 ───< N Producto  (creado_por)        User 1 ───< N Pedido (creado_por)
```

| Tabla | Campos principales | Relaciones |
|---|---|---|
| **Categoria** | nombre (único), descripcion | 1 categoría → N productos (`related_name="productos"`, `PROTECT`) |
| **Ingrediente** | nombre, unidad (TextChoices), stock (Decimal), fecha_caducidad (Date) | M2M con Producto (`related_name="productos"`) |
| **Producto** | nombre, descripcion, precio (Decimal), tipo_venta (TextChoices), fecha_elaboracion (Date), disponible | FK a Categoria, M2M a Ingrediente, FK a User `creado_por` (`SET_NULL`) |
| **Pedido** | cliente, cantidad, estado (TextChoices), fecha_pedido, fecha_entrega | FK a Producto (`related_name="pedidos"`, `PROTECT`), FK a User `creado_por` |

## Levantar el proyecto desde cero

```bash
git clone <URL-DEL-REPOSITORIO>
cd panaderia-app

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate          # crea las tablas y los grupos con sus permisos
python manage.py cargar_datos     # usuarios de prueba + datos de ejemplo
python manage.py runserver
```

Abrir http://127.0.0.1:8000/

Para correr las pruebas automáticas: `python manage.py test`

## Datos de prueba

`python manage.py cargar_datos` se puede ejecutar varias veces sin duplicar nada. Crea 5 categorías, 7 ingredientes, 7 productos y 6 pedidos.

## Usuarios de prueba

| Usuario | Contraseña | Grupo | Qué puede hacer |
|---|---|---|---|
| `admin` | `Admin12345*` | superusuario | Todo, incluido `/admin/` |
| `administrador1` | `Admin12345*` | administradores | Crear, editar y eliminar en las cuatro entidades |
| `consultor1` | `Consul12345*` | consultores | Ver todo; crear productos; editar/eliminar **solo los productos que creó** |
| `consultor2` | `Consul12345*` | consultores | Igual que consultor1 |

Quien se registra desde `/registro/` entra automáticamente al grupo **consultores**.

## Grupos y permisos

- Los grupos se crean **por código**: `panaderia/utils/grupos.py`, enganchado a la señal `post_migrate` en `apps.py`. Basta con ejecutar `migrate`.
- **administradores**: todos los permisos de la app (`add_`, `change_`, `delete_`, `view_` de las cuatro entidades).
- **consultores**: `view_*` de todo + `add_producto`, `change_producto`, `delete_producto`.
- **Regla de propiedad** (`panaderia/utils/permisos.py`): un consultor solo edita o borra los registros donde `creado_por` es él. Los administradores se saltan la regla.
- Las vistas están protegidas con `@login_required` + `@permission_required(..., raise_exception=True)` y la comprobación de propiedad; las plantillas ocultan los botones con `{% if perms.panaderia.xxx %}` y el filtro `puede_editar` / `puede_eliminar`.
- Un usuario sin permiso que entra por URL recibe la página **403 — Acceso denegado**; un anónimo es enviado al login.

## Estructura del proyecto

```
panaderia-app/
├── config/                      # settings.py, urls.py, wsgi.py, asgi.py
├── templates/
│   ├── base.html                # navbar según user.is_authenticated + messages
│   └── 403.html
├── panaderia/
│   ├── models/                  # categoria.py, ingrediente.py, producto.py, pedido.py
│   ├── forms/                   # un ModelForm por entidad + registro_form.py
│   ├── views/                   # *_views.py por entidad + auth_views.py + home_views.py
│   ├── urls/                    # *_urls.py por entidad + auth_urls.py
│   ├── templates/panaderia/
│   │   ├── categorias/ ingredientes/ productos/ pedidos/   # lista, detalle, formulario, confirmar_eliminar
│   │   ├── auth/                # login.html, registro.html
│   │   ├── home.html  _paginacion.html  _campos_formulario.html
│   ├── templatetags/permisos_tags.py
│   ├── utils/                   # grupos.py, permisos.py
│   ├── management/commands/cargar_datos.py
│   ├── admin.py  apps.py  tests.py  migrations/
├── manage.py
└── requirements.txt
```

## Rutas principales

| URL | Vista |
|---|---|
| `/` | Portada |
| `/registro/` · `/login/` · `/logout/` (POST) | Autenticación |
| `/categorias/` · `/ingredientes/` · `/productos/` · `/pedidos/` | Listados (públicos) |
| `<entidad>/nueva/` · `<entidad>/<pk>/` · `/editar/` · `/borrar/` | Crear, detalle, editar, borrar |
