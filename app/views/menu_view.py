from app.controllers import entidad_controller
from app.services.entidad_service import cargar_datos_api

def mostrar_menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Cargar datos desde API")
        print("2. Crear entidad")
        print("3. Listar entidades")
        print("4. Buscar entidad por ID")
        print("5. Editar entidad")
        print("6. Eliminar entidad")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cargar_datos_api()
        elif opcion == "2":
            entidad_controller.crear_entidad()
        elif opcion == "3":
            entidad_controller.listar_entidades()
        elif opcion == "4":
            entidad_controller.buscar_entidad()
        elif opcion == "5":
            entidad_controller.editar_entidad()
        elif opcion == "6":
            entidad_controller.eliminar_entidad()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")