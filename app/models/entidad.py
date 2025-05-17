from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Entidad(Base):
    __tablename__ = 'entidades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    nit = Column(String)
    orden = Column(String)
    sector = Column(String)

    def __repr__(self):
        return f"<Entidad(id={self.id}, nombre={self.nombre}, nit={self.nit}, orden={self.orden}, sector={self.sector})>"
