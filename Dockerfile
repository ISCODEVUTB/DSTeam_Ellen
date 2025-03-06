
FROM python:3.9-slim

WORKDIR /app


COPY main.py /app/main.py

# Comando que se ejecutará al iniciar el contenedor
CMD ["python", "main.py"]
