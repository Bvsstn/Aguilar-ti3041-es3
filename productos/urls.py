from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultas/', views.customer_consultation, name='customer_consultation'),
    path('cuenta/', views.account, name='account'),
    path('cuenta/crear/', views.register_account, name='account_register'),
    path('cuenta/editar/', views.edit_account, name='edit_account'),
    path('cerrar-sesion/', views.logout_account, name='logout'),
    path('panel-administrador/', views.admin_panel, name='admin_panel'),
    path('panel-administrador/reportes/', views.admin_reports, name='admin_reports'),
    path('panel-administrador/reportes/categorias/', views.admin_category_report, name='admin_category_report'),
    path('panel-administrador/reportes/stock/', views.admin_stock_report, name='admin_stock_report'),
    path('panel-administrador/productos/', views.admin_product_list, name='admin_product_list'),
    path('panel-administrador/productos/agregar/', views.admin_product_create, name='admin_product_create'),
    path('panel-administrador/productos/<int:product_id>/editar/', views.admin_product_edit, name='admin_product_edit'),
    path('panel-administrador/productos/<int:product_id>/eliminar/', views.admin_product_delete, name='admin_product_delete'),
    path('carrito/', views.cart, name='cart'),
    path('carrito/agregar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/actualizar/<int:product_id>/', views.update_cart, name='update_cart'),
    path('carrito/eliminar/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrito/comprar/', views.checkout, name='checkout'),
]