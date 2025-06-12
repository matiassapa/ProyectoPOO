from sqlalchemy import Column, Integer, Text, DateTime
from database import Base  # ✅ correcto si estás dentro de `app/`

class Historial(Base):
    __tablename__ = "historial"

    id = Column(Integer, primary_key=True, index=True)
    pedido = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=False)
    fecha = Column(DateTime, nullable=False)
