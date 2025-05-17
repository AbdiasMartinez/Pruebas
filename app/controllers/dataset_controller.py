from app.dall import dataset_dao, entidad_dao
from datetime import datetime

def crear_dataset():
    """
    Crea un nuevo dataset con datos ingresados por el usuario
    """
    # Solicitar al usuario que ingrese la entidad
    print("\n--- ENTIDADES DISPONIBLES ---")
    entidades = entidad_dao.obtener_todas_entidades()
    for e in entidades:
        print(f"{e.id}: {e.nombre}")
    
    entidad_id = input("\nID de la entidad asociada: ")
    try:
        entidad_id = int(entidad_id)
        entidad = entidad_dao.buscar_por_id(entidad_id)
        if not entidad:
            print("Entidad no encontrada.")
            return
    except ValueError:
        print("ID inválido.")
        return
    
    # Solicitar datos del dataset
    data = {
        "entidad_id": entidad_id,
        "nombre": input("Nombre del conjunto de datos: "),
        "descripcion": input("Descripción: "),
        "frecuencia_actualizacion": input("Frecuencia de actualización (Mensual/Trimestral/Semestral/Anual): "),
        "fecha_ultima_actualizacion": input("Fecha última actualización (YYYY-MM-DD): "),
        "responsable_publicacion": input("Responsable de publicación: "),
        "url_acceso": input("URL de acceso: ")
    }
    
    # Validar fechas
    try:
        if data["fecha_ultima_actualizacion"]:
            datetime.strptime(data["fecha_ultima_actualizacion"], "%Y-%m-%d")
    except ValueError:
        print("Formato de fecha incorrecto. Use YYYY-MM-DD.")
        return
        
    dataset_dao.insertar_dataset(data)
    print("Dataset creado con éxito.")

def listar_datasets():
    """
    Lista todos los datasets almacenados
    """
    datasets = dataset_dao.obtener_todos_datasets()
    
    if not datasets:
        print("No hay datasets registrados.")
        return
        
    print("\n--- LISTADO DE DATASETS ---")
    for ds in datasets:
        entidad = entidad_dao.buscar_por_id(ds.entidad_id)
        entidad_nombre = entidad.nombre if entidad else "Entidad desconocida"
        
        print(f"ID: {ds.id}")
        print(f"Entidad: {entidad_nombre}")
        print(f"Nombre: {ds.nombre}")
        print(f"Frecuencia: {ds.frecuencia_actualizacion}")
        print(f"Última actualización: {ds.fecha_ultima_actualizacion}")
        print(f"Estado: {ds.estado_cumplimiento or 'No evaluado'}")
        print("-" * 40)

def buscar_dataset():
    """
    Busca un dataset por su ID
    """
    id_busqueda = input("ID del dataset: ")
    try:
        id_busqueda = int(id_busqueda)
    except ValueError:
        print("ID inválido.")
        return
        
    dataset = dataset_dao.buscar_dataset_por_id(id_busqueda)
    
    if not dataset:
        print("Dataset no encontrado.")
        return
        
    entidad = entidad_dao.buscar_por_id(dataset.entidad_id)
    entidad_nombre = entidad.nombre if entidad else "Entidad desconocida"
    
    print("\n--- DETALLES DEL DATASET ---")
    print(f"ID: {dataset.id}")
    print(f"Entidad: {entidad_nombre}")
    print(f"Nombre: {dataset.nombre}")
    print(f"Descripción: {dataset.descripcion}")
    print(f"Frecuencia: {dataset.frecuencia_actualizacion}")
    print(f"Última actualización: {dataset.fecha_ultima_actualizacion}")
    print(f"Responsable: {dataset.responsable_publicacion}")
    print(f"URL: {dataset.url_acceso}")
    print(f"Estado: {dataset.estado_cumplimiento or 'No evaluado'}")

def editar_dataset():
    """
    Edita un dataset existente
    """
    id_editar = input("ID del dataset a editar: ")
    try:
        id_editar = int(id_editar)
    except ValueError:
        print("ID inválido.")
        return
        
    dataset = dataset_dao.buscar_dataset_por_id(id_editar)
    
    if not dataset:
        print("Dataset no encontrado.")
        return
    
    entidad = entidad_dao.buscar_por_id(dataset.entidad_id)
    entidad_nombre = entidad.nombre if entidad else "Entidad desconocida"
    
    print(f"\nEditando dataset: {dataset.nombre} (Entidad: {entidad_nombre})")
    
    nuevos_datos = {
        "nombre": input(f"Nuevo nombre ({dataset.nombre}): ") or dataset.nombre,
        "descripcion": input(f"Nueva descripción ({dataset.descripcion}): ") or dataset.descripcion,
        "frecuencia_actualizacion": input(f"Nueva frecuencia ({dataset.frecuencia_actualizacion}): ") or dataset.frecuencia_actualizacion,
        "fecha_ultima_actualizacion": input(f"Nueva fecha última actualización ({dataset.fecha_ultima_actualizacion}): ") or (dataset.fecha_ultima_actualizacion.strftime("%Y-%m-%d") if dataset.fecha_ultima_actualizacion else ""),
        "responsable_publicacion": input(f"Nuevo responsable ({dataset.responsable_publicacion}): ") or dataset.responsable_publicacion,
        "url_acceso": input(f"Nueva URL ({dataset.url_acceso}): ") or dataset.url_acceso
    }

    # Validar fechas
    try:
        if nuevos_datos["fecha_ultima_actualizacion"]:
            datetime.strptime(nuevos_datos["fecha_ultima_actualizacion"], "%Y-%m-%d")
    except ValueError:
        print("Formato de fecha incorrecto. Use YYYY-MM-DD.")
        return
    
    resultado = dataset_dao.actualizar_dataset(id_editar, nuevos_datos)
    if resultado:
        print("Dataset actualizado con éxito.")
    else:
        print("Error al actualizar el dataset.")

def eliminar_dataset():
    """
    Elimina un dataset de la base de datos
    """
    id_eliminar = input("ID del dataset a eliminar: ")
    try:
        id_eliminar = int(id_eliminar)
    except ValueError:
        print("ID inválido.")
        return
        
    resultado = dataset_dao.eliminar_dataset(id_eliminar)
    if resultado:
        print("Dataset eliminado con éxito.")
    else:
        print("Dataset no encontrado o error al eliminar.")

def evaluar_cumplimiento_datasets():
    """
    Evalúa el estado de cumplimiento de todos los datasets
    """
    stats = dataset_dao.evaluar_cumplimiento()
    
    print("\n--- EVALUACIÓN DE CUMPLIMIENTO ---")
    print(f"Total de datasets: {stats['total']}")
    print(f"Cumplen: {stats['cumplen']} ({stats['cumplen']/stats['total']*100:.1f}% si hay datos)")
    print(f"Cumplen parcialmente: {stats['parcial']} ({stats['parcial']/stats['total']*100:.1f}% si hay datos)")
    print(f"No cumplen: {stats['no_cumplen']} ({stats['no_cumplen']/stats['total']*100:.1f}% si hay datos)")
    
    return stats

def listar_datasets_por_entidad():
    """
    Lista los datasets asociados a una entidad específica
    """
    print("\n--- ENTIDADES DISPONIBLES ---")
    entidades = entidad_dao.obtener_todas_entidades()
    for e in entidades:
        print(f"{e.id}: {e.nombre}")
    
    entidad_id = input("\nID de la entidad: ")
    try:
        entidad_id = int(entidad_id)
    except ValueError:
        print("ID inválido.")
        return
        
    entidad = entidad_dao.buscar_por_id(entidad_id)
    if not entidad:
        print("Entidad no encontrada.")
        return
        
    datasets = dataset_dao.buscar_datasets_por_entidad(entidad_id)
    
    if not datasets:
        print(f"No hay datasets registrados para la entidad '{entidad.nombre}'.")
        return
        
    print(f"\n--- DATASETS DE '{entidad.nombre}' ---")
    for ds in datasets:
        print(f"ID: {ds.id}")
        print(f"Nombre: {ds.nombre}")
        print(f"Frecuencia: {ds.frecuencia_actualizacion}")
        print(f"Última actualización: {ds.fecha_ultima_actualizacion}")
        print(f"Estado: {ds.estado_cumplimiento or 'No evaluado'}")
        print("-" * 40)