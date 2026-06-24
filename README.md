# API de Finanzas Personales para Estudiantes Universitarios

## Descripción
API RESTful desarrollada con **Django Rest Framework** y **MongoDB** que permite a estudiantes universitarios administrar sus finanzas personales mediante el registro de ingresos, gastos, presupuestos y recomendaciones de ahorro.

## Tecnologías

> ⚠️ **VERSIONES FIJAS — no las cambien.** djongo 1.3.7 (su última versión) clava `django<=3.1.12`, `pymongo<=3.11.4` y `sqlparse==0.2.4`. Subir cualquiera rompe la instalación entera. Está congelado en la era de Django 3.1.

- **Python 3.9** (NO 3.10/3.11/3.12 — djongo se rompe en runtime)
- Django 3.1.12
- Django Rest Framework 3.14.0
- djongo 1.3.7 (conector Django-MongoDB)
- pymongo 3.11.4
- MongoDB (local en `localhost:27017`)

## Instalación

> **El orden importa:** Mongo prendido → `migrate` (crea la estructura) → `loaddata` (mete los datos). Nunca al revés.

### 0. Requisitos previos (una sola vez)

1. **Python 3.9** — https://www.python.org/downloads/release/python-390/ (en Windows: tildá *"Add Python to PATH"*).
2. **Git** — https://git-scm.com/downloads
3. **MongoDB Community Server** — https://www.mongodb.com/try/download/community
   - En Windows: dejá marcado *"Install MongoDB as a Service"* (arranca solo en `localhost:27017`).

### 1. Obtener el proyecto

**Si lo clonás de cero:**
```bash
git clone https://github.com/mazadelgadojoel/proyectoFinal-finanzas.git
cd proyectoFinal-finanzas
```

**Si ya lo tenías clonado:**
```bash
cd proyectoFinal-finanzas
git pull
```

### 2. Crear y activar el entorno virtual (Python 3.9)

**Windows (PowerShell):**
```powershell
py -3.9 -m venv venv
venv\Scripts\Activate.ps1
```
> Si PowerShell bloquea el script con un error de *execution policy*, corré antes:
> `Set-ExecutionPolicy -Scope Process Unrestricted`
> (o usá CMD y activá con `venv\Scripts\activate.bat`)

**Mac / Linux:**
```bash
python3.9 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Verificar que MongoDB esté corriendo

Debe estar escuchando en `localhost:27017`.
- **Windows:** `Get-Service MongoDB` — si dice *Stopped*, corré `net start MongoDB`.
- **Mac/Linux:** verificá tu servicio de mongod, o abrí MongoDB Compass.

### 5. Crear la estructura de la base
```bash
python manage.py migrate
```
> djongo imprime warnings tipo *"does not support X fully"* — son inofensivos.

### 6. Cargar los datos de ejemplo (75 registros)
```bash
python manage.py loaddata datos.json
```
> Si funcionó, verás: `Installed 75 object(s) from 1 fixture(s)`.

### 7. (Opcional) Crear superusuario para el panel admin
```bash
python manage.py createsuperuser
```

### 8. Iniciar el servidor
```bash
python manage.py runserver
```

La API estará disponible en: http://127.0.0.1:8000/api/

### Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `Connection refused` en migrate/loaddata | MongoDB apagado | Arrancá el servicio (`net start MongoDB` en Windows) |
| Falla `pip install` con conflicto de versiones | Usaste Python 3.10+ | Recreá el venv con Python **3.9** |
| `Activate.ps1` bloqueado | Política de PowerShell | `Set-ExecutionPolicy -Scope Process Unrestricted` o usá CMD |

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
├── datos_ejemplo.json           # 15 documentos JSON por colección (semilla original)
├── datos.json                   # Fixture de Django con 75 registros (para loaddata)
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
