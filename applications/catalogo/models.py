import uuid

from django.db import models
from django.urls import reverse


# Create your models here.

class Genero(models.Model):
    """Modelo que representa un género literario."""
    nombre = models.CharField(max_length=200, help_text="Ingrese el nombre del género")

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    """Modelo que representa un autor."""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_fallecimiento = models.DateField('Fallecido', null=True, blank=True)
    biografia = models.TextField(max_length=1000, blank=True)

    class Meta:
        ordering = ['apellido', 'nombre']

    def get_absolute_url(self):
        return reverse('autor-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Libro(models.Model):
    """ Modelo que representa un libro (pero no un ejemplar específico). """

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, related_name='libros')
    resumen = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>')
    genero = models.ManyToManyField(Genero, help_text="Seleccione un género para este libro")
    idioma = models.CharField(max_length=20, default='Español')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio del libro")
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True, help_text="Portada del libro")
    class Meta:
        ordering = ['titulo']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('libro-detail', args=[str(self.id)])


class EjemplarLibro(models.Model):
    """Modelo que representa una copia específica de un libro."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="ID único para este ejemplar particular")
    libro = models.ForeignKey(Libro, on_delete=models.RESTRICT, related_name='ejemplares')
    fecha_adquisicion = models.DateField(null=True, blank=True)
    fecha_devolucion = models.DateField(null=True, blank=True)

    ESTADO_PRESTAMO = (
        ('m', 'Mantenimiento'),
        ('p', 'Prestado'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estado = models.CharField(
        max_length=1,
        choices=ESTADO_PRESTAMO,
        blank=True,
        default='d',
        help_text='Disponibilidad del libro',
    )

    class Meta:
        ordering = ['fecha_devolucion']
        permissions = (("puede_marcar_devuelto", "Marcar libro como devuelto"),)

    def __str__(self):
        return f"{self.id} ({self.libro.titulo})"

class Prestamo(models.Model):
    """Modelo que representa una solicitud de préstamo hecha por un visitante."""
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ejemplar = models.ForeignKey(EjemplarLibro, on_delete=models.CASCADE, related_name='prestamos')
    nombre_solicitante = models.CharField(max_length=150)
    correo_solicitante = models.EmailField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Préstamo {self.codigo} - {self.ejemplar.libro.titulo}"