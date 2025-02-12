from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Obtiene la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Reemplaza "mysql://" por "mysql+mysqlconnector://" en la URL
DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+mysqlconnector://", 1)

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear la base declarativa
Base = declarative_base()

# Sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()