from AccesoDatos.MongoConnection import MongoConnection


class TableModel:
    def __init__(self, connection: MongoConnection = None):
        self.mongo_connection = connection or MongoConnection()
        self.db = None
        self.collection = None
        self._initialize_connection()

    def _initialize_connection(self):
        self.mongo_connection.connect()
        self.db = self.mongo_connection.client["Restaurante"]
        self.collection = self.db["Mesas"]

    def insert_reserva(self, reserva_info):
        return self.collection.insert_one(reserva_info)

    def leer_entradas(self):
        return list(self.collection.find())

    def leer_reserva(self, nombre_reserva):
        return self.collection.find_one({"Nombre_Reserva": nombre_reserva})

    def obtener_entrada(self, nombre_reserva):
        return self.collection.find_one({"Nombre_Reserva": nombre_reserva})

    def modificar_entrada(self, nombre_reserva, nueva_reserva, cantidad_comensales):
        return self.collection.update_one(
            {"Nombre_Reserva": nombre_reserva},
            {
                "$set": {
                    "Nombre_Reserva": nueva_reserva,
                    "Cantidad_Comensales": cantidad_comensales,
                }
            },
        )

    def borrar_entrada(self, nombre_reserva):
        return self.collection.delete_one({"Nombre_Reserva": nombre_reserva})

    def contar_reservas(self):
        return self.collection.count_documents({})

    def close_connection(self):
        self.mongo_connection.close()


# Ejemplo de uso:
if __name__ == "__main__":
    table_model = TableModel()
    # Aquí puedes hacer llamadas a métodos de TableModel para interactuar con la base de datos.
    table_model.close_connection()
