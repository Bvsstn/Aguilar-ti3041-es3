import io
import os
import tempfile
from urllib.parse import urlsplit

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from .models import Categoria, Producto


class CatalogoUrlTests(TestCase):
    def test_catalogo_is_available_at_root_and_productos(self):
        for url in ('/', '/productos/'):
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'productos/index.html')


class ProductoFixtureImagenTests(TestCase):
    fixtures = ['productos.json']

    def test_seeded_products_have_unique_images_without_attribution(self):
        productos = list(Producto.objects.all())

        self.assertEqual(len(productos), 40)
        self.assertEqual(len({producto.imagen_url for producto in productos}), 40)
        self.assertTrue(all(not producto.imagen_fuente_url for producto in productos))
        self.assertTrue(all(not producto.imagen_credito for producto in productos))


class ProductoImagenTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Herramientas',
            descripcion='Herramientas de prueba.',
        )

    def test_catalog_displays_each_products_external_image_and_source(self):
        image_url = 'https://example.com/images/martillo.jpg'
        source_url = 'https://example.com/products/martillo'
        Producto.objects.create(
            nombre='Martillo de prueba',
            categoria=self.categoria,
            precio='1000.00',
            stock=1,
            imagen_url=image_url,
            imagen_fuente_url=source_url,
        )

        response = self.client.get('/')

        self.assertContains(response, image_url)
        self.assertContains(response, source_url)
        self.assertContains(response, 'alt="Martillo de prueba"')

    def test_uploaded_image_takes_precedence_over_external_url(self):
        Producto.objects.create(
            nombre='Alicate de prueba',
            categoria=self.categoria,
            precio='1000.00',
            stock=1,
            imagen_archivo='productos/alicate.jpg',
            imagen_url='https://example.com/images/alicate.jpg',
        )

        response = self.client.get('/')

        self.assertContains(response, 'src="/media/productos/alicate.jpg"')
        self.assertNotContains(response, 'https://example.com/images/alicate.jpg')

    def test_product_requires_a_local_or_external_image(self):
        producto = Producto(
            nombre='Producto de prueba',
            categoria=self.categoria,
            precio='1000.00',
            stock=1,
        )

        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_admin_add_form_offers_local_upload_and_image_url(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(user)

        response = self.client.get('/admin/productos/producto/add/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="imagen_archivo"')
        self.assertContains(response, 'name="imagen_url"')
        self.assertNotContains(response, 'name="imagen_fuente_url"')
        self.assertNotContains(response, 'name="imagen_credito"')

    def test_admin_saves_a_locally_uploaded_product_image(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(user)
        image_bytes = io.BytesIO()
        Image.new('RGB', (1, 1), color='red').save(image_bytes, format='PNG')
        image = SimpleUploadedFile(
            'martillo.png',
            image_bytes.getvalue(),
            content_type='image/png',
        )

        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    '/admin/productos/producto/add/',
                    {
                        'nombre': 'Martillo con imagen local',
                        'categoria': self.categoria.pk,
                        'precio': '1000.00',
                        'stock': 1,
                        'imagen_archivo': image,
                        'imagen_url': '',
                    },
                )

                self.assertEqual(response.status_code, 302)
                producto = Producto.objects.get(nombre='Martillo con imagen local')
                self.assertTrue(
                    os.path.isfile(os.path.join(media_root, str(producto.imagen_archivo)))
                )


class CarritoTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Herramientas',
            descripcion='Herramientas de prueba.',
        )
        self.producto = Producto.objects.create(
            nombre='Martillo de prueba',
            categoria=self.categoria,
            precio='1200.00',
            stock=5,
            imagen_url='https://example.com/images/martillo.jpg',
        )

    def test_catalog_adds_product_and_cart_page_shows_it(self):
        response = self.client.post(
            reverse('add_to_cart', args=[self.producto.pk]),
        )

        self.assertRedirects(response, reverse('index'))
        response = self.client.get(reverse('cart'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.nombre)
        self.assertEqual(response.context['cart_count'], 1)
        self.assertEqual(response.context['items'][0]['cantidad'], 1)
        self.assertContains(response, reverse('cart'))

    def test_adding_product_shows_dismissible_notification_with_its_name(self):
        response = self.client.post(
            reverse('add_to_cart', args=[self.producto.pk]),
            follow=True,
        )

        self.assertContains(
            response,
            f'{self.producto.nombre} se agregó al carro.',
        )
        self.assertContains(response, 'data-dismiss-message')
        self.assertContains(response, 'data-autodismiss')

    def test_quantity_can_be_updated_and_product_removed(self):
        self.client.post(reverse('add_to_cart', args=[self.producto.pk]))

        response = self.client.post(
            reverse('update_cart', args=[self.producto.pk]),
            {'quantity': 3},
        )
        self.assertRedirects(response, reverse('cart'))
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.context['cart_count'], 3)

        response = self.client.post(
            reverse('remove_from_cart', args=[self.producto.pk]),
        )
        self.assertRedirects(response, reverse('cart'))
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.context['items'], [])

    def test_quantity_update_cannot_exceed_current_stock(self):
        self.client.post(reverse('add_to_cart', args=[self.producto.pk]))

        response = self.client.post(
            reverse('update_cart', args=[self.producto.pk]),
            {'quantity': 6},
            follow=True,
        )

        self.assertEqual(self.client.session['cart'][str(self.producto.pk)], 1)
        self.assertContains(response, 'Solo quedan 5 unidades')

    def test_checkout_deducts_stock_and_clears_cart(self):
        for _ in range(2):
            self.client.post(reverse('add_to_cart', args=[self.producto.pk]))

        response = self.client.post(reverse('checkout'), follow=True)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 3)
        self.assertEqual(self.client.session.get('cart'), {})
        self.assertContains(
            response,
            'Su pago se proceso correctamente, muchas gracias por comprar en Ferresteban',
        )

    def test_checkout_with_insufficient_stock_changes_nothing(self):
        other_product = Producto.objects.create(
            nombre='Alicate de prueba',
            categoria=self.categoria,
            precio='2000.00',
            stock=1,
            imagen_url='https://example.com/images/alicate.jpg',
        )
        session = self.client.session
        session['cart'] = {
            str(self.producto.pk): 1,
            str(other_product.pk): 2,
        }
        session.save()

        response = self.client.post(reverse('checkout'), follow=True)

        self.producto.refresh_from_db()
        other_product.refresh_from_db()
        self.assertEqual(self.producto.stock, 5)
        self.assertEqual(other_product.stock, 1)
        self.assertContains(response, 'Solo quedan 1 unidad')


class AccountTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_login_page_only_shows_login_and_links_to_registration(self):
        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Iniciar sesión')
        self.assertContains(response, '¿Primera compra?')
        self.assertContains(response, reverse('account_register'))
        self.assertNotContains(response, 'name="password1"')

        response = self.client.get(reverse('account_register'))
        self.assertContains(response, 'Crear cuenta')
        self.assertContains(response, 'name="ciudad"')
        self.assertContains(response, 'name="comuna"')
        self.assertContains(response, 'name="direccion"')
        self.assertNotContains(response, 'name="username"')

    def test_registration_saves_account_and_starts_session(self):
        response = self.client.post(
            reverse('account_register'),
            {
                'action': 'register',
                'first_name': 'Camila',
                'last_name': 'Rojas',
                'email': 'camila@example.com',
                'ciudad': 'Santiago',
                'comuna': 'Maipú',
                'direccion': 'Av. Principal 123',
                'password1': 'PalaSegura2026!',
                'password2': 'PalaSegura2026!',
            },
            follow=True,
        )

        user = self.User.objects.get(email='camila@example.com')
        self.assertTrue(user.check_password('PalaSegura2026!'))
        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))
        self.assertContains(response, 'Bienvenido Camila')
        self.assertEqual(user.perfil.ciudad, 'Santiago')
        self.assertEqual(user.perfil.comuna, 'Maipú')
        self.assertEqual(user.perfil.direccion, 'Av. Principal 123')

    def test_login_and_logout_use_django_authentication(self):
        user = self.User.objects.create_user(
            username='usuario-test',
            email='usuario@example.com',
            password='MartilloSeguro-8842!',
        )

        response = self.client.post(
            reverse('account'),
            {
                'action': 'login',
                'identifier': 'usuario@example.com',
                'password': 'MartilloSeguro-8842!',
            },
            follow=True,
        )

        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))
        self.assertContains(response, 'Bienvenido usuario@example.com')

        response = self.client.post(reverse('logout'), follow=True)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(response, 'Iniciar sesión')

    def test_invalid_login_shows_a_friendly_error(self):
        response = self.client.post(
            reverse('account'),
            {
                'action': 'login',
                'identifier': 'usuario-inexistente',
                'password': 'incorrecta',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'El correo electrónico o la contraseña no son correctos.',
        )

    def test_account_owner_can_edit_saved_profile_data(self):
        user = self.User.objects.create_user(
            username='usuario-antiguo',
            password='MartilloSeguro-8842!',
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('edit_account'),
            {
                'first_name': 'Camila',
                'last_name': 'Rojas',
                'email': 'camila@example.com',
                'ciudad': 'Valparaíso',
                'comuna': 'Viña del Mar',
                'direccion': 'Calle del Mar 456',
            },
            follow=True,
        )

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Camila')
        self.assertEqual(user.last_name, 'Rojas')
        self.assertEqual(user.email, 'camila@example.com')
        self.assertEqual(user.perfil.ciudad, 'Valparaíso')
        self.assertEqual(user.perfil.comuna, 'Viña del Mar')
        self.assertEqual(user.perfil.direccion, 'Calle del Mar 456')
        self.assertContains(response, 'Tus datos se actualizaron correctamente.')

    def test_header_shows_login_link_or_account_menu(self):
        response = self.client.get('/')
        self.assertContains(response, 'Iniciar sesión')

        user = self.User.objects.create_user(
            username='usuario-menu',
            first_name='Camila',
            password='MartilloSeguro-8842!',
        )
        self.client.force_login(user)

        response = self.client.get('/')
        self.assertContains(response, 'Bienvenido Camila')
        self.assertContains(response, 'Editar mis datos')
        self.assertContains(response, 'Cerrar sesión')


class AdminProductManagementTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.staff = self.User.objects.create_user(
            username='administrador',
            password='AdminSeguro-2026!',
            is_staff=True,
        )
        self.regular_user = self.User.objects.create_user(
            username='cliente',
            password='ClienteSeguro-2026!',
        )
        self.category = Categoria.objects.create(
            nombre='Herramientas',
            descripcion='Herramientas de prueba.',
        )
        self.product = Producto.objects.create(
            nombre='Martillo de prueba',
            categoria=self.category,
            precio='1200.00',
            stock=5,
            imagen_url='https://example.com/martillo.jpg',
        )

    def test_admin_panel_link_is_only_shown_to_staff(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Panel Administrador')

        self.client.force_login(self.regular_user)
        response = self.client.get('/')
        self.assertNotContains(response, 'Panel Administrador')

        self.client.force_login(self.staff)
        response = self.client.get('/')
        self.assertContains(response, 'Panel Administrador')

    def test_admin_views_reject_non_staff_users(self):
        self.client.force_login(self.regular_user)

        for route in ('admin_panel', 'admin_product_list', 'admin_product_create'):
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 302)
                self.assertEqual(urlsplit(response.url).path, reverse('index'))

    def test_admin_panel_and_product_listing_show_inventory(self):
        self.client.force_login(self.staff)

        response = self.client.get(reverse('admin_panel'))
        self.assertContains(response, 'Ver listado y modificar productos')
        self.assertContains(response, 'Ver reportes')
        self.assertEqual(response.content.count(b'<a class="admin-option'), 2)

        response = self.client.get(reverse('admin_product_list'))
        self.assertContains(response, self.product.nombre)
        self.assertContains(response, reverse('admin_reports'))
        self.assertContains(response, reverse('admin_category_report'))
        self.assertContains(response, reverse('admin_stock_report'))
        self.assertContains(response, 'Disponible')
        self.assertContains(response, self.category.nombre)
        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'name="disponibilidad"')

    def test_admin_can_filter_products_and_manage_stock(self):
        empty_product = Producto.objects.create(
            nombre='Alicate agotado',
            categoria=self.category,
            precio='2000.00',
            stock=0,
            imagen_url='https://example.com/alicate.jpg',
        )
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse('admin_product_list'),
            {'q': 'agotado', 'disponibilidad': 'agotado'},
        )
        self.assertContains(response, empty_product.nombre)
        self.assertNotContains(response, self.product.nombre)

        response = self.client.post(
            reverse('admin_product_edit', args=[self.product.pk]),
            {
                'nombre': self.product.nombre,
                'categoria': self.category.pk,
                'precio': '1200.00',
                'stock': 2,
                'imagen_archivo': '',
                'imagen_url': self.product.imagen_url,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('admin_product_list'))
        self.assertContains(response, 'Producto modificado correctamente')
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)

    def test_admin_can_create_and_delete_products(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse('admin_product_create'),
            {
                'nombre': 'Destornillador nuevo',
                'categoria': self.category.pk,
                'precio': '3500.00',
                'stock': 8,
                'imagen_archivo': '',
                'imagen_url': 'https://example.com/destornillador.jpg',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('admin_product_list'))
        self.assertContains(response, 'Producto agregado correctamente')
        created = Producto.objects.get(nombre='Destornillador nuevo')
        self.assertEqual(created.stock, 8)

        delete_url = reverse('admin_product_delete', args=[created.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Producto.objects.filter(pk=created.pk).exists())

        response = self.client.post(delete_url, follow=True)
        self.assertRedirects(response, reverse('admin_product_list'))
        self.assertContains(response, 'Producto borrado correctamente')
        self.assertFalse(Producto.objects.filter(pk=created.pk).exists())

    def test_admin_can_upload_local_product_image_from_management_page(self):
        image_bytes = io.BytesIO()
        Image.new('RGB', (1, 1), color='blue').save(image_bytes, format='PNG')
        image = SimpleUploadedFile(
            'taladro.png',
            image_bytes.getvalue(),
            content_type='image/png',
        )
        self.client.force_login(self.staff)

        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse('admin_product_create'),
                    {
                        'nombre': 'Taladro con imagen local',
                        'categoria': self.category.pk,
                        'precio': '4500.00',
                        'stock': 3,
                        'imagen_archivo': image,
                        'imagen_url': '',
                    },
                )

                self.assertRedirects(response, reverse('admin_product_list'))
                product = Producto.objects.get(nombre='Taladro con imagen local')
                self.assertTrue(
                    os.path.isfile(os.path.join(media_root, str(product.imagen_archivo)))
                )


class AdminReportTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.staff = self.User.objects.create_user(
            username='report-admin',
            password='ReportSeguro-2026!',
            is_staff=True,
        )
        self.category = Categoria.objects.create(
            nombre='Pinturas',
            descripcion='Pinturas de prueba.',
        )
        self.other_category = Categoria.objects.create(
            nombre='Herramientas',
            descripcion='Herramientas de prueba.',
        )
        self.product_a = Producto.objects.create(
            nombre='Pintura blanca',
            categoria=self.category,
            precio='1000.00',
            stock=2,
            imagen_url='https://example.com/pintura.jpg',
        )
        self.product_b = Producto.objects.create(
            nombre='Pintura azul',
            categoria=self.category,
            precio='2000.00',
            stock=0,
            imagen_url='https://example.com/azul.jpg',
        )
        Producto.objects.create(
            nombre='Sierra disponible',
            categoria=self.other_category,
            precio='5000.00',
            stock=10,
            imagen_url='https://example.com/sierra.jpg',
        )
        self.client.force_login(self.staff)

    def test_reports_dashboard_and_base_navigation_link_to_each_report(self):
        response = self.client.get(reverse('admin_reports'))

        self.assertContains(response, 'Productos por categoría')
        self.assertContains(response, 'Stock crítico y no disponibles')
        self.assertContains(response, reverse('admin_category_report'))
        self.assertContains(response, reverse('admin_stock_report'))

        response = self.client.get(reverse('admin_category_report'))
        self.assertContains(response, 'Stock crítico')
        self.assertContains(response, 'Productos')

    def test_category_report_aggregates_count_average_price_and_stock(self):
        response = self.client.get(reverse('admin_category_report'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productos/report_categories.html')
        category_report = next(
            item
            for item in response.context['categorias']
            if item.pk == self.category.pk
        )
        self.assertEqual(category_report.total_productos, 2)
        self.assertEqual(category_report.precio_promedio, 1500)
        self.assertEqual(category_report.stock_total, 2)
        self.assertContains(response, self.product_a.nombre)
        self.assertContains(response, self.product_b.nombre)

    def test_critical_stock_report_filters_by_threshold_and_orders_stock(self):
        response = self.client.get(
            reverse('admin_stock_report'),
            {'umbral': 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productos/report_stock.html')
        self.assertEqual(
            [producto.pk for producto in response.context['productos']],
            [self.product_b.pk, self.product_a.pk],
        )
        self.assertNotContains(response, 'Sierra disponible')
        self.assertContains(response, 'No disponible')
        self.assertContains(response, 'Stock crítico')

    def test_critical_stock_report_uses_default_threshold_for_invalid_input(self):
        response = self.client.get(
            reverse('admin_stock_report'),
            {'umbral': 'invalido'},
        )

        self.assertEqual(response.context['threshold'], 5)
        self.assertEqual(
            [product.pk for product in response.context['productos']],
            [self.product_b.pk, self.product_a.pk],
        )
