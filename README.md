# API de Finanzas Personales para Estudiantes Universitarios

## Descripción
API RESTful desarrollada con **Django Rest Framework** y **MongoDB** que permite a estudiantes universitarios administrar sus finanzas personales mediante el registro de ingresos, gastos, presupuestos y recomendaciones de ahorro.

## Tecnologías
- Python 3.10+
- Django 4.2
- Django Rest Framework 3.14
- MongoDB 6.0+ (con MongoDB Compass)
- Djongo (conector Django-MongoDB)

## Instalación

### 1. Clonar o descomprimir el proyecto
```bash
cd proyectoFinal
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Asegurar que MongoDB esté corriendo
```bash
# MongoDB debe estar corriendo en localhost:27017
# Puedes verificarlo abriendo MongoDB Compass
```

### 5. Ejecutar migraciones
```bash
python manage.py makemigrations finanzas
python manage.py migrate
```

### 6. Crear superusuario (opcional, para el panel admin)
```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor
```bash
python manage.py runserver
```

La API estará disponible en: http://127.0.0.1:8000/api/

## Colecciones de la Base de Datos

| # | Colección       | Descripción                                      |
|---|-----------------|--------------------------------------------------|
| 1 | Usuarios        | Perfil y datos académicos del estudiante         |
| 2 | Ingresos        | Fuentes de dinero (beca, trabajo, mesada, etc.)  |
| 3 | Gastos          | Egresos (alimentación, transporte, renta, etc.)  |
| 4 | Presupuestos    | Límites de gasto por categoría y periodo         |
| 5 | Recomendaciones | Consejos de ahorro personalizados                |

## Tabla de Rutas de la API RESTful

| Ruta                                | Método          | Descripción                                    |
|-------------------------------------|-----------------|------------------------------------------------|
| admin/                              | GET             | Panel de administración de Django              |
| api/                                | GET             | Raíz de la API - lista todos los endpoints     |
| api/resumen/                        | GET             | Resumen general con estadísticas de la API     |
| api/usuarios/                       | GET             | Lista todos los usuarios registrados           |
| api/usuarios/                       | POST            | Registra un nuevo estudiante                   |
| api/usuarios/{id}/                  | GET             | Consulta un usuario por su ID                  |
| api/usuarios/{id}/                  | PUT             | Actualiza todos los datos de un usuario        |
| api/usuarios/{id}/                  | PATCH           | Actualiza campos específicos de un usuario     |
| api/usuarios/{id}/                  | DELETE          | Elimina un usuario                             |
| api/usuarios/{id}/reporte/          | GET             | Genera reporte financiero del usuario          |
| api/ingresos/                       | GET             | Lista todos los ingresos                       |
| api/ingresos/                       | POST            | Registra un nuevo ingreso                      |
| api/ingresos/{id}/                  | GET             | Consulta un ingreso por su ID                  |
| api/ingresos/{id}/                  | PUT / PATCH     | Actualiza un ingreso                           |
| api/ingresos/{id}/                  | DELETE          | Elimina un ingreso                             |
| api/ingresos/?usuario=1             | GET             | Filtra ingresos por usuario                    |
| api/ingresos/?categoria=beca        | GET             | Filtra ingresos por categoría                  |
| api/gastos/                         | GET             | Lista todos los gastos                         |
| api/gastos/                         | POST            | Registra un nuevo gasto                        |
| api/gastos/{id}/                    | GET             | Consulta un gasto por su ID                    |
| api/gastos/{id}/                    | PUT / PATCH     | Actualiza un gasto                             |
| api/gastos/{id}/                    | DELETE          | Elimina un gasto                               |
| api/gastos/?usuario=1               | GET             | Filtra gastos por usuario                      |
| api/gastos/?categoria=alimentacion  | GET             | Filtra gastos por categoría                    |
| api/gastos/?necesario=true          | GET             | Filtra gastos necesarios vs prescindibles      |
| api/presupuestos/                   | GET             | Lista todos los presupuestos                   |
| api/presupuestos/                   | POST            | Crea un nuevo presupuesto                      |
| api/presupuestos/{id}/              | GET             | Consulta un presupuesto por su ID              |
| api/presupuestos/{id}/              | PUT / PATCH     | Actualiza un presupuesto                       |
| api/presupuestos/{id}/              | DELETE          | Elimina un presupuesto                         |
| api/presupuestos/?periodo=mensual   | GET             | Filtra presupuestos por periodo                |
| api/recomendaciones/                | GET             | Lista todas las recomendaciones                |
| api/recomendaciones/                | POST            | Crea una nueva recomendación                   |
| api/recomendaciones/{id}/           | GET             | Consulta una recomendación por su ID           |
| api/recomendaciones/{id}/           | PUT / PATCH     | Actualiza una recomendación                    |
| api/recomendaciones/{id}/           | DELETE          | Elimina una recomendación                      |
| api/recomendaciones/?prioridad=alta | GET             | Filtra recomendaciones por prioridad           |
| api/recomendaciones/?tipo=ahorro    | GET             | Filtra recomendaciones por tipo                |

## Estructura del Proyecto
```
proyectoFinal/
├── manage.py                    # Punto de entrada de Django
├── requirements.txt             # Dependencias
├── datos_ejemplo.json           # 15 documentos JSON por colección
├── README.md                    # Esta documentación
├── proyectoFinal/               # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py              # Configuración (MongoDB, DRF, etc.)
│   ├── urls.py                  # Rutas principales
│   ├── wsgi.py                  # Despliegue WSGI
│   └── asgi.py                  # Despliegue ASGI
└── finanzas/                    # App principal
    ├── __init__.py
    ├── apps.py                  # Configuración de la app
    ├── models.py                # 5 modelos (colecciones)
    ├── serializers.py           # Conversión modelo <-> JSON
    ├── views.py                 # Lógica de los endpoints
    ├── urls.py                  # Rutas de la API
    ├── admin.py                 # Registro en panel admin
    └── tests.py                 # Pruebas
```

## Autores
- [Nombres de los integrantes del equipo]

## Materia
Programación y Arquitectura de Aplicaciones - EBC
