from app.dall import entidad_dao

def crear_entidad():
    data = {
        "nombre": input("Nombre: "),
        "nit": input("NIT: "),
        "orden": input("Orden: "),
        "sector": input("Sector: ")
    }
    entidad_dao.insertar_entidad(data)
    print("Entidad creada con éxito.")

def listar_entidades():
    entidades = entidad_dao.obtener_todas_entidades()
    for e in entidades:
        print(e)

def buscar_entidad():
    id_busqueda = int(input("ID de la entidad: "))
    entidad = entidad_dao.buscar_por_id(id_busqueda)
    if entidad:
        print(entidad)
    else:
        print("Entidad no encontrada.")

def editar_entidad():
    id_editar = int(input("ID de la entidad a editar: "))
    entidad = entidad_dao.buscar_por_id(id_editar)
    if not entidad:
        print("Entidad no encontrada.")
        return

    nuevos_datos = {
        "nombre": input(f"Nuevo nombre ({entidad.nombre}): ") or entidad.nombre,
        "nit": input(f"Nuevo NIT ({entidad.nit}): ") or entidad.nit,
        "orden": input(f"Nuevo orden ({entidad.orden}): ") or entidad.orden,
        "sector": input(f"Nuevo sector ({entidad.sector}): ") or entidad.sector
    }

    entidad_dao.actualizar_entidad(id_editar, nuevos_datos)
    print("Entidad actualizada.")

def eliminar_entidad():
    id_eliminar = int(input("ID de la entidad a eliminar: "))
    entidad_dao.eliminar_entidad(id_eliminar)
    print("Entidad eliminada.")
