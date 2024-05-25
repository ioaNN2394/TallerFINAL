from AccesoDatos.TablesDataBase import TableModel

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
    MAX_COMENSALES = 8
    MAX_MESAS = 9

    def __init__(self):
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.bd = TableModel()
            self.initialized = True

    def crear_reserva(self, reserva_info):
        if int(reserva_info['Cantidad_Comensales']) > self.MAX_COMENSALES:
            return "Error: Supera la cantidad máxima de comensales permitida (8)."
        if self.bd.contar_reservas() >= self.MAX_MESAS:
            return "Error: No hay mesas disponibles."
        self.bd.insert_reserva(reserva_info)
        return "Reserva creada exitosamente."

    def leer_entradas(self):
        return self.bd.leer_entradas()

    def leer_reserva(self, nombre_reserva):
        return self.bd.leer_reserva(nombre_reserva)

    def actualizar_reserva(self, nombre_reserva, nueva_reserva, cantidad_comensales):
        reserva_existente = self.bd.obtener_entrada(nombre_reserva)
        if reserva_existente:
            self.bd.modificar_entrada(nombre_reserva, nueva_reserva, cantidad_comensales)
            return f"Reserva a nombre de {nombre_reserva} actualizada correctamente."
        else:
            return f"Reserva a nombre de {nombre_reserva} no encontrada. No se pudo actualizar."

    def eliminar_reserva(self, nombre_reserva):
        reserva_existente = self.bd.obtener_entrada(nombre_reserva)
        if reserva_existente and reserva_existente.get('Cancelada', False):
            self.bd.borrar_entrada(nombre_reserva)
            return f"Reserva a nombre de {nombre_reserva} eliminada exitosamente."
        else:
            return f"Reserva a nombre de {nombre_reserva} no encontrada o no ha sido cancelada. No se pudo eliminar."
