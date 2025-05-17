import requests
from app.config.config import API_URL
from app.dall import entidad_dao, dataset_dao
from app.services.api_service import APIClient

def cargar_datos_api():
    """
    Carga datos desde la API y los guarda en la base de datos local
    
    Returns:
        dict: Estadísticas de importación
    """
    client = APIClient()
    
    # Cargar entidades
    print("Cargando entidades desde la API...")
    entidades_api = client.obtener_entidades()
    
    count_entidades = 0
    for entidad_data in entidades_api:
        resultado = entidad_dao.insertar_entidad(entidad_data)
        if resultado:
            count_entidades += 1
    
    print(f"Se importaron {count_entidades} entidades nuevas.")
    
    # Cargar datasets
    print("Cargando datasets desde la API...")
    datasets_api = client.obtener_datasets()
    
    count_datasets = 0
    for dataset_data in datasets_api:
        # Buscar la entidad correspondiente
        entidad_nombre = dataset_data.pop("entidad_nombre")
        entidad = entidad_dao.buscar_por_nombre(entidad_nombre)
        
        if entidad:
            dataset_data["entidad_id"] = entidad.id
            resultado = dataset_dao.insertar_dataset(dataset_data)
            if resultado:
                count_datasets += 1
    
    print(f"Se importaron {count_datasets} datasets nuevos.")
    
    # Evaluar cumplimiento después de importar
    print("Evaluando cumplimiento...")
    dataset_dao.evaluar_cumplimiento()
    
    return {
        "entidades": count_entidades,
        "datasets": count_datasets
    }

def generar_informe_cumplimiento():
    """
    Genera un informe de cumplimiento por sector
    
    Returns:
        dict: Estadísticas de cumplimiento por sector
    """
    entidades = entidad_dao.obtener_todas_entidades()
    
    stats_sectores = {}
    
    for entidad in entidades:
        sector = entidad.sector
        
        if sector not in stats_sectores:
            stats_sectores[sector] = {
                "total": 0,
                "cumplen": 0,
                "no_cumplen": 0,
                "parcial": 0
            }
        
        # Obtener datasets de la entidad
        datasets = dataset_dao.buscar_datasets_por_entidad(entidad.id)
        
        for ds in datasets:
            stats_sectores[sector]["total"] += 1
            
            if ds.estado_cumplimiento == "Cumple":
                stats_sectores[sector]["cumplen"] += 1
            elif ds.estado_cumplimiento == "Parcial":
                stats_sectores[sector]["parcial"] += 1
            else:
                stats_sectores[sector]["no_cumplen"] += 1
    
    return stats_sectores