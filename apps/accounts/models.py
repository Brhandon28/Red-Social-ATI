from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        PROFESIONAL = 'profesional', _('Profesional')
        EMPRESA = 'empresa', _('Empresa')
        ADMINISTRADOR = 'administrador', _('Administrador')

    class EstadoCuenta(models.TextChoices):
        ACTIVO = 'activo', _('Activo')
        INACTIVO = 'inactivo', _('Inactivo')
        SUSPENDIDO = 'suspendido', _('Suspendido')

    nombreMostrado = models.CharField(
        _('nombre mostrado'),
        max_length=150,
        blank=True,
    )
    profileImage = models.ImageField(
        _('foto de perfil'),
        upload_to='profiles/',
        blank=True,
        null=True,
    )
    bannerImage = models.ImageField(
        _('banner de perfil'),
        upload_to='profile_banners/',
        blank=True,
        null=True,
    )
    tipoUsuario = models.CharField(
        _('tipo de usuario'),
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.PROFESIONAL,
    )
    estado = models.CharField(
        _('estado'),
        max_length=20,
        choices=EstadoCuenta.choices,
        default=EstadoCuenta.ACTIVO,
    )

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        permissions = [
            ('puede_moderar', _('Puede moderar contenido')),
            ('puede_gestionar_usuarios', _('Puede gestionar usuarios')),
        ]

    def __str__(self):
        return self.nombreMostrado or self.get_full_name() or self.username

    def save(self, *args, **kwargs):
        if not self.nombreMostrado:
            self.nombreMostrado = self.get_full_name() or self.username
        super().save(*args, **kwargs)


class Profesional(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profesional',
        verbose_name=_('usuario'),
    )
    nombre = models.CharField(_('nombre'), max_length=100)
    apellido = models.CharField(_('apellido'), max_length=100)
    fechaNac = models.DateField(_('fecha de nacimiento'), null=True, blank=True)
    experienciaLaboral = models.TextField(
        _('experiencia laboral'),
        blank=True,
        default='',
    )
    certificaciones = models.TextField(
        _('certificaciones'),
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = _('profesional')
        verbose_name_plural = _('profesionales')

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Empresa(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='empresa',
        verbose_name=_('usuario'),
    )
    razonSocial = models.CharField(_('razón social'), max_length=200)
    infoEmpresa = models.TextField(
        _('información de la empresa'),
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = _('empresa')
        verbose_name_plural = _('empresas')

    def __str__(self):
        return self.razonSocial


class Administrador(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='administrador',
        verbose_name=_('usuario'),
    )
    nivelDePermisos = models.CharField(
        _('nivel de permisos'),
        max_length=50,
        default='total',
    )
    rol = models.CharField(
        _('rol'),
        max_length=100,
        default='administrador',
    )

    class Meta:
        verbose_name = _('administrador')
        verbose_name_plural = _('administradores')

    def __str__(self):
        return f'{self.usuario} - {self.rol}'
