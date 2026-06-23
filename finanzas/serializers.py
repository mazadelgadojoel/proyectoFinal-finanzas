"""
Serializers de la API de Finanzas Estudiantiles.

Los serializers convierten los objetos de Django (modelos) a formato JSON
para que la API pueda enviar y recibir datos. Funcionan como traductores
entre Python y JSON.
"""

from rest_framework import serializers
from .models import Usuario, Ingreso, Gasto, Presupuesto, Recomendacion


# ============================================================
# SERIALIZER DE USUARIO
# Convierte el modelo Usuario a JSON y viceversa.
# Incluye campos de solo lectura como fecha_registro.
# ============================================================
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ['fecha_registro']


# ============================================================
# SERIALIZER DE INGRESO
# Incluye el nombre del usuario como campo de solo lectura
# para que al consultar un ingreso se vea a quién pertenece.
# ============================================================
class IngresoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Ingreso
        fields = '__all__'


# ============================================================
# SERIALIZER DE GASTO
# Similar al de ingreso, incluye el nombre del usuario.
# ============================================================
class GastoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Gasto
        fields = '__all__'


# ============================================================
# SERIALIZER DE PRESUPUESTO
# Incluye el campo calculado porcentaje_usado y el nombre
# del usuario.
# ============================================================
class PresupuestoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    porcentaje_usado = serializers.ReadOnlyField()

    class Meta:
        model = Presupuesto
        fields = '__all__'


# ============================================================
# SERIALIZER DE RECOMENDACIÓN
# Incluye el nombre del usuario como referencia.
# ============================================================
class RecomendacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Recomendacion
        fields = '__all__'
        read_only_fields = ['fecha_creacion']


# ============================================================
# SERIALIZER DE REPORTE FINANCIERO
# Serializer especial que genera un resumen de las finanzas
# de un usuario: total ingresos, total gastos y balance.
# ============================================================
class ReporteFinancieroSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    nombre = serializers.CharField()
    total_ingresos = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_gastos = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    numero_ingresos = serializers.IntegerField()
    numero_gastos = serializers.IntegerField()
    presupuestos_activos = serializers.IntegerField()
