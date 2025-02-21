from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
from database import engine

# Crear la base de modelos de SQLAlchemy
Base = declarative_base()

# Modelo para la tabla "concerts"
class Concert(Base):
    __tablename__ = "concerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_name = Column(String(255), nullable=False)  # Cambio de eventName a event_name
    img = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    dateTime = Column(DateTime, nullable=False)
    place = Column(String(255), nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)
    stock = Column(Integer, nullable=False, server_default=text("6"))

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)