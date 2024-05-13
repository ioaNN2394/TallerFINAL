from TallerFINAL.LogicaNegocio.CRUD import CRUD

class Blog:

    def __init__(self):
        self.bd = CRUD.get_instance()

    def menu(self):
        print("1. Crear entrada")
        print("2. Ver entradas")
        print("3. Ver una entrada en especifico")
        print("4. Actualizar entrada")
        print("5. Eliminar entrada")
        print("6. Salir")
        opcion = input("Elige una opción: ")
        return opcion

    def main(self):
        opciones = {
            "1": self.opcion_crear_entrada,
            "2": self.opcion_ver_entradas,
            "3": self.opcion_ver_entrada_especifica,
            "4": self.opcion_actualizar_entrada,
            "5": self.opcion_eliminar_entrada,
            "6": self.opcion_salir

        }

        while True:
            opcion = self.menu()
            opciones.get(opcion, self.opcion_invalida)()

    def opcion_crear_entrada(self):
        titulo = input("Introduce el título de la entrada: ")
        contenido = input("Introduce el contenido de la entrada: ")
        self.bd.crear_entrada(titulo, contenido)

    def opcion_ver_entradas(self):
        entradas = self.bd.leer_entradas()
        for entrada in entradas:
            print(entrada)

    def opcion_ver_entrada_especifica(self):
        id_entrada = input("Introduce el ID de la entrada a leer: ")
        entrada = self.bd.leer_entrada(id_entrada)
        print(entrada)

    def opcion_actualizar_entrada(self):
        id_entrada = input("Introduce el ID de la entrada a actualizar: ")
        titulo = input("Introduce el nuevo título de la entrada: ")
        contenido = input("Introduce el nuevo contenido de la entrada: ")
        self.bd.actualizar_entrada(id_entrada, titulo, contenido)

    def opcion_eliminar_entrada(self):
        id_entrada = input("Introduce el ID de la entrada a eliminar: ")
        self.bd.eliminar_entrada(id_entrada)

    def opcion_salir(self):
        raise StopIteration("Saliendo del programa")

    def opcion_invalida(self):
        print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    blog = Blog()
    blog.main()