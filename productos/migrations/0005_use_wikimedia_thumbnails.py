from urllib.parse import quote, unquote, urlsplit, urlunsplit

from django.db import migrations


def use_thumbnails(apps, schema_editor):
    Producto = apps.get_model('productos', 'Producto')

    for producto in Producto.objects.exclude(imagen_url='').iterator():
        parsed_url = urlsplit(producto.imagen_url)
        if (
            parsed_url.hostname != 'upload.wikimedia.org'
            or not parsed_url.path.startswith('/wikipedia/commons/')
            or '/thumb/' in parsed_url.path
        ):
            continue

        original_path = unquote(parsed_url.path)
        relative_path = original_path[len('/wikipedia/commons/'):]
        filename = relative_path.rsplit('/', 1)[-1]
        thumbnail_path = (
            '/wikipedia/commons/thumb/'
            + relative_path
            + '/500px-'
            + filename
        )
        producto.imagen_url = urlunsplit((
            parsed_url.scheme,
            parsed_url.netloc,
            quote(thumbnail_path, safe='/'),
            '',
            '',
        ))
        producto.save(update_fields=('imagen_url',))


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_assign_product_images'),
    ]

    operations = [
        migrations.RunPython(use_thumbnails, migrations.RunPython.noop),
    ]
