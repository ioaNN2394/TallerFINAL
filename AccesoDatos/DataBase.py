class EntradasBlogGuardadas:
    def __init__(self):
        self.entradas = []

    def insertar_entrada(self, titulo, contenido):
        id_entrada = len(self.entradas) + 1
        self.entradas.append(
            {"id": id_entrada, "titulo": titulo, "contenido": contenido}
        )

    def obtener_entradas(self):
        return self.entradas

    def obtener_entrada(self, id_entrada):
        try:
            id_entrada = int(id_entrada)  # Convertir a entero
        except ValueError:
            print("Error: El ID de la entrada debe ser un número entero.")
            return None

        for entrada in self.entradas:
            if entrada["id"] == id_entrada:
                return entrada

        print(f"Entrada con ID {id_entrada} no encontrada.")
        return None

    def modificar_entrada(self, id_entrada, titulo, contenido):
        try:
            id_entrada = int(id_entrada)  # Convertir a entero
        except ValueError:
            print("Error: El ID de la entrada debe ser un número entero.")
            return

        entrada_encontrada = False
        for i in range(len(self.entradas)):
            if self.entradas[i]["id"] == id_entrada:
                self.entradas[i]["titulo"] = titulo
                self.entradas[i]["contenido"] = contenido
                print(f"Entrada con ID {id_entrada} modificada correctamente.")
                entrada_encontrada = True
                break

        if not entrada_encontrada:
            print(f"Entrada con ID {id_entrada} no encontrada. No se pudo modificar.")

    def borrar_entrada(self, id_entrada):
        try:
            id_entrada = int(id_entrada)  # Convertir a entero
        except ValueError:
            print("Error: El ID de la entrada debe ser un número entero.")
            return

        entrada_encontrada = False
        for entrada in self.entradas[:]:
            if entrada["id"] == id_entrada:
                self.entradas.remove(entrada)
                print(f"Entrada con ID {id_entrada} eliminada correctamente.")
                entrada_encontrada = True
                break

        if not entrada_encontrada:
            print(f"Entrada con ID {id_entrada} no encontrada. No se pudo eliminar.")
