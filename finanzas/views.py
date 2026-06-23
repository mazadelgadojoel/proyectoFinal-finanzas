"""
Vistas de la API de Finanzas Estudiantiles.

Se utilizan ModelViewSet que proporcionan automáticamente
las operaciones CRUD (Create, Read, Update, Delete) para
cada colección. Cada ViewSet genera los siguientes endpoints:

- GET    /api/{recurso}/          → Listar todos
- POST   /api/{recurso}/          → Crear uno nuevo
- GET    /api/{recurso}/{id}/     → Obtener uno por ID
- PUT    /api/{recurso}/{id}/     → Actualizar completo
- PATCH  /api/{recurso}/{id}/     → Actualizar parcial
- DELETE /api/{recurso}/{id}/     → Eliminar
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Sum

from .models import Usuario, Ingreso, Gasto, Presupuesto, Recomendacion
from .serializers import (
    UsuarioSerializer,
    IngresoSerializer,
    GastoSerializer,
    PresupuestoSerializer,
    RecomendacionSerializer,
    ReporteFinancieroSerializer,
)


# ============================================================
# VISTA 1: USUARIOS
# CRUD completo para gestionar estudiantes.
# Endpoints adicionales:
#   - GET /api/usuarios/{id}/reporte/ → reporte financiero
# ============================================================
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar usuarios (estudiantes).

    list:    GET    /api/usuarios/        - Lista todos los usuarios
    create:  POST   /api/usuarios/        - Registra un nuevo usuario
    read:    GET    /api/usuarios/{id}/   - Consulta un usuario por ID
    update:  PUT    /api/usuarios/{id}/   - Actualiza un usuario completo
    partial: PATCH  /api/usuarios/{id}/   - Actualiza campos específicos
    delete:  DELETE /api/usuarios/{id}/   - Elimina un usuario
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=True, methods=['get'], url_path='reporte')
    def reporte_financiero(self, request, pk=None):
        """
        Genera un reporte financiero personalizado del usuario.
        GET /api/usuarios/{id}/reporte/

        Retorna: total ingresos, total gastos, balance,
        cantidad de movimientos y presupuestos activos.
        """
        usuario = self.get_object()

        total_ingresos = usuario.ingresos.aggregate(
            total=Sum('monto')
        )['total'] or 0

        total_gastos = usuario.gastos.aggregate(
            total=Sum('monto')
        )['total'] or 0

        reporte = {
            'usuario_id': usuario.id,
            'nombre': usuario.nombre,
            'total_ingresos': total_ingresos,
            'total_gastos': total_gastos,
            'balance': total_ingresos - total_gastos,
            'numero_ingresos': usuario.ingresos.count(),
            'numero_gastos': usuario.gastos.count(),
            'presupuestos_activos': usuario.presupuestos.count(),
        }

        serializer = ReporteFinancieroSerializer(reporte)
        return Response(serializer.data)


# ============================================================
# VISTA 2: INGRESOS
# CRUD completo para registrar fuentes de ingreso.
# Se puede filtrar por usuario con ?usuario={id}
# ============================================================
class IngresoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar ingresos de estudiantes.

    Filtros opcionales via query params:
      - ?usuario=1       → ingresos del usuario con id=1
      - ?categoria=beca  → solo ingresos de tipo beca
    """
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer

    def get_queryset(self):
        queryset = Ingreso.objects.all()
        usuario_id = self.request.query_params.get('usuario')
        categoria = self.request.query_params.get('categoria')

        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        return queryset


# ============================================================
# VISTA 3: GASTOS
# CRUD completo para registrar egresos.
# Se puede filtrar por usuario y categoría.
# ============================================================
class GastoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar gastos de estudiantes.

    Filtros opcionales via query params:
      - ?usuario=1               → gastos del usuario con id=1
      - ?categoria=alimentacion  → solo gastos de alimentación
      - ?necesario=true          → solo gastos necesarios
    """
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer

    def get_queryset(self):
        queryset = Gasto.objects.all()
        usuario_id = self.request.query_params.get('usuario')
        categoria = self.request.query_params.get('categoria')
        necesario = self.request.query_params.get('necesario')

        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if necesario is not None:
            queryset = queryset.filter(necesario=necesario.lower() == 'true')

        return queryset


# ============================================================
# VISTA 4: PRESUPUESTOS
# CRUD completo para definir límites de gasto.
# ============================================================
class PresupuestoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar presupuestos de estudiantes.

    Filtros opcionales via query params:
      - ?usuario=1        → presupuestos del usuario con id=1
      - ?periodo=mensual  → solo presupuestos mensuales
    """
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer

    def get_queryset(self):
        queryset = Presupuesto.objects.all()
        usuario_id = self.request.query_params.get('usuario')
        periodo = self.request.query_params.get('periodo')

        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)
        if periodo:
            queryset = queryset.filter(periodo=periodo)

        return queryset


# ============================================================
# VISTA 5: RECOMENDACIONES
# CRUD completo para consejos de ahorro.
# ============================================================
class RecomendacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar recomendaciones de ahorro.

    Filtros opcionales via query params:
      - ?usuario=1      → recomendaciones del usuario con id=1
      - ?prioridad=alta → solo recomendaciones de alta prioridad
      - ?tipo=ahorro    → solo recomendaciones de ahorro
    """
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer

    def get_queryset(self):
        queryset = Recomendacion.objects.all()
        usuario_id = self.request.query_params.get('usuario')
        prioridad = self.request.query_params.get('prioridad')
        tipo = self.request.query_params.get('tipo')

        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset


# ============================================================
# VISTA EXTRA: RESUMEN GENERAL
# Endpoint independiente que muestra un resumen de toda la API.
# GET /api/resumen/
# ============================================================
@api_view(['GET'])
def resumen_api(request):
    """
    Retorna un resumen general de la API:
    - Total de usuarios registrados
    - Total de ingresos y gastos registrados
    - Total de presupuestos y recomendaciones
    """
    data = {
        'nombre_api': 'API de Finanzas Personales para Estudiantes Universitarios',
        'version': '1.0',
        'estadisticas': {
            'total_usuarios': Usuario.objects.count(),
            'total_ingresos': Ingreso.objects.count(),
            'total_gastos': Gasto.objects.count(),
            'total_presupuestos': Presupuesto.objects.count(),
            'total_recomendaciones': Recomendacion.objects.count(),
        },
        'endpoints': {
            'usuarios': '/api/usuarios/',
            'ingresos': '/api/ingresos/',
            'gastos': '/api/gastos/',
            'presupuestos': '/api/presupuestos/',
            'recomendaciones': '/api/recomendaciones/',
            'reporte_usuario': '/api/usuarios/{id}/reporte/',
        }
    }
    return Response(data)
