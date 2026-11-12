from django.db import migrations


def clear_product_attribution(apps, schema_editor):
    Producto = apps.get_model('productos', 'Producto')
    Producto.objects.update(imagen_fuente_url='', imagen_credito='')


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_use_thumbnail_host'),
    ]

    operations = [
        migrations.RunPython(clear_product_attribution, migrations.RunPython.noop),
    ]
