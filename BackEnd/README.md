# 💻 POO - Backend con FastAPI + MySQL + phpMyAdmin

Este proyecto proporciona una infraestructura completa para los trabajos prácticos de la asignatura **Programación Orientada a Objetos** (Universidad Blas Pascal).

Incluye una API REST en FastAPI con autenticación, una base de datos MySQL 8 y phpMyAdmin, todo mediante Docker Compose.

---

## 📦 Servicios incluidos

- **poo_mysql**: base de datos MySQL 8.0 (puerto 3306)
- **poo_phpmyadmin**: interfaz phpMyAdmin para gestión de la BD (puerto 8080)
- **poo_api**: backend en FastAPI (puerto 8000)

---

## 📁 Estructura del proyecto

```
poo-api-db/
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── init_db.py           # Carga inicial de usuarios
│   ├── database.py          # Configuración SQLAlchemy
│   ├── models/
│   │   └── usuarios.py      # Modelo Usuario
│   ├── routers/
│   │   └── auth.py          # Endpoint de login
│   └── security.py          # (si se implementa en el futuro)
├── .env                     # Configuración sensible (NO versionar)
├── Dockerfile               # Imagen de FastAPI
├── docker-compose.yml       # Orquestación de servicios
├── .gitignore
└── README.md
```

---

## ⚙️ Variables de entorno

Configurar en el archivo `.env`:

```dotenv
MYSQL_ROOT_PASSWORD=...
MYSQL_DATABASE=poo_db
MYSQL_USER=...
MYSQL_PASSWORD=...

DEFAULT_USER_PASSWORD=...

SECRET_KEY=...
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_ALGORITHM=HS256
MYSQL_HOST=poo_mysql
```

> ⚠️ Este archivo está listado en `.gitignore` y **no debe subirse al repositorio**.

---

## 👤 Usuarios iniciales

Al iniciar por primera vez, se crea automáticamente la tabla `usuarios` con registros de prueba. Todos ellos usan la contraseña especificada en `DEFAULT_USER_PASSWORD`.

El script `init_db.py` se ejecuta automáticamente desde `main.py` al levantar el contenedor.

---

## 🌐 Accesos

- **API FastAPI (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **phpMyAdmin**: [http://localhost:8080](http://localhost:8080)
- **Base de datos MySQL**: desde `localhost:3306`, usuario y clave según `.env`

---

## 🧪 Comandos útiles

```bash
# Construir y levantar los servicios
docker compose up --build -d

# Ver logs del backend
docker compose logs -f poo_api

# Detener los servicios
docker compose down

# Reiniciar el entorno
docker compose restart
```

---

## 🧱 Requisitos previos

- Docker y Docker Compose instalados
- Puertos 3306, 8000 y 8080 disponibles
- Archivo `.env` correctamente configurado (sin valores por defecto)

---

## 🎓 Uso académico

Este entorno sirve como base para prácticas de:

- Modelado de clases y relaciones
- Desarrollo de APIs RESTful
- Conexión y manejo de bases de datos relacionales
- Autenticación de usuarios (JWT básico)
- Uso de contenedores con Docker

---

## 📌 Notas técnicas

- Los datos de MySQL persisten en el volumen `mysql_data`
- FastAPI se inicia en `0.0.0.0:8000` para permitir acceso externo
- Los servicios están conectados por la red `app-network`

---

> 🏫 Proyecto educativo - Universidad Blas Pascal  
> Docente: Dr. Ing. César Osimani
