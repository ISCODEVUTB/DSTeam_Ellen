# 1) Imagen base
FROM python:3.9-slim

# 2) Creamos una carpeta de trabajo
WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Creamos un usuario "myuser" sin privilegio
RUN useradd -ms /bin/bash myuser


USER myuser


COPY . .


CMD ["python", "main.py"]
