# Sistema Biblioteca 📚

Sistema de gestión de biblioteca digital desarrollado con Django. Permite consultar un catálogo de libros, ver disponibilidad de ejemplares y solicitar préstamos con generación de código de retiro.

## Tecnologías

- Django 5.2.1
- PostgreSQL
- Tailwind CSS (django-tailwind)
- Pillow (manejo de imágenes)

## Requisitos previos

- Python 3.11+
- PostgreSQL instalado y corriendo
- Node.js (para Tailwind)

## Instalación
1. Clona el repositorio:

git clone https://github.com/melanybermeo/SISTEMA_BIBLIOTECA.git

cd SISTEMA_BIBLIOTECA 

2. Crea y activa un entorno virtual:

python -m venv venv
venv\Scripts\activate


3. Instala las dependencias:

pip install -r requeriments.txt


4. Crea una base de datos en PostgreSQL llamada `Biblioteca` (usuario `postgres`).

5. Ajusta la contraseña de PostgreSQL en `sistema_biblioteca/settings.py` si es distinta a la tuya.

6. Aplica las migraciones:
   
python manage.py migrate


7. Carga los datos de ejemplo (libros, autores, géneros):

python manage.py loaddata datos_iniciales


8. Crea un superusuario para el panel de administración:
   
python manage.py createsuperuser


9. Levanta el servidor:

python manage.py runserver


10. Abre tu navegador en `http://127.0.0.1:8000/`

## Funcionalidades

- Catálogo de libros con búsqueda y filtros por género
- Detalle de cada libro con portada, resumen y disponibilidad
- Solicitud de préstamo con formulario (nombre y correo)
- Generación de código único de retiro por préstamo
- Panel de administración para gestionar libros, autores, géneros y ejemplares

## Autora

Melanie Bermeo