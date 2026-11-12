from urllib.parse import urlsplit, urlunsplit

from django.db import migrations


def use_thumbnail_host(apps, schema_editor):
    Producto = apps.get_model('productos', 'Producto')

    for producto in Producto.objects.exclude(imagen_url='').iterator():
        parsed_url = urlsplit(producto.imagen_url)
        if (
            parsed_url.hostname != 'upload.wikimedia.org'
            or '/commons/thumb/' not in parsed_url.path
        ):
            continue

        producto.imagen_url = urlunsplit((
            parsed_url.scheme,
            'thumb.wikimedia.org',
            parsed_url.path,
            '',
            '',
        ))
        producto.save(update_fields=('imagen_url',))


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_use_wikimedia_thumbnails'),
    ]

    operations = [
        migrations.RunPython(use_thumbnail_host, migrations.RunPython.noop),
    ]
