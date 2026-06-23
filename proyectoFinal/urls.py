"""
URL configuration for proyectoFinal project.
Rutas principales del proyecto.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    # Todas las rutas de la API de finanzas
    path('api/', include('finanzas.urls')),
]
