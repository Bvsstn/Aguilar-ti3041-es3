from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen_archivo = models.ImageField(
        upload_to='productos/',
        blank=True,
        verbose_name='Imagen local',
        help_text='Sube una imagen desde tu equipo. Si agregas ambas, se mostrará esta.',
    )
    imagen_url = models.URLField(
        max_length=2048,
        blank=True,
        verbose_name='Enlace de imagen',
        help_text='URL directa a una imagen. Puedes usarla en vez de subir un archivo.',
    )
    imagen_fuente_url = models.URLField(
        max_length=2048,
        blank=True,
        verbose_name='Fuente de la imagen',
        help_text='Página de origen de la imagen (opcional).',
    )
    imagen_credito = models.TextField(
        blank=True,
        verbose_name='Crédito de la imagen',
        help_text='Autor y licencia de la imagen, cuando corresponda.',
    )
    creado_en = models.DateTimeField(default=timezone.now)

    def clean(self):
        super().clean()
        if not self.imagen_archivo and not self.imagen_url:
            raise ValidationError({
                'imagen_url': 'Debes subir una imagen local o proporcionar un enlace.'
            })

    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    ciudad = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f'Perfil de {self.usuario}'