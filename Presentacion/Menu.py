from LogicaNegocio import CRUD


class Menu:
    def __init__(self, bd):
        self.bd = bd

    def menu(self):
        while True:
            print("\nElige una opción:")
            print("1. Ver mesas reservadas")
            print("2. Actualizar reserva")
            print("3. Crear reserva")
            print("4. Eliminar reserva")
            print("5. Salir")
            opcion = input("Introduce el número de la opción: ")

            if opcion == "1":
                self.opcion_ver_mesas_reservadas()
            elif opcion == "2":
                self.opcion_actualizar_reserva()
            elif opcion == "3":
                self.opcion_crear_reserva()
            elif opcion == "4":
                self.opcion_eliminar_reserva()
            elif opcion == "5":
                if input("¿Está seguro que desea salir? (s/n): ").lower() == "s":
                    break
            else:
                print("Opción no válida. Por favor, introduce un número del 1 al 5.")

    def opcion_crear_reserva(self):
        nombre_reserva = input("A nombre de quien es la reserva: ")
        cantidad_comensales = input("Introduce la cantidad de comensales (máximo 8): ")
        mensaje = self.bd.crear_reserva(
            {
                "Nombre_Reserva": nombre_reserva,
                "Cantidad_Comensales": cantidad_comensales,
            }
        )
        print(mensaje)

    def opcion_ver_mesas_reservadas(self):
        reservas = self.bd.leer_entradas()
        for reserva in reservas:
            print(
                f"\nNombre de la reserva: {reserva['Nombre_Reserva']}\nCantidad de comensales: {reserva['Cantidad_Comensales']}"
            )

    def opcion_actualizar_reserva(self):
        nombre_reserva = input("Introduce a nombre de quien quedó la reserva: ")
        nueva_reserva = input("Introduce el nombre de quien reservó: ")
        cantidad_comensales = input("Introduce la nueva cantidad de comensales: ")
        mensaje = self.bd.actualizar_reserva(
            nombre_reserva, nueva_reserva, cantidad_comensales
        )
        print(mensaje)

    def opcion_eliminar_reserva(self):
        nombre_reserva = input("Introduce a nombre de quien se cancelará la reserva: ")
        mensaje = self.bd.eliminar_reserva(nombre_reserva)
        print(mensaje)


if __name__ == "__main__":
    bd = CRUD.CRUD.get_instance()  # Create an instance of CRUD
    menu = Menu(bd)  # Pass the instance of CRUD as the first argument
    menu.menu()
