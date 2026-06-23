"""
Registro de modelos en el panel de administración de Django.
Permite gestionar los datos desde /admin/
"""

from django.contrib import admin
from .models import Usuario, Ingreso, Gasto, Presupuesto, Recomendacion


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'universidad', 'carrera', 'semestre', 'activo')
    search_fields = ('nombre', 'correo', 'universidad')
    list_filter = ('universidad', 'activo', 'semestre')


@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'monto', 'fecha', 'recurrente')
    search_fields = ('descripcion',)
    list_filter = ('categoria', 'recurrente', 'fecha')


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'monto', 'fecha', 'metodo_pago', 'necesario')
    search_fields = ('descripcion',)
    list_filter = ('categoria', 'metodo_pago', 'necesario', 'fecha')


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'monto_limite', 'monto_gastado', 'periodo')
    list_filter = ('periodo', 'alerta_activada')


@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'titulo', 'prioridad', 'aplicada')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('tipo', 'prioridad', 'aplicada')
