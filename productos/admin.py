from django.contrib import admin
from .models import Categoria, ConsultaCliente, Producto

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre', 'descripcion')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock', 'creado_en')
    search_fields = ('nombre', 'categoria__nombre')
    list_filter = ('categoria', 'creado_en')
    readonly_fields = ('creado_en',)
    exclude = ('imagen_fuente_url', 'imagen_credito')


class ConsultaClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'producto_interes', 'fecha')
    search_fields = ('nombre', 'correo', 'mensaje', 'producto_interes__nombre')
    list_filter = ('fecha',)
    readonly_fields = ('fecha',)


# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ConsultaCliente, ConsultaClienteAdmin)
