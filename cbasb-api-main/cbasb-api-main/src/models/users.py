from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = "user"

    login = Column(String(190), primary_key=True, nullable=False)  # login varchar(190)
    clave = Column(String(255), nullable=False)  # clave varchar(255)
    nombre = Column(String(64), nullable=False)  # nombre varchar(64)
    apellido = Column(String(64), nullable=True)  # apellido varchar(64)
    celular = Column(String(20), nullable=True)  # celular varchar(20)
    mail = Column(String(255), nullable=True)  # mail varchar(255)
    fecha_nacimiento = Column(Date, nullable=True)  # fecha_nacimiento date
    active = Column(String(1), nullable=True)  # active varchar(1)
    activation_code = Column(String(32), nullable=True)  # activation_code varchar(32)
    foto_perfil = Column(String(255), nullable=True)  # foto_perfil varchar(255)
    calle_y_nro = Column(String(50), nullable=True)  # calle_y_nro varchar(50)
    depto_etc = Column(String(50), nullable=True)  # depto_etc varchar(50)
    barrio = Column(String(50), nullable=True)  # barrio varchar(50)
    localidad = Column(String(50), nullable=True)  # localidad varchar(50)
    provincia = Column(String(50), nullable=True)  # provincia varchar(50)
    recuperacion_code = Column(String(32), nullable=True)  # recuperacion_code varchar(32)
    fecha_alta = Column(Date, nullable=True)  # fecha_alta date
    operativo = Column(String(1), nullable=True, default="Y")  # operativo varchar(1)
    role_id = Column(Integer, ForeignKey("role.role_id"), nullable=True)  

    role = relationship("Role", back_populates="user")  # Relación con Role


class Role(Base):
    __tablename__ = "role"
    
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=True)

    user = relationship("User", back_populates="role")  # Relación inversa con User
