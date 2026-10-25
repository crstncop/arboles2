
from modelo import arbol,TOTAL_OPERACIONES_FUSION,medicamento
from Base import  printTree


def menu():
    inventario = arbol()

    while True:
        print("\n--- INVENTARIO DE FARMACIA ---")
        print("1. Registrar medicamento")
        print("2. Vender medicamento")
        print("3. Eliminar por ID")
        print("4. Limpieza por caducidad")
        print("5. Consultar estado global")
        print("6. Mostrar inventario inverso")
        print("7. Consultar rango de IDs")
        print("8. Fusionar medicamentos")
        print("9. Imprimir árbol")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id = int(input("ID: "))
            nombre = input("Nombre: ")
            stock = int(input("Stock: "))
            año = int(input("Año de vencimiento: "))
            precio = float(input("Precio: "))

            nuevo = medicamento(id, nombre, stock, año, precio)
            inventario.registrar(nuevo)
            inventario.mostrar_estado()

        elif opcion == "2":
            id = int(input("ID del medicamento: "))
            cantidad = int(input("Cantidad a vender: "))

            resultado = inventario.busqueda_venta(
                id, cantidad, inventario.raiz
            )

            print(resultado)
            inventario.mostrar_estado()

        elif opcion == "3":
            id = int(input("ID a eliminar: "))
            inventario.eliminar_id(id)
            inventario.mostrar_estado()

        elif opcion == "4":
            año = int(input("Año actual: "))
            inventario.reporte_caducidad(año)
            inventario.mostrar_estado()

        elif opcion == "5":
            inventario.mostrar_estado()

        elif opcion == "6":
            if inventario.raiz is None:
                print("Inventario vacío")
            else:
                inventario.visualizar_inverso(inventario.raiz)

        elif opcion == "7":
            minimo = int(input("ID mínimo: "))
            maximo = int(input("ID máximo: "))

            if minimo > maximo:
                print("El ID mínimo no puede superar al máximo")
            else:
                inventario.consultar_rango(
                    minimo, maximo, inventario.raiz
                )

        elif opcion == "8":
            id_origen = int(input("ID del medicamento de origen: "))
            id_destino = int(input("ID del medicamento de destino: "))

            inventario.fusionar(id_origen, id_destino)
            inventario.mostrar_estado()

        elif opcion == "9":
            if inventario.raiz is None:
                print("Inventario vacío")
            else:
                print("\n--- ÁRBOL DE INVENTARIO ---")
                printTree(inventario.raiz)

        elif opcion == "0":
            print("Saliendo del sistema")
            break

        else:
            print("Opción inválida")


menu()

