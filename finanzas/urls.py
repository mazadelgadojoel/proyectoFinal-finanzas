"""
Rutas de la API de Finanzas Estudiantiles.

Se usa DefaultRouter de Django Rest Framework, que genera
automáticamente todas las rutas CRUD para cada ViewSet:

  /api/usuarios/          → GET (listar), POST (crear)
  /api/usuarios/{id}/     → GET (detalle), PUT, PATCH, DELETE
  /api/usuarios/{id}/reporte/ → GET (reporte financiero)

  /api/ingresos/          → GET, POST
  /api/ingresos/{id}/     → GET, PUT, PATCH, DELETE

  /api/gastos/            → GET, POST
  /api/gastos/{id}/       → GET, PUT, PATCH, DELETE

  /api/presupuestos/      → GET, POST
  /api/presupuestos/{id}/ → GET, PUT, PATCH, DELETE

  /api/recomendaciones/          → GET, POST
  /api/recomendaciones/{id}/     → GET, PUT, PATCH, DELETE

  /api/resumen/           → GET (resumen general de la API)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# El router genera automáticamente las URLs para cada ViewSet
router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'ingresos', views.IngresoViewSet)
router.register(r'gastos', views.GastoViewSet)
router.register(r'presupuestos', views.PresupuestoViewSet)
router.register(r'recomendaciones', views.RecomendacionViewSet)

urlpatterns = [
    # Ruta del resumen general
    path('resumen/', views.resumen_api, name='resumen-api'),
    # Todas las rutas del router
    path('', include(router.urls)),
]
