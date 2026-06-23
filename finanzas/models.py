"""
Modelos de la API de Finanzas Personales para Estudiantes Universitarios.

Colecciones en MongoDB:
1. Usuarios        - Registro y perfil de estudiantes
2. Ingresos        - Fuentes de dinero del estudiante
3. Gastos          - Egresos y compras del estudiante
4. Presupuestos    - Límites de gasto por categoría
5. Recomendaciones - Consejos de ahorro personalizados
"""

from django.db import models


# ============================================================
# COLECCIÓN 1: USUARIOS
# Almacena la información personal y académica del estudiante.
# Cada usuario puede tener múltiples ingresos, gastos,
# presupuestos y recomendaciones asociadas.
# ============================================================
class Usuario(models.Model):
    nombre = models.CharField(max_length=100, help_text="Nombre completo del estudiante")
    correo = models.EmailField(unique=True, help_text="Correo electrónico institucional")
    contrasena = models.CharField(max_length=255, help_text="Contraseña del usuario")
    universidad = models.CharField(max_length=150, help_text="Universidad donde estudia")
    carrera = models.CharField(max_length=150, help_text="Carrera que cursa")
    semestre = models.IntegerField(help_text="Semestre actual")
    fecha_registro = models.DateTimeField(auto_now_add=True, help_text="Fecha de registro en la plataforma")
    activo = models.BooleanField(default=True, help_text="Indica si la cuenta está activa")

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} - {self.universidad}"


# ============================================================
# COLECCIÓN 2: INGRESOS
# Registra todas las fuentes de ingreso del estudiante:
# beca, trabajo, mesada, freelance, etc.
# ============================================================
class Ingreso(models.Model):
    CATEGORIAS_INGRESO = [
        ('beca', 'Beca'),
        ('trabajo', 'Trabajo'),
        ('mesada', 'Mesada familiar'),
        ('freelance', 'Trabajo freelance'),
        ('venta', 'Venta de productos'),
        ('otro', 'Otro'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='ingresos',
        help_text="Estudiante al que pertenece este ingreso"
    )
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_INGRESO, help_text="Tipo de ingreso")
    monto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cantidad en pesos MXN")
    descripcion = models.CharField(max_length=255, help_text="Descripción del ingreso")
    fecha = models.DateField(help_text="Fecha en que se recibió el ingreso")
    recurrente = models.BooleanField(default=False, help_text="¿Es un ingreso recurrente?")

    class Meta:
        db_table = 'ingresos'
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.categoria} - ${self.monto} ({self.usuario.nombre})"


# ============================================================
# COLECCIÓN 3: GASTOS
# Registra todos los egresos del estudiante:
# alimentación, transporte, material escolar, etc.
# ============================================================
class Gasto(models.Model):
    CATEGORIAS_GASTO = [
        ('alimentacion', 'Alimentación'),
        ('transporte', 'Transporte'),
        ('material_escolar', 'Material escolar'),
        ('entretenimiento', 'Entretenimiento'),
        ('salud', 'Salud'),
        ('renta', 'Renta / Vivienda'),
        ('servicios', 'Servicios (luz, agua, internet)'),
        ('ropa', 'Ropa'),
        ('tecnologia', 'Tecnología'),
        ('otro', 'Otro'),
    ]

    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta_debito', 'Tarjeta de débito'),
        ('tarjeta_credito', 'Tarjeta de crédito'),
        ('transferencia', 'Transferencia bancaria'),
        ('app_pago', 'App de pago (mercado pago, etc.)'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='gastos',
        help_text="Estudiante al que pertenece este gasto"
    )
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_GASTO, help_text="Tipo de gasto")
    monto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cantidad gastada en pesos MXN")
    descripcion = models.CharField(max_length=255, help_text="Descripción del gasto")
    fecha = models.DateField(help_text="Fecha del gasto")
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, default='efectivo', help_text="Método de pago utilizado")
    necesario = models.BooleanField(default=True, help_text="¿Es un gasto necesario o prescindible?")

    class Meta:
        db_table = 'gastos'
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.categoria} - ${self.monto} ({self.usuario.nombre})"


# ============================================================
# COLECCIÓN 4: PRESUPUESTOS
# Permite al estudiante definir límites de gasto
# por categoría y periodo (semanal, quincenal, mensual).
# ============================================================
class Presupuesto(models.Model):
    PERIODOS = [
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='presupuestos',
        help_text="Estudiante al que pertenece este presupuesto"
    )
    categoria = models.CharField(max_length=50, help_text="Categoría del presupuesto (alimentación, transporte, etc.)")
    monto_limite = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto máximo asignado")
    monto_gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Monto gastado hasta el momento")
    periodo = models.CharField(max_length=20, choices=PERIODOS, default='mensual', help_text="Periodo del presupuesto")
    fecha_inicio = models.DateField(help_text="Fecha de inicio del periodo")
    fecha_fin = models.DateField(help_text="Fecha de fin del periodo")
    alerta_activada = models.BooleanField(default=True, help_text="¿Activar alerta al llegar al 80% del límite?")

    class Meta:
        db_table = 'presupuestos'
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'

    def __str__(self):
        return f"{self.categoria} - Límite: ${self.monto_limite} ({self.usuario.nombre})"

    @property
    def porcentaje_usado(self):
        """Calcula el porcentaje del presupuesto utilizado."""
        if self.monto_limite > 0:
            return round((self.monto_gastado / self.monto_limite) * 100, 2)
        return 0


# ============================================================
# COLECCIÓN 5: RECOMENDACIONES
# Consejos de ahorro personalizados para el estudiante,
# basados en sus patrones de gasto e ingreso.
# ============================================================
class Recomendacion(models.Model):
    PRIORIDADES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    TIPOS = [
        ('ahorro', 'Ahorro'),
        ('reduccion_gasto', 'Reducción de gasto'),
        ('inversion', 'Inversión'),
        ('habito', 'Hábito financiero'),
        ('alerta', 'Alerta de presupuesto'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='recomendaciones',
        help_text="Estudiante al que va dirigida la recomendación"
    )
    tipo = models.CharField(max_length=50, choices=TIPOS, help_text="Tipo de recomendación")
    titulo = models.CharField(max_length=200, help_text="Título de la recomendación")
    descripcion = models.TextField(help_text="Detalle de la recomendación")
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='media', help_text="Nivel de prioridad")
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text="Fecha en que se generó")
    aplicada = models.BooleanField(default=False, help_text="¿El estudiante ya aplicó esta recomendación?")

    class Meta:
        db_table = 'recomendaciones'
        verbose_name = 'Recomendación'
        verbose_name_plural = 'Recomendaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} ({self.usuario.nombre})"
