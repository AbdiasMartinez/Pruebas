from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import DB_NAME
from app.models.entidad import Entidad, Base

engine = create_engine(f"sqlite:///{DB_NAME}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insertar_entidad(data):
    """
    Inserta una nueva entidad en la base de datos
    
    Args:
        data (dict): Datos de la entidad a insertar
    
    Returns:
        Entidad: La entidad creada o None si ya existe
    """
    with Session() as session:
        # Verificar si la entidad ya existe por nombre
        existe = session.query(Entidad).filter_by(nombre=data["nombre"]).first()
        if existe:
            return None
            
        entidad = Entidad(**data)
        session.add(entidad)
        session.commit()
        return entidad

def obtener_todas_entidades():
    """
    Obtiene todas las entidades de la base de datos
    
    Returns:
        list: Lista de entidades
    """
    with Session() as session:
        return session.query(Entidad).all()

def buscar_por_id(entidad_id):
    """
    Busca una entidad por su ID
    
    Args:
        entidad_id (int): ID de la entidad a buscar
    
    Returns:
        Entidad: La entidad encontrada o None
    """
    with Session() as session:
        return session.query(Entidad).filter_by(id=entidad_id).first()

def buscar_por_nombre(nombre):
    """
    Busca una entidad por su nombre
    
    Args:
        nombre (str): Nombre de la entidad a buscar
    
    Returns:
        Entidad: La entidad encontrada o None
    """
    with Session() as session:
        return session.query(Entidad).filter_by(nombre=nombre).first()

def actualizar_entidad(entidad_id, nuevos_datos):
    """
    Actualiza los datos de una entidad
    
    Args:
        entidad_id (int): ID de la entidad a actualizar
        nuevos_datos (dict): Nuevos datos para la entidad
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    with Session() as session:
        entidad = session.query(Entidad).filter_by(id=entidad_id).first()
        if entidad:
            for key, value in nuevos_datos.items():
                setattr(entidad, key, value)
            session.commit()
            return True
        return False

def eliminar_entidad(entidad_id):
    """
    Elimina una entidad de la base de datos
    
    Args:
        entidad_id (int): ID de la entidad a eliminar
    
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario
    """
    with Session() as session:
        entidad = session.query(Entidad).filter_by(id=entidad_id).first()
        if entidad:
            session.delete(entidad)
            session.commit()
            return True
        return False