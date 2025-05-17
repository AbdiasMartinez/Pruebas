from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DB_NAME
from app.models.entidad import Entidad, Base

engine = create_engine(f"sqlite:///{DB_NAME}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insertar_entidad(data):
    with Session() as session:
        entidad = Entidad(**data)
        session.add(entidad)
        session.commit()

def obtener_todas_entidades():
    with Session() as session:
        return session.query(Entidad).all()

def buscar_por_id(entidad_id):
    with Session() as session:
        return session.query(Entidad).filter_by(id=entidad_id).first()

def actualizar_entidad(entidad_id, nuevos_datos):
    with Session() as session:
        entidad = session.query(Entidad).filter_by(id=entidad_id).first()
        if entidad:
            for key, value in nuevos_datos.items():
                setattr(entidad, key, value)
            session.commit()

def eliminar_entidad(entidad_id):
    with Session() as session:
        entidad = session.query(Entidad).filter_by(id=entidad_id).first()
        if entidad:
            session.delete(entidad)
            session.commit()
