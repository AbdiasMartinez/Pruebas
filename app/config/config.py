import os

# URL de la API de datos abiertos de Colombia
API_URL = "https://www.datos.gov.co/resource/8mn3-4dn4.json"

# Configuración de la base de datos
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
DB_NAME = os.path.join(DB_PATH, "database.db")

# Configuración de frecuencias de actualización (en días)
FRECUENCIAS = {
    "Mensual": 31,
    "Trimestral": 93,
    "Semestral": 183,
    "Anual": 366
}

# Configuración de la aplicación
APP_NAME = "Sistema de Análisis de Datos Abiertos en Colombia"
APP_VERSION = "1.0.0"