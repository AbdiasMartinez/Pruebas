import os
from sqlalchemy import create_engine
from app.config.config import DB_NAME
from app.models.entidad import Base as EntidadBase
from app.models.dataset import Base as DatasetBase

# Asegurarse de que existe el directorio para la base de datos
os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

# Crear el motor de base de datos y las tablas
engine = create_engine(f"sqlite:///{DB_NAME}")
EntidadBase.metadata.create_all(engine)
DatasetBase.metadata.create_all(engine)

print("Base de datos inicializada correctamente.")