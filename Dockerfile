# Utiliza la imagen base de Python 3.10
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instala el cliente de MariaDB
RUN apt-get update && apt-get install -y mariadb-client

# Copia el código fuente al contenedor
COPY  . .

# Expone el puerto 8000 (o cualquier otro puerto que uses en tu aplicación)
EXPOSE 8000

# Comando para ejecutar tu aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]