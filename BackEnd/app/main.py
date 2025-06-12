from fastapi import FastAPI
from routers import auth
from routers import analisis
import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

app = FastAPI()

# 🚨 Agrega esto antes de incluir los routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiá esto a ["http://localhost:3000"] si usás frontend en React por ejemplo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa DB y carga usuarios si no existen
init_db.init()
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TP4 - Planificador de Tareas",
        version="1.0.0",
        description="API para login, análisis y descarga de PDF.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(analisis.router, tags=["Análisis"])
