from django.contrib import admin
from .models import Autor, Libro, Genero, EjemplarLibro

admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(Genero)
admin.site.register(EjemplarLibro)