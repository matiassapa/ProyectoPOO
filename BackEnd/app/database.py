import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"La variable de entorno {var_name} no está definida o está vacía.")
    return value

# 🚫 Sin valores por defecto: todas las variables deben estar en .env
MYSQL_USER = require_env("MYSQL_USER")
MYSQL_PASSWORD = require_env("MYSQL_PASSWORD")
MYSQL_DATABASE = require_env("MYSQL_DATABASE")
MYSQL_HOST = require_env("MYSQL_HOST")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
