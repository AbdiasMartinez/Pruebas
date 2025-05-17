import requests
from app.config import API_URL
from app.dall import entidad_dao

def cargar_datos_api():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            entidad_dao.insertar_entidad({
                "nombre": item.get("nombre_entidad", "Desconocido"),
                "nit": item.get("nit_entidad", "Sin NIT"),
                "orden": item.get("orden", "No especificado"),
                "sector": item.get("sector_administrativo", "No especificado")
            })

