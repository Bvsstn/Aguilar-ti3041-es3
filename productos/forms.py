import uuid

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import PerfilUsuario, Producto


class LoginForm(forms.Form):
    error_message = 'El correo electrónico o la contraseña no son correctos.'

    identifier = forms.CharField(
        label='Correo electrónico o nombre de usuario',
        widget=forms.TextInput(attrs={'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')
        if not identifier or not password:
            return cleaned_data

        User = get_user_model()
        if '@' in identifier:
            matching_users = User.objects.filter(email__iexact=identifier)
            if matching_users.count() == 1:
                identifier = matching_users.get().get_username()
            elif matching_users.exists():
                raise ValidationError(self.error_message)

        self.user_cache = authenticate(
            self.request,
            username=identifier,
            password=password,
        )
        if self.user_cache is None:
            raise ValidationError(self.error_message)
        return cleaned_data

    def get_user(self):
        return self.user_cache


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    ciudad = forms.CharField(
        max_length=100,
        label='Ciudad',
        widget=forms.TextInput(attrs={'autocomplete': 'address-level2'}),
    )
    comuna = forms.CharField(
        max_length=100,
        label='Comuna',
        widget=forms.TextInput(attrs={'autocomplete': 'address-level3'}),
    )
    direccion = forms.CharField(
        max_length=255,
        label='Dirección',
        widget=forms.TextInput(attrs={'autocomplete': 'street-address'}),
    )

    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden.',
    }

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'autocomplete': 'given-name'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'family-name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].help_text = (
            'Usa al menos 8 caracteres; evita contraseñas comunes, solo números '
            'o datos personales.'
        )
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].help_text = (
            'Escribe nuevamente la contraseña para confirmarla.'
        )
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise ValidationError('Ya existe una cuenta con ese correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f'cliente_{uuid.uuid4().hex}'
        if commit:
            with transaction.atomic():
                user.save()
                self.save_m2m()
                PerfilUsuario.objects.create(
                    usuario=user,
                    ciudad=self.cleaned_data['ciudad'],
                    comuna=self.cleaned_data['comuna'],
                    direccion=self.cleaned_data['direccion'],
                )
        return user


class AccountUpdateForm(forms.ModelForm):
    ciudad = forms.CharField(max_length=100, label='Ciudad')
    comuna = forms.CharField(max_length=100, label='Comuna')
    direccion = forms.CharField(max_length=255, label='Dirección')

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'autocomplete': 'given-name'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'family-name'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.profile = self.instance.perfil
        except PerfilUsuario.DoesNotExist:
            self.profile = None
        if self.profile:
            self.initial.update({
                'ciudad': self.profile.ciudad,
                'comuna': self.profile.comuna,
                'direccion': self.profile.direccion,
            })

    def clean_email(self):
        email = self.cleaned_data['email']
        users = get_user_model().objects.filter(email__iexact=email)
        if users.exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe una cuenta con ese correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = self.profile or PerfilUsuario(usuario=user)
            profile.ciudad = self.cleaned_data['ciudad']
            profile.comuna = self.cleaned_data['comuna']
            profile.direccion = self.cleaned_data['direccion']
            profile.save()
            self.profile = profile
        return user


class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'nombre',
            'categoria',
            'precio',
            'stock',
            'imagen_archivo',
            'imagen_url',
        )
        labels = {
            'nombre': 'Nombre del producto',
            'categoria': 'Grupo / categoría',
            'precio': 'Precio (CLP)',
            'stock': 'Stock',
            'imagen_archivo': 'Imagen local',
            'imagen_url': 'Enlace de imagen',
        }

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise ValidationError('El stock no puede ser negativo.')
        return stock

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        return precio
