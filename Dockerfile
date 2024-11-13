FROM alpine:3.20.3

# Instala las dependencias necesarias, incluyendo mysql-dev para la conexión a MySQL
RUN apk add --no-cache python3-dev py3-pip mysql-client mysql-dev \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip


WORKDIR /back-automationSA

COPY . /back-automationSA/

# Instalar requirements directamente usando el Python del entorno virtual
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Define el comando por defecto para ejecutar tu aplicación
CMD ["/opt/venv/bin/python", "run.py"]
