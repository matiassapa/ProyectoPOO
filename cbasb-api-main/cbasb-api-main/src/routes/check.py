from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.config import get_db, SessionLocal
import time
from models.users import User
from security.security import verify_api_key


check_router = APIRouter()


@check_router.get("/db_check", dependencies=[ Depends( verify_api_key ) ] )
async def db_check():
    """
    Verifica si se puede conectar a la base de datos.
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )
    finally:
        db.close()

