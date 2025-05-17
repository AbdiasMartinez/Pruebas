import requests
from app.config.config import API_URL

class APIClient:
    def obtener_datos(self, limite=100):
        """
        Obtiene datos de la API de datos abiertos de Colombia
        
        Args:
            limite (int): Número máximo de registros a obtener
            
        Returns:
            dict: Datos obtenidos de la API en formato JSON
        """
        response = requests.get(f"{API_URL}?$limit={limite}")
        return response.json()

    def obtener_entidades(self, limite=100):
        """
        Extrae y formatea los datos de entidades desde la API
        
        Returns:
            list: Lista de diccionarios con datos de entidades
        """
        datos = self.obtener_datos(limite)
        entidades = []
        
        for item in datos:
            entidad = {
                "nombre": item.get("nombre_entidad", "Desconocido"),
                "nit": item.get("nit_entidad", "Sin NIT"),
                "orden": item.get("orden", "No especificado"),
                "sector": item.get("sector_administrativo", "No especificado")
            }
            
            # Verificamos si la entidad ya existe en nuestra lista
            if entidad not in entidades:
                entidades.append(entidad)
                
        return entidades
    
    def obtener_datasets(self, limite=100):
        """
        Extrae y formatea los datos de conjuntos de datos desde la API
        
        Returns:
            list: Lista de diccionarios con datos de datasets
        """
        datos = self.obtener_datos(limite)
        datasets = []
        
        for item in datos:
            dataset = {
                "nombre": item.get("nombre_conjunto_de_datos", "Sin nombre"),
                "descripcion": item.get("descripcion_conjunto_de_datos", "Sin descripción"),
                "frecuencia_actualizacion": item.get("frecuencia_de_actualizacion", "No especificada"),
                "fecha_ultima_actualizacion": item.get("fecha_ultima_de_actualizacion"),
                "responsable_publicacion": item.get("responsable_de_la_publicacion", "No especificado"),
                "url_acceso": item.get("url_de_acceso", ""),
                "entidad_nombre": item.get("nombre_entidad", "Desconocido")
            }
            datasets.append(dataset)
                
        return datasets