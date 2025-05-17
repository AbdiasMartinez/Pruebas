from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config.config import DB_NAME
from app.models.dataset import Dataset, Base
from app.dall.entidad_dao import buscar_por_nombre

engine = create_engine(f"sqlite:///{DB_NAME}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insertar_dataset(data):
    """
    Inserta un nuevo dataset en la base de datos
    
    Args:
        data (dict): Datos del dataset a insertar
    
    Returns:
        Dataset: El objeto dataset creado
    """
    with Session() as session:
        # Convertir la fecha si existe
        if "fecha_ultima_actualizacion" in data and data["fecha_ultima_actualizacion"]:
            try:
                data["fecha_ultima_actualizacion"] = datetime.strptime(
                    data["fecha_ultima_actualizacion"], "%Y-%m-%d"
                ).date()
            except ValueError:
                data["fecha_ultima_actualizacion"] = None
                
        # Crear y guardar el dataset
        dataset = Dataset(**data)
        session.add(dataset)
        session.commit()
        return dataset

def obtener_todos_datasets():
    """
    Obtiene todos los datasets de la base de datos
    
    Returns:
        list: Lista de datasets
    """
    with Session() as session:
        return session.query(Dataset).all()

def buscar_dataset_por_id(dataset_id):
    """
    Busca un dataset por su ID
    
    Args:
        dataset_id (int): ID del dataset a buscar
    
    Returns:
        Dataset: El dataset encontrado o None
    """
    with Session() as session:
        return session.query(Dataset).filter_by(id=dataset_id).first()

def buscar_datasets_por_entidad(entidad_id):
    """
    Busca datasets por ID de entidad
    
    Args:
        entidad_id (int): ID de la entidad
    
    Returns:
        list: Lista de datasets asociados a la entidad
    """
    with Session() as session:
        return session.query(Dataset).filter_by(entidad_id=entidad_id).all()

def actualizar_dataset(dataset_id, nuevos_datos):
    """
    Actualiza los datos de un dataset
    
    Args:
        dataset_id (int): ID del dataset a actualizar
        nuevos_datos (dict): Nuevos datos para el dataset
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    with Session() as session:
        dataset = session.query(Dataset).filter_by(id=dataset_id).first()
        if dataset:
            # Convertir la fecha si existe
            if "fecha_ultima_actualizacion" in nuevos_datos and nuevos_datos["fecha_ultima_actualizacion"]:
                try:
                    nuevos_datos["fecha_ultima_actualizacion"] = datetime.strptime(
                        nuevos_datos["fecha_ultima_actualizacion"], "%Y-%m-%d"
                    ).date()
                except ValueError:
                    nuevos_datos["fecha_ultima_actualizacion"] = None
                
            for key, value in nuevos_datos.items():
                setattr(dataset, key, value)
            session.commit()
            return True
        return False

def eliminar_dataset(dataset_id):
    """
    Elimina un dataset de la base de datos
    
    Args:
        dataset_id (int): ID del dataset a eliminar
    
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario
    """
    with Session() as session:
        dataset = session.query(Dataset).filter_by(id=dataset_id).first()
        if dataset:
            session.delete(dataset)
            session.commit()
            return True
        return False

def evaluar_cumplimiento():
    """
    Evalúa el estado de cumplimiento de todos los datasets basado en su frecuencia
    de actualización y fecha de última actualización
    
    Returns:
        dict: Estadísticas de cumplimiento
    """
    with Session() as session:
        datasets = session.query(Dataset).all()
        hoy = datetime.now().date()
        
        stats = {
            "total": len(datasets),
            "cumplen": 0,
            "no_cumplen": 0,
            "parcial": 0
        }
        
        for ds in datasets:
            if not ds.fecha_ultima_actualizacion:
                ds.estado_cumplimiento = "No Cumple"
                stats["no_cumplen"] += 1
                continue
                
            dias_desde_actualizacion = (hoy - ds.fecha_ultima_actualizacion).days
            
            if ds.frecuencia_actualizacion == "Mensual" and dias_desde_actualizacion <= 31:
                ds.estado_cumplimiento = "Cumple"
                stats["cumplen"] += 1
            elif ds.frecuencia_actualizacion == "Trimestral" and dias_desde_actualizacion <= 93:
                ds.estado_cumplimiento = "Cumple"
                stats["cumplen"] += 1
            elif ds.frecuencia_actualizacion == "Semestral" and dias_desde_actualizacion <= 183:
                ds.estado_cumplimiento = "Cumple"
                stats["cumplen"] += 1
            elif ds.frecuencia_actualizacion == "Anual" and dias_desde_actualizacion <= 366:
                ds.estado_cumplimiento = "Cumple"
                stats["cumplen"] += 1
            elif dias_desde_actualizacion <= 366:
                ds.estado_cumplimiento = "Parcial"
                stats["parcial"] += 1
            else:
                ds.estado_cumplimiento = "No Cumple"
                stats["no_cumplen"] += 1
                
        session.commit()
        return stats