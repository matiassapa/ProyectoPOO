import os
import secrets  # Para comparar contraseñas de forma segura
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBearer, HTTPBasicCredentials, HTTPAuthorizationCredentials
from routes.login import login_router
from routes.check import check_router
from routes.users import users_router


from dotenv import load_dotenv


# Cargar variables de entorno
load_dotenv()

# Definir seguridad con `Bearer API Key`
# security = HTTPBearer()

security = HTTPBasic()

api = FastAPI(title="Córdoba sin Barreras API", version="1.0")


# Configurar CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://ec2-3-87-47-158.compute-1.amazonaws.com:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Solo estos métodos
    allow_headers=["Authorization", "Content-Type"],  # Solo los headers necesarios
)
 

# Rutas de la aplicación
api.include_router(login_router, prefix="/auth", tags=["Auth"])
api.include_router(check_router, prefix="/check", tags=["Checks"])
api.include_router(users_router, prefix="/users", tags=["Users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:api", host="0.0.0.0", port=8002, reload=True)

