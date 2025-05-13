import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos desde las variables de entorno
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")  # Valor por defecto: localhost
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")  # Valor por defecto: 3306
DATABASE_NAME = os.getenv("DATABASE_NAME")

# URI de conexión para SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependencia para la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()