# Changelog

Todos los cambios importantes del proyecto **Sistema Biblioteca** se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [1.0.0] - 2026-10-06

### Agregado
- Pipeline de integración continua con GitHub Actions (`.github/workflows/ci.yml`) que se ejecuta en cada push y pull request.
- Verificación automática de sintaxis del código Python.
- Revisión automática de configuración de Django (`manage.py check`).
- Ejecución automática de migraciones sobre un servicio PostgreSQL 16 temporal.
- Ejecución de pruebas automatizadas y generación de reporte (`reporte-ci`) como artefacto.
- Archivo `CHANGELOG.md` para el registro de versiones.

### Corregido
- Se agregó la dependencia `psycopg2-binary==2.9.10` en `requeriments.txt`. Su ausencia provocaba el error `Error loading psycopg2 or psycopg module` al ejecutar el proyecto fuera del equipo de desarrollo.

### Funcionalidades existentes incluidas en esta versión
- Gestión del catálogo de libros (modelo `Libro` con imagen de portada).
- Registro de préstamos con código único UUID (modelo `Prestamo`).
- Interfaz web con Django y Tailwind CSS.
- Base de datos PostgreSQL.