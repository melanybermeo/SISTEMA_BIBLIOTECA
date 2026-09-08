from applications.catalogo.models import *

""" Consultas básicas """

# 1. Todos los libros
libros = Libro.objects.all()

# 2. Libros ordenados por título
libros = Libro.objects.order_by('titulo')

# 3. Filtrado por autor
libros_de_autor = Libro.objects.filter(autor__apellido='García Márquez')

# 4. Búsqueda por palabra clave en título o resumen
from django.db.models import Q

libros = Libro.objects.filter(Q(titulo__icontains='quijote') | Q(resumen__icontains='quijote'))

# 5. Ejemplares disponibles
ejemplares_disponibles = EjemplarLibro.objects.filter(estado='d')

""" Consultas avanzadas """
# 6. Contar libros por género
from django.db.models import Count

generos_con_conteo = Genero.objects.annotate(num_libros=Count('libro'))

# 7. Autores con sus libros (evitando N+1 query)
autores_con_libros = Autor.objects.prefetch_related('libros')

# 8. Libro con su autor (evitando N+1 query)
libros_con_autor = Libro.objects.select_related('autor')

# 9. Contar ejemplares por estado
from django.db.models import Count, Case, When, IntegerField

libro_stats = Libro.objects.annotate(
    ejemplares_disponibles=Count(
        Case(
            When(ejemplares__estado='d', then=1),
            output_field=IntegerField()
        )
    ),
    ejemplares_prestados=Count(
        Case(
            When(ejemplares__estado='p', then=1),
            output_field=IntegerField()
        )
    )
)

# 10. Consulta compleja: libros que no tienen ejemplares disponibles
libros_sin_disponibles = Libro.objects.exclude(
    ejemplares__estado='d'
).distinct()

# 11. Libros con múltiples filtros combinados
libros = Libro.objects.filter(
    Q(autor__apellido='Cervantes') &
    (Q(genero__nombre='Novela') | Q(genero__nombre='Clásico')) &
    ~Q(ejemplares__estado='m')
).distinct()

""" Introspección de múltiples registros """


# Ejemplo detallado: Recorrer múltiples registros y mostrar sus campos
def inspeccionar_multiples_registros():
    """
    Función para demostrar cómo recorrer múltiples registros
    y mostrar todos sus campos de manera eficiente.
    """

    # 1. Optimizar la consulta para evitar el problema N+1
    # Usamos select_related para cargar las relaciones ForeignKey
    # y prefetch_related para las relaciones ManyToMany
    libros = Libro.objects.select_related('autor').prefetch_related('genero')

    # Podríamos añadir filtros si fuera necesario
    # libros = libros.filter(publicado__year__gte=2000)

    total_libros = libros.count()

    print(f"\n{'=' * 60}")
    print(f"ANÁLISIS DE {total_libros} LIBROS (CON OPTIMIZACIÓN DE CONSULTAS)")
    print(f"{'=' * 60}")

    # 2. Recorrer cada registro
    for i, libro in enumerate(libros, 1):
        print(f"\n[LIBRO {i}/{total_libros}]: {libro.titulo}")
        print(f"{'-' * 50}")

        # 3. Mostrar campos básicos usando introspección
        for campo in libro._meta.fields:
            nombre_campo = campo.name
            tipo_campo = campo.get_internal_type()
            valor = getattr(libro, nombre_campo)

            # Tratar de manera especial diferentes tipos de campos
            if tipo_campo == 'ForeignKey' or tipo_campo == 'OneToOneField':
                if valor:
                    print(f"{nombre_campo} ({tipo_campo}): {valor} [ID: {valor.id}]")
                else:
                    print(f"{nombre_campo} ({tipo_campo}): None")
            elif tipo_campo == 'DateField' or tipo_campo == 'DateTimeField':
                print(f"{nombre_campo} ({tipo_campo}): {valor}")
            else:
                print(f"{nombre_campo} ({tipo_campo}): {valor}")

        # 4. Mostrar campos ManyToMany
        for campo in libro._meta.many_to_many:
            nombre_campo = campo.name
            objetos_relacionados = getattr(libro, nombre_campo).all()

            print(f"\n{nombre_campo} (ManyToManyField):")
            if objetos_relacionados.exists():
                for obj in objetos_relacionados:
                    print(f"  - {obj} [ID: {obj.id}]")
            else:
                print("  - No hay objetos relacionados")

        # 5. Estadísticas y resumen

        print(f"\n{'=' * 60}")
        print("RESUMEN DE ANÁLISIS:")
        print(f"{'-' * 50}")
        print(f"Total de libros analizados: {total_libros}")

        # Podríamos añadir estadísticas adicionales
        generos_counts = {}
        for libro in libros:
            for genero in libro.genero.all():
                generos_counts[genero.nombre] = generos_counts.get(genero.nombre, 0) + 1

        if generos_counts:
            print("\nDistribución por género literario:")
            for genero, count in sorted(generos_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {genero}: {count} libros ({count / total_libros:.1%})")


# Llamado de la función para un ejemplo práctico
# inspeccionar_multiples_registros()

"""  Relaciones entre Modelos """


#  Relación Uno a Muchos (ForeignKey)

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    publicado = models.DateField()

    def __str__(self):
        return self.titulo


#  Relación Muchos a Muchos (ManyToManyField)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    # ... otros campos
    categorias = models.ManyToManyField(Categoria, related_name='libros')


# Relación Uno a Uno (OneToOneField)

class DetalleAutor(models.Model):
    autor = models.OneToOneField(Autor, on_delete=models.CASCADE, related_name='detalle')
    biografia = models.TextField()
    website = models.URLField(blank=True)


'''  Operadores de Consulta (Field Lookups) '''

# Contiene
libros = Libro.objects.filter(titulo__contains='don')

# Contiene (case-insensitive)
libros = Libro.objects.filter(titulo__icontains='don')

# Empieza con
libros = Libro.objects.filter(titulo__startswith='El')

# Termina con
libros = Libro.objects.filter(titulo__endswith='Quijote')

# Mayor que
libros = Libro.objects.filter(publicado__gt='2000-01-01')

# Menor que
libros = Libro.objects.filter(publicado__lt='2000-01-01')

# En una lista
libros = Libro.objects.filter(id__in=[1, 2, 3])

# Rango
libros = Libro.objects.filter(publicado__range=('2000-01-01', '2010-12-31'))

# Isnull
autores = Autor.objects.filter(fecha_nacimiento__isnull=True)

""" Consultas Q para Operaciones OR y Operaciones Complejas """

from django.db.models import Q

# OR
libros = Libro.objects.filter(Q(titulo__contains='don') | Q(titulo__contains='quijote'))

# AND
libros = Libro.objects.filter(Q(titulo__contains='don') & Q(publicado__year=1605))

# NOT
libros = Libro.objects.filter(~Q(autor__apellido='Cervantes'))

# Combinaciones complejas
libros = Libro.objects.filter(
    (Q(publicado__year__gte=2000) | Q(autor__apellido='Cervantes')) &
    ~Q(categorias__nombre='Poesía')
)

"""  Agregaciones y Anotaciones """

from django.db.models import Count, Sum, Avg, Min, Max, F, Q

# Agregaciones básicas
# Contar todos los libros
total_libros = Libro.objects.count()

# Calcular el precio promedio de todos los libros
precio_promedio = Libro.objects.aggregate(promedio=Avg('precio'))

# Múltiples agregaciones en una consulta
estadisticas = Libro.objects.aggregate(
    total=Count('id'),
    precio_promedio=Avg('precio'),
    precio_maximo=Max('precio'),
    precio_minimo=Min('precio'),
    suma_total=Sum('precio')
)

# Anotaciones
# Anotar el número de libros por autor
autores_con_conteo = Autor.objects.annotate(num_libros=Count('libros'))
for autor in autores_con_conteo:
    print(f"{autor.nombre} {autor.apellido}: {autor.num_libros} libros")

# Anotar con filtros (libros publicados después de 2000)
autores_con_libros_recientes = Autor.objects.annotate(
    libros_recientes=Count('libros', filter=Q(libros__publicado__year__gt=2000))
)

# Ordenar por campo anotado
autores_populares = Autor.objects.annotate(
    num_libros=Count('libros')
).order_by('-num_libros')[:5]  # Top 5 autores con más libros

# Filtrar por campo anotado
autores_prolificos = Autor.objects.annotate(
    num_libros=Count('libros')
).filter(num_libros__gt=5)  # Autores con más de 5 libros

# Combinando anotaciones y F expressions
libros_con_descuento = Libro.objects.annotate(
    precio_descuento=F('precio') * 0.9
)

# Anotaciones complejas con múltiples consultas relacionadas
libros_stats = Libro.objects.annotate(
    num_ejemplares=Count('ejemplares'),
    ejemplares_disponibles=Count('ejemplares', filter=Q(ejemplares__estado='d')),
    ejemplares_prestados=Count('ejemplares', filter=Q(ejemplares__estado='p')),
    porcentaje_disponibilidad=100.0 * Count('ejemplares', filter=Q(ejemplares__estado='d')) / Count('ejemplares'))

""" Optimización de Consultas """

# Sin optimización - Genera N+1 consultas
libros = Libro.objects.all()
for libro in libros:
    print(libro.autor.nombre)  # Consulta adicional por cada libro

# Con select_related (para ForeignKey y OneToOneField) - Solo 1 consulta
libros = Libro.objects.select_related('autor')
for libro in libros:
    print(libro.autor.nombre)  # No genera consultas adicionales

# Con prefetch_related (para ManyToManyField o consultas "inversas") - 2 consultas
libros = Libro.objects.prefetch_related('categorias')
for libro in libros:
    for categoria in libro.categorias.all():  # No genera consultas adicionales
        print(categoria.nombre)

# Combinar ambos para optimizar múltiples tipos de relaciones
libros = Libro.objects.select_related('autor').prefetch_related('categorias')

"""  Ejemplos de optimización de consultas """

# Sin optimización - Genera N+1 consultas
libros = Libro.objects.all()
for libro in libros:
    print(libro.autor.nombre)  # Consulta adicional por cada libro

# Con select_related (para ForeignKey y OneToOneField) - Solo 1 consulta
libros = Libro.objects.select_related('autor')
for libro in libros:
    print(libro.autor.nombre)  # No genera consultas adicionales

# Con prefetch_related (para ManyToManyField o consultas "inversas") - 2 consultas
libros = Libro.objects.prefetch_related('categorias')
for libro in libros:
    for categoria in libro.categorias.all():  # No genera consultas adicionales
        print(categoria.nombre)

# Combinar ambos para optimizar múltiples tipos de relaciones
libros = Libro.objects.select_related('autor').prefetch_related('categorias')

# Uso de annotate para añadir conteo de ejemplares
libros_con_conteo = Libro.objects.annotate(
    num_ejemplares=Count('ejemplares'),
    ejemplares_disponibles=Count('ejemplares', filter=Q(ejemplares__estado='d'))
)

# Uso de only para seleccionar solo ciertos campos
autores_basico = Autor.objects.only('nombre', 'apellido')

# Uso de defer para excluir campos grandes
libros_sin_resumen = Libro.objects.defer('resumen')

"""  Ejemplo: Mostrar campos en múltiples registros """

# Seleccionar múltiples registros
libros = Libro.objects.all().select_related('autor').prefetch_related('categorias')

# Recorrer todos los libros
for i, libro in enumerate(libros, 1):
    print(f"\n--- LIBRO {i} ---")

    # Mostrar campos básicos
    print(f"Título: {libro.titulo}")
    print(f"Publicado: {libro.publicado}")

    # Mostrar relación ForeignKey (Autor)
    print(f"Autor: {libro.autor.nombre} {libro.autor.apellido}")

    # Mostrar relación ManyToMany (Categorías)
    categorias = libro.categorias.all()
    if categorias:
        print("Categorías:")
        for categoria in categorias:
            print(f"  - {categoria.nombre}")
    else:
        print("Sin categorías")

    # Alternativa usando introspección para mostrar todos los campos
    print("\nCAMPOS DETALLADOS:")
    for campo in libro._meta.fields:
        nombre_campo = campo.name
        valor = getattr(libro, nombre_campo)

        # Formatear según tipo de relación
        if campo.is_relation and valor:
            print(f"{nombre_campo}: {valor} (ID: {valor.id})")
        else:
            print(f"{nombre_campo}: {valor}")

""" Consultas Complejas """

# Subconsultas con Subquery y OuterRef

from django.db.models import Subquery, OuterRef, Count

# Obtener el último libro de cada autor
ultimo_libro = Libro.objects.filter(
    autor=OuterRef('pk')
).order_by('-publicado').values('titulo')[:1]
autores = Autor.objects.annotate(
    ultimo_libro=Subquery(ultimo_libro)
)

# Contar libros por categoría
categoria_count = Libro.objects.filter(
    categorias=OuterRef('pk')
).values('categorias').annotate(c=Count('*')).values('c')
categorias = Categoria.objects.annotate(
    num_libros=Subquery(categoria_count)
)

""" Consulta de Ventana (Window Functions) """

from django.db.models import Window, F
from django.db.models.functions import RowNumber, Rank, DenseRank

# Clasificar libros por fecha de publicación dentro de cada autor
libros = Libro.objects.annotate(
    rank=Window(
        expression=Rank(),
        partition_by=F('autor'),
        order_by=F('publicado').desc()
    )
)

# Obtener solo los libros más recientes de cada autor (rank=1)
libros_recientes = libros.filter(rank=1)

"""  Consultas Raw SQL """

# Consulta SQL Raw
autores = Autor.objects.raw('SELECT * FROM myapp_autor WHERE apellido LIKE %s', ['C%'])

# Con parámetros nominados
autores = Autor.objects.raw(
    'SELECT * FROM myapp_autor WHERE fecha_nacimiento > %(fecha)s',
    {'fecha': '1950-01-01'}
)

# Acceder a los resultados
for autor in autores:
    print(autor.nombre)

"""  Transacciones """

from django.db import transaction


# Usando decorator
@transaction.atomic
def transferir_libros(autor_origen, autor_destino):
    Libro.objects.filter(autor=autor_origen).update(autor=autor_destino)
    Autor.objects.filter(pk=autor_origen.pk).delete()


# Usando context manager
def procesar_importacion():
    with transaction.atomic():
        # Todas estas operaciones se ejecutan en una transacción
        autor = Autor.objects.create(nombre="Nuevo", apellido="Autor")
        Libro.objects.create(titulo="Nuevo Libro", autor=autor, publicado="2023-01-01")
        # Si ocurre una excepción, se hace rollback automáticamente


""" Gestión de Índices """


class Libro(models.Model):
    titulo = models.CharField(max_length=200, db_index=True)  # Índice simple
    isbn = models.CharField(max_length=13, unique=True)  # Índice único

    # ...

    class Meta:
        indexes = [
            models.Index(fields=['publicado']),  # Índice simple
            models.Index(fields=['autor', 'publicado']),  # Índice compuesto
            models.Index(fields=['-publicado']),  # Índice ordenado descendente
        ]


""" Managers Personalizados """


class LibroPublicadoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publicado__lte=timezone.now()) # type: ignore

    def recientes(self):
        return self.get_queryset().order_by('-publicado')[:10]


class Libro(models.Model):
    # ...
    objects = models.Manager()  # Manager predeterminado
    publicados = LibroPublicadoManager()  # Manager personalizado
