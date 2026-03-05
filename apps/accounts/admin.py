from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Usuario, Profesional, Empresa, Administrador


class ProfesionalInline(admin.StackedInline):
    model = Profesional
    can_delete = False
    verbose_name = _('Perfil profesional')
    verbose_name_plural = _('Perfil profesional')


class EmpresaInline(admin.StackedInline):
    model = Empresa
    can_delete = False
    verbose_name = _('Perfil empresa')
    verbose_name_plural = _('Perfil empresa')


class AdministradorInline(admin.StackedInline):
    model = Administrador
    can_delete = False
    verbose_name = _('Perfil administrador')
    verbose_name_plural = _('Perfil administrador')


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'nombreMostrado',
        'tipoUsuario',
        'estado',
        'is_staff',
        'is_active',
    )
    list_filter = ('tipoUsuario', 'estado', 'is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'nombreMostrado', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        (_('Información SOCIALIT'), {
            'fields': ('nombreMostrado', 'tipoUsuario', 'estado'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Información SOCIALIT'), {
            'fields': ('email', 'nombreMostrado', 'tipoUsuario', 'estado'),
        }),
    )

    inlines = [ProfesionalInline, EmpresaInline, AdministradorInline]


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre', 'apellido', 'fechaNac')
    search_fields = ('nombre', 'apellido', 'usuario__email')
    list_filter = ('fechaNac',)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'razonSocial')
    search_fields = ('razonSocial', 'usuario__email')


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nivelDePermisos', 'rol')
    search_fields = ('usuario__email', 'rol')
    list_filter = ('nivelDePermisos', 'rol')
