from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from panaderia.models import Categoria, Ingrediente, Pedido, Producto
from panaderia.utils.grupos import GRUPO_ADMIN, GRUPO_CONSULTOR, crear_grupos

USUARIOS = [
    # (username, correo, contraseña, grupo, es_superusuario)
    ("admin", "admin@panaderia.test", "Admin12345*", None, True),
    ("administrador1", "administrador1@panaderia.test", "Admin12345*", GRUPO_ADMIN, False),
    ("consultor1", "consultor1@panaderia.test", "Consul12345*", GRUPO_CONSULTOR, False),
    ("consultor2", "consultor2@panaderia.test", "Consul12345*", GRUPO_CONSULTOR, False),
]

CATEGORIAS = [
    ("Panes", "Panes frescos horneados cada mañana."),
    ("Pasteles", "Pasteles para celebraciones."),
    ("Galletas", "Galletas caseras."),
    ("Bocaditos", "Piezas pequeñas para el café."),
    ("Bebidas", "Bebidas calientes y frías."),
]

INGREDIENTES = [
    ("Harina de trigo", "KG", "50.00"),
    ("Azúcar", "KG", "30.00"),
    ("Huevos", "U", "200.00"),
    ("Mantequilla", "KG", "15.00"),
    ("Leche", "L", "40.00"),
    ("Levadura", "KG", "5.00"),
    ("Chocolate", "KG", "12.00"),
]

# (nombre, categoria, precio, tipo_venta, ingredientes, propietario)
PRODUCTOS = [
    ("Pan de agua", "Panes", "0.15", "UNIDAD", ["Harina de trigo", "Levadura"], "administrador1"),
    ("Pan de yuca", "Panes", "0.40", "UNIDAD", ["Harina de trigo", "Leche"], "administrador1"),
    ("Pastel de chocolate", "Pasteles", "18.50", "PORCION", ["Harina de trigo", "Chocolate", "Huevos", "Azúcar"], "administrador1"),
    ("Pastel tres leches", "Pasteles", "16.00", "PORCION", ["Harina de trigo", "Leche", "Huevos", "Azúcar"], "consultor1"),
    ("Galletas de avena", "Galletas", "3.50", "DOCENA", ["Harina de trigo", "Mantequilla", "Azúcar"], "consultor1"),
    ("Empanada de viento", "Bocaditos", "0.90", "UNIDAD", ["Harina de trigo", "Mantequilla"], "consultor2"),
    ("Chocolate caliente", "Bebidas", "1.75", "PORCION", ["Leche", "Chocolate", "Azúcar"], "consultor2"),
]

CLIENTES = ["María Pérez", "Juan Andrade", "Lucía Torres", "Carlos Mena", "Ana Villacís", "Pedro Cevallos"]


class Command(BaseCommand):
    help = "Crea grupos, usuarios de prueba y datos de ejemplo (se puede ejecutar varias veces)."

    def handle(self, *args, **options):
        administradores, consultores = crear_grupos()
        grupos = {GRUPO_ADMIN: administradores, GRUPO_CONSULTOR: consultores}

        usuarios = {}
        for username, correo, clave, grupo, es_super in USUARIOS:
            user, creado = User.objects.get_or_create(username=username, defaults={"email": correo})
            if creado:
                user.set_password(clave)
            user.is_superuser = es_super
            user.is_staff = es_super
            user.save()
            if grupo:
                user.groups.add(grupos[grupo])
            usuarios[username] = user

        categorias = {}
        for nombre, descripcion in CATEGORIAS:
            categorias[nombre], _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": descripcion}
            )

        ingredientes = {}
        for nombre, unidad, stock in INGREDIENTES:
            ingredientes[nombre], _ = Ingrediente.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "unidad": unidad,
                    "stock": Decimal(stock),
                    "fecha_caducidad": date.today() + timedelta(days=90),
                },
            )

        productos = []
        for nombre, cat, precio, venta, ings, dueno in PRODUCTOS:
            producto, creado = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "categoria": categorias[cat],
                    "precio": Decimal(precio),
                    "tipo_venta": venta,
                    "descripcion": f"{nombre} elaborado a diario.",
                    "creado_por": usuarios[dueno],
                },
            )
            if creado:
                producto.ingredientes.set([ingredientes[i] for i in ings])
            productos.append(producto)

        if Pedido.objects.count() < 5:
            estados = [e for e, _ in Pedido.Estado.choices]
            for i, cliente in enumerate(CLIENTES):
                Pedido.objects.create(
                    cliente=cliente,
                    producto=productos[i % len(productos)],
                    cantidad=i + 1,
                    estado=estados[i % len(estados)],
                    fecha_entrega=date.today() + timedelta(days=i + 1),
                    creado_por=usuarios["administrador1"],
                )

        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados correctamente."))
        self.stdout.write(
            f"Categorías: {Categoria.objects.count()} | Ingredientes: {Ingrediente.objects.count()} "
            f"| Productos: {Producto.objects.count()} | Pedidos: {Pedido.objects.count()}"
        )
