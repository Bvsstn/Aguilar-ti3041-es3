from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Avg, Count, Sum

from .forms import (
    AccountUpdateForm,
    ConsultaClienteForm,
    LoginForm,
    ProductoAdminForm,
    RegistrationForm,
)
from .models import Categoria, Producto


def _session_cart(request):
    cart = request.session.get('cart', {})
    return cart if isinstance(cart, dict) else {}


def _cart_count(request):
    return sum(
        quantity
        for quantity in _session_cart(request).values()
        if type(quantity) is int and quantity > 0
    )


def index(request):
    visit_count = request.session.get('visit_count', 0)
    if type(visit_count) is not int or visit_count < 0:
        visit_count = 0
    visit_count += 1
    request.session['visit_count'] = visit_count
    productos = Producto.objects.select_related('categoria').order_by('nombre')
    return render(request, 'productos/index.html', {
        'productos': productos,
        'cart_count': _cart_count(request),
        'visit_count': visit_count,
    })


@require_http_methods(['GET', 'POST'])
def customer_consultation(request):
    form_data = request.POST if request.method == 'POST' else None
    form = ConsultaClienteForm(form_data)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tu consulta se envió correctamente.')
        return redirect('customer_consultation')

    return render(request, 'productos/consulta_cliente.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def account(request):
    if request.user.is_authenticated:
        return redirect('index')

    login_form = LoginForm(request=request)
    if request.method == 'POST':
        if request.POST.get('action') != 'login':
            return HttpResponseBadRequest('Acción de cuenta no válida.')
        login_form = LoginForm(request=request, data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            messages.success(request, 'Iniciaste sesión correctamente.')
            return redirect('index')

    return render(request, 'productos/account.html', {'form': login_form})


@require_http_methods(['GET', 'POST'])
def register_account(request):
    if request.user.is_authenticated:
        return redirect('index')

    form_data = request.POST if request.method == 'POST' else None
    form = RegistrationForm(form_data)
    if request.method == 'POST':
        if request.POST.get('action') != 'register':
            return HttpResponseBadRequest('Acción de cuenta no válida.')
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Tu cuenta se creó correctamente.')
            return redirect('index')

    return render(request, 'productos/account_register.html', {'form': form})


@login_required(login_url='account')
@require_http_methods(['GET', 'POST'])
def edit_account(request):
    form_data = request.POST if request.method == 'POST' else None
    form = AccountUpdateForm(form_data, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tus datos se actualizaron correctamente.')
        return redirect('edit_account')

    return render(request, 'productos/account_edit.html', {'form': form})


@require_POST
def logout_account(request):
    logout(request)
    messages.success(request, 'Cerraste sesión.')
    return redirect('index')


def _staff_required(view_func):
    return login_required(login_url='account')(
        user_passes_test(
            lambda user: user.is_staff,
            login_url='index',
        )(view_func)
    )


@_staff_required
def admin_panel(request):
    return render(request, 'productos/admin_panel.html')


@_staff_required
def admin_reports(request):
    return render(request, 'productos/admin_reports.html')


@_staff_required
def admin_category_report(request):
    categorias = Categoria.objects.annotate(
        total_productos=Count('producto'),
        precio_promedio=Avg('producto__precio'),
        stock_total=Sum('producto__stock'),
    ).prefetch_related('producto_set').order_by('nombre')
    return render(request, 'productos/report_categories.html', {
        'categorias': categorias,
    })


@_staff_required
def admin_stock_report(request):
    try:
        threshold = int(request.GET.get('umbral', '5'))
    except (TypeError, ValueError):
        threshold = 5
    threshold = max(threshold, 0)
    productos = Producto.objects.select_related('categoria').filter(
        stock__lte=threshold,
    ).order_by('stock', 'nombre')
    return render(request, 'productos/report_stock.html', {
        'productos': productos,
        'threshold': threshold,
    })


@_staff_required
def admin_product_list(request):
    productos = Producto.objects.select_related('categoria').order_by('nombre')
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('categoria', '').strip()
    availability = request.GET.get('disponibilidad', '').strip()

    if query:
        productos = productos.filter(nombre__icontains=query)
    if category_id.isdigit():
        productos = productos.filter(categoria_id=int(category_id))
    if availability == 'disponible':
        productos = productos.filter(stock__gt=0)
    elif availability == 'agotado':
        productos = productos.filter(stock__lte=0)

    return render(request, 'productos/admin_product_list.html', {
        'productos': productos,
        'categorias': Categoria.objects.order_by('nombre'),
        'query': query,
        'selected_category': category_id,
        'availability': availability,
    })


@_staff_required
@require_http_methods(['GET', 'POST'])
def admin_product_create(request):
    form_data = request.POST if request.method == 'POST' else None
    form = ProductoAdminForm(form_data, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto agregado correctamente')
        return redirect('admin_product_list')

    return render(request, 'productos/admin_product_form.html', {
        'form': form,
        'title': 'Agregar producto',
        'submit_label': 'Crear producto',
    })


@_staff_required
@require_http_methods(['GET', 'POST'])
def admin_product_edit(request, product_id):
    product = get_object_or_404(Producto, pk=product_id)
    form_data = request.POST if request.method == 'POST' else None
    form = ProductoAdminForm(
        form_data,
        request.FILES or None,
        instance=product,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto modificado correctamente')
        return redirect('admin_product_list')

    return render(request, 'productos/admin_product_form.html', {
        'form': form,
        'title': 'Editar producto',
        'submit_label': 'Guardar cambios',
        'product': product,
    })


@_staff_required
@require_http_methods(['GET', 'POST'])
def admin_product_delete(request, product_id):
    product = get_object_or_404(Producto, pk=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto borrado correctamente')
        return redirect('admin_product_list')

    return render(request, 'productos/admin_product_delete.html', {
        'product': product,
    })


def cart(request):
    session_cart = _session_cart(request)
    quantities = {}
    for product_id, quantity in session_cart.items():
        if type(quantity) is int and quantity > 0:
            try:
                quantities[int(product_id)] = quantity
            except (TypeError, ValueError):
                continue

    products = Producto.objects.select_related('categoria').filter(
        pk__in=quantities
    ).order_by('nombre')
    items = [
        {
            'producto': product,
            'cantidad': quantities[product.pk],
            'subtotal': product.precio * quantities[product.pk],
        }
        for product in products
    ]
    valid_ids = {str(item['producto'].pk) for item in items}
    if any(product_id not in valid_ids for product_id in session_cart):
        request.session['cart'] = {
            product_id: quantity
            for product_id, quantity in session_cart.items()
            if product_id in valid_ids
        }

    return render(request, 'productos/cart.html', {
        'items': items,
        'total': sum((item['subtotal'] for item in items), start=0),
        'cart_count': sum(item['cantidad'] for item in items),
    })


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Producto, pk=product_id)
    session_cart = _session_cart(request)
    product_key = str(product.pk)
    quantity = session_cart.get(product_key, 0)
    if type(quantity) is not int or quantity < 0:
        quantity = 0

    if quantity >= product.stock:
        messages.error(request, f'No hay más unidades disponibles de {product.nombre}.')
    else:
        session_cart[product_key] = quantity + 1
        request.session['cart'] = session_cart
        messages.success(
            request,
            f'{product.nombre} se agregó al carro.',
            extra_tags='cart-added',
        )

    return redirect('index')


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Producto, pk=product_id)
    session_cart = _session_cart(request)
    product_key = str(product.pk)

    try:
        quantity = int(request.POST.get('quantity', ''))
    except (TypeError, ValueError):
        quantity = 0

    if product_key not in session_cart:
        messages.error(request, 'Ese producto ya no está en tu carro.')
    elif quantity < 1:
        messages.error(request, 'La cantidad debe ser al menos 1.')
    elif quantity > product.stock:
        unit = 'unidad' if product.stock == 1 else 'unidades'
        messages.error(
            request,
            f'Solo quedan {product.stock} {unit} de {product.nombre}.',
        )
    else:
        session_cart[product_key] = quantity
        request.session['cart'] = session_cart
        messages.success(request, 'Se actualizó la cantidad del producto.')

    return redirect('cart')


@require_POST
def remove_from_cart(request, product_id):
    session_cart = _session_cart(request)
    session_cart.pop(str(product_id), None)
    request.session['cart'] = session_cart
    messages.success(request, 'Se eliminó el producto del carro.')
    return redirect('cart')


class _StockUnavailable(Exception):
    pass


@require_POST
def checkout(request):
    session_cart = _session_cart(request)
    requested = {}
    for product_id, quantity in session_cart.items():
        try:
            parsed_id = int(product_id)
        except (TypeError, ValueError):
            continue
        if type(quantity) is int and quantity > 0:
            requested[parsed_id] = quantity

    if not requested:
        messages.error(request, 'Tu carro está vacío.')
        return redirect('cart')

    try:
        with transaction.atomic():
            products = list(
                Producto.objects.select_for_update()
                .filter(pk__in=requested)
                .order_by('pk')
            )
            if len(products) != len(requested):
                raise _StockUnavailable(
                    'Uno o más productos ya no están disponibles. Revisa tu carro.'
                )

            for product in products:
                quantity = requested[product.pk]
                if product.stock < quantity:
                    unit = 'unidad' if product.stock == 1 else 'unidades'
                    raise _StockUnavailable(
                        f'Solo quedan {product.stock} {unit} de {product.nombre}.'
                    )

            for product in products:
                quantity = requested[product.pk]
                updated = Producto.objects.filter(
                    pk=product.pk,
                    stock__gte=quantity,
                ).update(stock=F('stock') - quantity)
                if not updated:
                    raise _StockUnavailable(
                        f'El stock de {product.nombre} cambió. Revisa tu carro.'
                    )
    except _StockUnavailable as error:
        messages.error(request, str(error))
        return redirect('cart')

    request.session['cart'] = {}
    messages.success(
        request,
        'Su pago se proceso correctamente, muchas gracias por comprar en Ferresteban',
    )
    return redirect('cart')
