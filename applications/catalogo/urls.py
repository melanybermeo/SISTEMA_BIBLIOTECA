from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.LibroListView.as_view(), name='libros'),
    path('libro/<int:pk>/', views.LibroDetailView.as_view(), name='libro-detail'),
    path('libro/<int:pk>/prestamo/', views.solicitar_prestamo, name='solicitar-prestamo'),
    path('prestamo/<uuid:codigo>/confirmacion/', views.prestamo_confirmacion, name='prestamo-confirmacion'),
]