from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Usuario, Profesional, Empresa


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Correo Electrónico'),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': _('ejemplo@correo.com'),
            'autocomplete': 'email',
        }),
    )
    password = forms.CharField(
        label=_('Contraseña'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': _('Tu contraseña'),
            'autocomplete': 'current-password',
        }),
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Buscar usuario por email
            from .models import Usuario
            try:
                user = Usuario.objects.get(email=email)
                self.cleaned_data['username'] = user.username
            except Usuario.DoesNotExist:
                pass

        return super().clean()


class RegistroProfesionalForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('Nombre'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Tu nombre'),
            'autocomplete': 'given-name',
        }),
    )
    last_name = forms.CharField(
        label=_('Apellido'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Tu apellido'),
            'autocomplete': 'family-name',
        }),
    )
    email = forms.EmailField(
        label=_('Correo Electrónico'),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': _('ejemplo@correo.com'),
            'autocomplete': 'email',
        }),
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.tipoUsuario = Usuario.TipoUsuario.PROFESIONAL
        user.nombreMostrado = (
            f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        )
        if commit:
            user.save()
            Profesional.objects.create(
                usuario=user,
                nombre=self.cleaned_data['first_name'],
                apellido=self.cleaned_data['last_name'],
            )
        return user


class RegistroEmpresaForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('Nombre de la Empresa'),
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Nombre de la empresa'),
        }),
    )
    last_name = forms.CharField(
        label=_('RIF / NIT'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('J-12345678-9'),
        }),
    )
    email = forms.EmailField(
        label=_('Correo Corporativo'),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': _('empresa@correo.com'),
            'autocomplete': 'email',
        }),
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.tipoUsuario = Usuario.TipoUsuario.EMPRESA
        user.nombreMostrado = self.cleaned_data['first_name']
        if commit:
            user.save()
            Empresa.objects.create(
                usuario=user,
                razonSocial=self.cleaned_data['first_name'],
                infoEmpresa='',
            )
        return user
