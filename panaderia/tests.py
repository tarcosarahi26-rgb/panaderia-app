from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from panaderia.models import Categoria, Pedido, Producto
from panaderia.utils.grupos import GRUPO_ADMIN, GRUPO_CONSULTOR


class PanaderiaBaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adm", password="x12345678*")
        cls.admin.groups.add(Group.objects.get(name=GRUPO_ADMIN))
        cls.cons1 = User.objects.create_user("c1", password="x12345678*")
        cls.cons1.groups.add(Group.objects.get(name=GRUPO_CONSULTOR))
        cls.cons2 = User.objects.create_user("c2", password="x12345678*")
        cls.cons2.groups.add(Group.objects.get(name=GRUPO_CONSULTOR))
        cls.categoria = Categoria.objects.create(nombre="Panes")
        cls.producto = Producto.objects.create(
            nombre="Pan de agua", precio="0.15", categoria=cls.categoria, creado_por=cls.cons1
        )


class GruposTest(PanaderiaBaseTest):
    def test_los_grupos_existen_tras_migrate(self):
        self.assertTrue(Group.objects.filter(name=GRUPO_ADMIN).exists())
        self.assertTrue(Group.objects.filter(name=GRUPO_CONSULTOR).exists())

    def test_consultor_no_tiene_permisos_de_categoria(self):
        self.assertFalse(self.cons1.has_perm("panaderia.add_categoria"))
        self.assertTrue(self.cons1.has_perm("panaderia.add_producto"))


class VistasProtegidasTest(PanaderiaBaseTest):
    def test_anonimo_va_al_login(self):
        r = self.client.get(reverse("panaderia:producto_create"))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("panaderia:login"), r.url)

    def test_listados_son_publicos(self):
        self.assertEqual(self.client.get(reverse("panaderia:producto_list")).status_code, 200)

    def test_id_inexistente_da_404(self):
        self.assertEqual(self.client.get(reverse("panaderia:producto_detail", args=[9999])).status_code, 404)

    def test_logout_solo_por_post(self):
        self.client.force_login(self.cons1)
        self.assertEqual(self.client.get(reverse("panaderia:logout")).status_code, 405)
        self.assertEqual(self.client.post(reverse("panaderia:logout")).status_code, 302)

    def test_consultor_no_puede_crear_categoria(self):
        self.client.force_login(self.cons1)
        self.assertEqual(self.client.get(reverse("panaderia:categoria_create")).status_code, 403)

    def test_consultor_puede_crear_producto_y_queda_como_propietario(self):
        self.client.force_login(self.cons2)
        r = self.client.post(reverse("panaderia:producto_create"), {
            "categoria": self.categoria.pk, "nombre": "Nuevo", "precio": "1.00",
            "tipo_venta": "UNIDAD", "fecha_elaboracion": "2026-11-24", "disponible": "on",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Producto.objects.get(nombre="Nuevo").creado_por, self.cons2)


class ReglaDePropiedadTest(PanaderiaBaseTest):
    def test_otro_consultor_no_puede_editar_ni_borrar(self):
        self.client.force_login(self.cons2)
        self.assertEqual(self.client.get(reverse("panaderia:producto_update", args=[self.producto.pk])).status_code, 403)
        self.assertEqual(self.client.post(reverse("panaderia:producto_delete", args=[self.producto.pk])).status_code, 403)
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_el_creador_si_puede_editar(self):
        self.client.force_login(self.cons1)
        self.assertEqual(self.client.get(reverse("panaderia:producto_update", args=[self.producto.pk])).status_code, 200)

    def test_administrador_puede_borrar_lo_de_otros(self):
        self.client.force_login(self.admin)
        r = self.client.post(reverse("panaderia:producto_delete", args=[self.producto.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_borrar_categoria_con_productos_no_da_500(self):
        self.client.force_login(self.admin)
        r = self.client.post(reverse("panaderia:categoria_delete", args=[self.categoria.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())


class RegistroTest(TestCase):
    def test_registro_crea_usuario_en_consultores(self):
        r = self.client.post(reverse("panaderia:registro"), {
            "username": "nuevo", "email": "nuevo@x.com",
            "password1": "ClaveSegura2026*", "password2": "ClaveSegura2026*",
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.get(username="nuevo").groups.filter(name=GRUPO_CONSULTOR).exists())
