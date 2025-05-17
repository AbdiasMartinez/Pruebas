from app.controllers import entidad_controller, dataset_controller
from app.services.entidad_service import cargar_datos_api, generar_informe_cumplimiento

def mostrar_menu():
    """
    Muestra el menú principal de la aplicación
    """
    while True:
        print("\n=== SISTEMA DE ANÁLISIS DE DATOS ABIERTOS EN COLOMBIA ===")
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Cargar datos desde API")
        print("2. Gestión de Entidades")
        print("3. Gestión de Datasets")
        print("4. Evaluación de Cumplimiento")
        print("5. Informes")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            cargar_datos_api()
        elif opcion == "2":
            menu_entidades()
        elif opcion == "3":
            menu_datasets()
        elif opcion == "4":
            dataset_controller.evaluar_cumplimiento_datasets()
        elif opcion == "5":
            menu_informes()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def menu_entidades():
    """
    Muestra el submenú para gestión de entidades
    """
    while True:
        print("\n--- GESTIÓN DE ENTIDADES ---")
        print("1. Crear entidad")
        print("2. Listar entidades")
        print("3. Buscar entidad por ID")
        print("4. Editar entidad")
        print("5. Eliminar entidad")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            entidad_controller.crear_entidad()
        elif opcion == "2":
            entidad_controller.listar_entidades()
        elif opcion == "3":
            entidad_controller.buscar_entidad()
        elif opcion == "4":
            entidad_controller.editar_entidad()
        elif opcion == "5":
            entidad_controller.eliminar_entidad()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def menu_datasets():
    """
    Muestra el submenú para gestión de datasets
    """
    while True:
        print("\n--- GESTIÓN DE DATASETS ---")
        print("1. Crear dataset")
        print("2. Listar todos los datasets")
        print("3. Listar datasets por entidad")
        print("4. Buscar dataset por ID")
        print("5. Editar dataset")
        print("6. Eliminar dataset")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            dataset_controller.crear_dataset()
        elif opcion == "2":
            dataset_controller.listar_datasets()
        elif opcion == "3":
            dataset_controller.listar_datasets_por_entidad()
        elif opcion == "4":
            dataset_controller.buscar_dataset()
        elif opcion == "5":
            dataset_controller.editar_dataset()
        elif opcion == "6":
            dataset_controller.eliminar_dataset()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def menu_informes():
    """
    Muestra el submenú para informes y estadísticas
    """
    while True:
        print("\n--- INFORMES Y ESTADÍSTICAS ---")
        print("1. Evaluación general de cumplimiento")
        print("2. Informe de cumplimiento por sector")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            dataset_controller.evaluar_cumplimiento_datasets()
        elif opcion == "2":
            mostrar_informe_por_sector()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def mostrar_informe_por_sector():
    """
    Muestra un informe de cumplimiento por sector
    """
    stats_sectores = generar_informe_cumplimiento()
    
    if not stats_sectores:
        print("No hay datos para generar el informe.")
        return
        
    print("\n--- INFORME DE CUMPLIMIENTO POR SECTOR ---")
    
    for sector, stats in stats_sectores.items():
        if stats["total"] == 0:
            continue
            
        print(f"\nSector: {sector}")
        print(f"Total de datasets: {stats['total']}")
        print(f"Cumplen: {stats['cumplen']} ({stats['cumplen']/stats['total']*100:.1f}%)")
        print(f"Cumplen parcialmente: {stats['parcial']} ({stats['parcial']/stats['total']*100:.1f}%)")
        print(f"No cumplen: {stats['no_cumplen']} ({stats['no_cumplen']/stats['total']*100:.1f}%)")
        print("-" * 40)