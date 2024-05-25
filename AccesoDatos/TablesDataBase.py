from pymongo import MongoClient
from AccesoDatos.MongoConnection import MongoConnection

class TableModel:
    def __init__(self):
        self.mongo_connection = None
        self.db = None
        self.collection = None

    def connect(self):
        self.mongo_connection = MongoConnection()
        self.mongo_connection.connect()
        self.db = self.mongo_connection.client['Restaurante']
        self.collection = self.db['Mesas']

    def insert_reserva(self, reserva_info):
        if not self.mongo_connection:
            self.connect()
        return self.collection.insert_one(reserva_info)

    def leer_entradas(self):
        if not self.mongo_connection:
            self.connect()
        return list(self.collection.find())

    def leer_reserva(self, nombre_reserva):
        if not self.mongo_connection:
            self.connect()
        return self.collection.find_one({"Nombre_Reserva": nombre_reserva})

    def obtener_entrada(self, nombre_reserva):
        if not self.mongo_connection:
            self.connect()
        return self.collection.find_one({"Nombre_Reserva": nombre_reserva})

    def modificar_entrada(self, nombre_reserva, nueva_reserva, cantidad_comensales):
        if not self.mongo_connection:
            self.connect()
        return self.collection.update_one(
            {"Nombre_Reserva": nombre_reserva},
            {"$set": {"Nombre_Reserva": nueva_reserva, "Cantidad_Comensales": cantidad_comensales}}
        )

    def borrar_entrada(self, nombre_reserva):
        if not self.mongo_connection:
            self.connect()
        return self.collection.delete_one({"Nombre_Reserva": nombre_reserva})

    def contar_reservas(self):
        if not self.mongo_connection:
            self.connect()
        return self.collection.count_documents({})

    def close_connection(self):
        if self.mongo_connection:
            self.mongo_connection.close()
