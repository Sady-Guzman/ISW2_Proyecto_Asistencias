# Usa imagen python
FROM python:3.9-slim


# Define variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL=postgresql://postgres:domino@some-postgres:5432/postgres

# Define directorio de trabajdo para el container
WORKDIR /app

# Copia contenido de las dependencias de requirements.txt
COPY requirements.txt ./


# Installa los requerimientos especificados
RUN pip install --no-cache-dir -r requirements.txt

# Instala dependencias para PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev


# Crea el directorio de carga y le asigna permisos 755
RUN mkdir -p /app/temp && chmod -R 755 /app/temp

# Copia los contenidos de la apicacion al container
COPY . .


# Expone puerto 5000
EXPOSE 10000

# Corre comandos para iniciar
CMD ["flask", "run", "--host=0.0.0.0"]
