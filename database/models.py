from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    fecha_ingreso = Column(Date, default=func.now())
    puntos = Column(Integer, default=0)
    nivel = Column(Integer, default=1)
    renovacion_automatica = Column(Boolean, default=False)
    meses_consecutivos = Column(Integer, default=0)
    logros = relationship("Logro", back_populates="usuario")
    interacciones = relationship("Interaccion", back_populates="usuario")

class Logro(Base):
    __tablename__ = "logros"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.user_id"))
    nombre_logro = Column(String)
    fecha_obtencion = Column(Date, default=func.now())
    usuario = relationship("Usuario", back_populates="logros")

class Interaccion(Base):
    __tablename__ = "interacciones"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.user_id"))
    tipo_interaccion = Column(String)
    fecha = Column(DateTime, default=func.now())
    puntos_obtenidos = Column(Integer)
    usuario = relationship("Usuario", back_populates="interacciones")
  
