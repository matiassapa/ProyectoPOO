# Usa una imagen base con Python 3.8
FROM python:3.8

# Configura variables de entorno para evitar la creación de archivos .pyc y asegurar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/Argentina/Cordoba

# Instala paquetes del sistema necesarios
RUN apt-get update && apt-get install -y --no-install-recommends \
    mc \
    tcpdump \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Define el directorio de trabajo en el contenedor
WORKDIR /workdir

# Copia primero el archivo de dependencias para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias de Python globalmente dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY src /workdir

# Expone el puerto 8001
EXPOSE 8001

# Comando de inicio del contenedor usando `workdir` como directorio de trabajo
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8002"]

