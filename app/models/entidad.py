from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Entidad(Base):
    __tablename__ = 'entidades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    nit = Column(String)
    orden = Column(String)
    sector = Column(String)
    
    # Relación con datasets
    datasets = relationship("Dataset", back_populates="entidad", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Entidad(id={self.id}, nombre='{self.nombre}', nit='{self.nit}', orden='{self.orden}', sector='{self.sector}')>"