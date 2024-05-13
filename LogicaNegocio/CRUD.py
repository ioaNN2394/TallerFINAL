from TallerFINAL.AccesoDatos.DataBase import EntradasBlogGuardadas

class Singleton:
    _instance = None

    def __init__(self):
        if self.__class__._instance is not None:
            raise Exception("No se puede crear una instancia de la clase Singleton")
        self.__class__._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class CRUD(Singleton):

    def __init__(self):
        super().__init__()
        self.bd = EntradasBlogGuardadas()

    def crear_entrada(self, titulo, contenido):
        self.bd.insertar_entrada(titulo, contenido)

    def leer_entradas(self):
        return self.bd.obtener_entradas()

    def leer_entrada(self, id_entrada):
        entrada = self.bd.obtener_entrada(id_entrada)
        if entrada:
            return entrada
        else:
            print(f"Entrada con ID {id_entrada} no encontrada.")
            return None

    def actualizar_entrada(self, id_entrada, titulo, contenido):
        entrada_existente = self.bd.obtener_entrada(id_entrada)
        if entrada_existente:
            self.bd.modificar_entrada(id_entrada, titulo, contenido)
            return f"Entrada con ID {id_entrada} actualizada correctamente."
        else:
            return f"Entrada con ID {id_entrada} no encontrada. No se pudo actualizar."

    def eliminar_entrada(self, id_entrada):
        entrada_existente = self.bd.obtener_entrada(id_entrada)
        if entrada_existente:
            self.bd.borrar_entrada(id_entrada)
            return f"Entrada con ID {id_entrada} eliminada exitosamente."
        else:
            return f"Entrada con ID {id_entrada} no encontrada. No se pudo eliminar."