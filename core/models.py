from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Univalluno(models.Model):

    TIPO_DOCUMENTO = [
        ("TI", "Tarjeta de Idetidad"),
        ("CC", "Cedula de Ciudadania"),
    ]

    TIPO_UNIVALLUNO = [
        ("E", "Estudiante"),
        ("F", "Funcionario"),
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipoDeUnivalluna = models.CharField(max_length=1,choices=TIPO_UNIVALLUNO)
    tipoDeDocumento = models.CharField(max_length=2,choices=TIPO_DOCUMENTO)
    numeroDeDocumento = models.CharField(max_length=50)
    codigoDeEstudiante = models.CharField(max_length=50)
    email = models.EmailField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipoDeDocumento', 'numeroDeDocumento'], name='unico numero de documento por tipo de documento')
        ]


class ArticuloDeportivo(models.Model):
    nombre = models.CharField(max_length=100)
    deporte = models.CharField(max_length=100)
    descripcion = models.TextField(max_length = 800)
    valor = models.CharField(max_length=100)
    disponible = models.BooleanField(default = False)

class Prestamos(models.Model):
    univalluno = models.ForeignKey(Univalluno, on_delete=models.CASCADE)
    articuloDeportivo = models.ForeignKey(ArticuloDeportivo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento_prestamos = models.DateTimeField()

class Multas(models.Model):
    univalluno = models.ForeignKey(Univalluno, on_delete=models.CASCADE)
    articuloDeportivo = models.ForeignKey(ArticuloDeportivo, on_delete=models.CASCADE)
    prestamo = models.ForeignKey(Prestamos, on_delete=models.CASCADE)
    valor = models.IntegerField()
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(auto_now_add=True)