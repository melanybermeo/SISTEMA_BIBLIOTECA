# catalogo/views.py
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from .models import Libro, Autor, EjemplarLibro, Genero, Prestamo
from .forms import PrestamoForm


def index(request):
    """Vista para la página de inicio del sitio."""
    # Generar contadores para algunos de los objetos principales
    num_libros = Libro.objects.count()
    num_ejemplares = EjemplarLibro.objects.count()
    num_ejemplares_disponibles = EjemplarLibro.objects.filter(estado='d').count()
    num_autores = Autor.objects.count()

    # Libros que contienen 'novela' en el título
    num_libros_novela = Libro.objects.filter(titulo__icontains='novela').count()

    context = {
        'num_libros': num_libros,
        'num_ejemplares': num_ejemplares,
        'num_ejemplares_disponibles': num_ejemplares_disponibles,
        'num_autores': num_autores,
        'num_libros_novela': num_libros_novela,
    }

    return render(request, 'index.html', context=context)


class LibroListView(generic.ListView):
    model = Libro
    paginate_by = 10

    def get_queryset(self):
        # Iniciar con el queryset base
        queryset = Libro.objects.select_related('autor')

        # Filtrar por términos de búsqueda si hay alguno
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(autor__nombre__icontains=query) |
                Q(autor__apellido__icontains=query)
            )

        # Filtrar por géneros si hay alguno seleccionado
        genero_ids = self.request.GET.getlist('genero')
        if genero_ids:
            queryset = queryset.filter(genero__id__in=genero_ids).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Agregar estadísticas de libros al contexto
        context['generos_populares'] = Genero.objects.annotate(
            num_libros=Count('libro')
        ).order_by('-num_libros')[:5]

        # Preservar todos los parámetros GET para la paginación
        if self.request.GET:
            q_dict = self.request.GET.copy()
            if 'page' in q_dict:
                del q_dict['page']
            context['current_filters'] = q_dict.urlencode()

        return context


class LibroDetailView(generic.DetailView):
    model = Libro

    def get_queryset(self):
        # Optimizar consulta cargando relacionados
        return Libro.objects.select_related('autor').prefetch_related('genero', 'ejemplares')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Añadir información de disponibilidad de ejemplares
        libro = self.get_object()
        context['ejemplares_disponibles'] = libro.ejemplares.filter(estado='d').count()

        # Libros relacionados (mismo autor o géneros)
        context['libros_relacionados'] = Libro.objects.filter(
            Q(autor=libro.autor) | Q(genero__in=libro.genero.all())
        ).exclude(id=libro.id).distinct()[:5]

        return context
def solicitar_prestamo(request, pk):
    """Vista que muestra el formulario y procesa la solicitud de préstamo."""
    libro = get_object_or_404(Libro, pk=pk)
    ejemplar = libro.ejemplares.filter(estado='d').first()

    if not ejemplar:
        # No hay ejemplares disponibles, regresamos al detalle del libro
        return redirect('libro-detail', pk=libro.pk)

    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = Prestamo.objects.create(
                ejemplar=ejemplar,
                nombre_solicitante=form.cleaned_data['nombre_solicitante'],
                correo_solicitante=form.cleaned_data['correo_solicitante'],
            )
            # Marcar el ejemplar como prestado
            ejemplar.estado = 'p'
            ejemplar.save()

            return redirect('prestamo-confirmacion', codigo=prestamo.codigo)
    else:
        form = PrestamoForm()

    context = {
        'libro': libro,
        'form': form,
    }
    return render(request, 'catalogo/solicitar_prestamo.html', context)


def prestamo_confirmacion(request, codigo):
    """Vista tipo 'factura' que confirma la solicitud de préstamo."""
    prestamo = get_object_or_404(Prestamo, codigo=codigo)
    context = {
        'prestamo': prestamo,
    }
    return render(request, 'catalogo/prestamo_confirmacion.html', context)