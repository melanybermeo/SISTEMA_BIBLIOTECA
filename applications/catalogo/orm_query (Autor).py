from applications.catalogo.models import Autor

""" Create (Crear) """
# Metodo 1: Crear y guardar
autor = Autor(nombre="Gabriel", apellido="García Márquez")
autor.save()

# Método 2: Crear con create()
autor = Autor.objects.create(nombre="Gabriel", apellido="García Márquez")

""" Read (Leer) """

# Obtener todos los registros
autores = Autor.objects.all()

# Obtener un registro por su clave primaria
autor = Autor.objects.get(pk=1)

# Obtener el primer registro que cumpla con ciertos criterios
autor = Autor.objects.filter(apellido="García Márquez").first()

""" Update (Actualizar) """

# Método 1: Obtener, modificar y guardar
autor = Autor.objects.get(pk=1)
autor.nombre = "Gabriel José"
autor.save()

# Método 2: Actualizar directamente
Autor.objects.filter(pk=1).update(nombre="Gabriel José")

""" Delete (Eliminar) """

# Método 1: Obtener y eliminar
autor = Autor.objects.get(pk=1)
autor.delete()

# Método 2: Eliminar directamente
Autor.objects.filter(apellido="García Márquez").delete()

"""  Filtros Simples """

# Filtrar por condición exacta
autores = Autor.objects.filter(apellido="García Márquez")

# Filtrar por múltiples condiciones (AND)
autores = Autor.objects.filter(apellido="García Márquez", nombre="Gabriel")

# Excluir registros
autores = Autor.objects.exclude(apellido="García Márquez")

# Limitar resultados
autores = Autor.objects.all()[:5]  # Primeros 5 resultados
autores = Autor.objects.all()[5:10]  # Resultados del 6 al 10

""" Ordenamiento """

# Ordenar por un campo (ascendente)
autores = Autor.objects.order_by('apellido')

# Ordenar por un campo (descendente)
autores = Autor.objects.order_by('-fecha_nacimiento')

# Ordenar por múltiples campos
autores = Autor.objects.order_by('apellido', 'nombre')

""" Técnicas de Introspección de Modelos """


def inspeccionar_registro_individual(pk):
    """
    Función para demostrar diferentes métodos de introspección
    para examinar todos los campos de un registro individual.
    """

    # 1. Seleccionar un registro específico
    autor = Autor.objects.get(pk=pk)  # Cambia el pk según sea necesario
    print(f"\n{'=' * 50}")
    print(f"DETALLES DEL AUTOR: {autor}")
    print(f"{'=' * 50}")

    # 2. Método 1: Usando __dict__ para obtener los campos como un diccionario
    # Este método es simple pero no muestra información sobre relaciones o metadatos
    print("\nMÉTODO 1: Usando __dict__")
    print(f"{'-' * 40}")
    for campo, valor in autor.__dict__.items():
        if not campo.startswith('_'):  # Excluimos campos internos
            print(f"{campo}: {valor}")

    # 3. Método 2: Usando introspección del modelo a través de _meta
    # Este método es más completo y ofrece información sobre el tipo de campo
    print("\nMÉTODO 2: Usando _meta.fields (introspección)")
    print(f"{'-' * 40}")
    for campo in autor._meta.fields:
        nombre_campo = campo.name
        valor = getattr(autor, nombre_campo)
        tipo_campo = campo.get_internal_type()

        # Formatear la salida según el tipo de campo
        if tipo_campo == 'ForeignKey' or tipo_campo == 'OneToOneField':
            if valor:
                objeto_relacionado = valor
                print(f"{nombre_campo} ({tipo_campo}): {objeto_relacionado} [ID: {objeto_relacionado.pk}]")
            else:
                print(f"{nombre_campo} ({tipo_campo}): None")
        elif tipo_campo == 'DateField' or tipo_campo == 'DateTimeField':
            print(f"{nombre_campo} ({tipo_campo}): {valor}")
        else:
            print(f"{nombre_campo} ({tipo_campo}): {valor}")

    # 4. Examinar campos ManyToMany, que requieren manejo especial

    print("\nCAMPOS MANY-TO-MANY:")
    print(f"{'-' * 40}")

    for campo in autor._meta.many_to_many:
        nombre_campo = campo.name

        queryset_relacionado = getattr(autor, nombre_campo).all()

        print(f"{nombre_campo} (ManyToManyField):")
        if queryset_relacionado.exists():
            for obj in queryset_relacionado:
                print(f"  - {obj} [ID: {obj.id}]")
        else:
            print("  - No hay objetos relacionados")

    # 5. Información sobre el modelo
    print("\nMETADATOS DEL MODELO:")
    print(f"{'-' * 40}")
    print(f"Nombre del modelo: {autor._meta.model.__name__}")
    print(f"Tabla en BD: {autor._meta.db_table}")
    print(f"Verbose name: {autor._meta.verbose_name}")
    print(f"Verbose name plural: {autor._meta.verbose_name_plural}")
    print(f"Campos: {[campo.name for campo in autor._meta.fields]}")
    print(f"Unique together: {autor._meta.unique_together}")

    # 6. Revisar permisos
    print("\nPERMISOS ASOCIADOS:")
    print(f"{'-' * 40}")
    for permiso in autor._meta.permissions:
        print(f"- {permiso}")


# Llamado de la función para un ejemplo práctico
# inspeccionar_registro_individual(1)  # Cambia el ID según sea necesario

