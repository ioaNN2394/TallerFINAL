import time
import unittest

from AccesoDatos.MongoConnection import MongoConnection
from LogicaNegocio.CRUD import CRUD


class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.crud = CRUD.get_instance()
        self.mongo_connection = MongoConnection()
        self.mongo_connection.connect()
        self.crud.bd.db = self.mongo_connection.client["Restaurante"]
        self.crud.bd.collection = self.crud.bd.db["Mesas"]

    def test_database_operations_performance(self):
        reserva_info = {"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}

        start_time = time.time()
        self.crud.crear_reserva(reserva_info)
        create_time = time.time() - start_time
        print(f"Tiempo de creación: {create_time} segundos")

        start_time = time.time()
        self.crud.leer_reserva("Test")
        read_time = time.time() - start_time
        print(f"Tiempo de lectura: {read_time} segundos")

        start_time = time.time()
        self.crud.actualizar_reserva("Test", "Test2", "5")
        update_time = time.time() - start_time
        print(f"Tiempo de actualización: {update_time} segundos")

        start_time = time.time()
        self.crud.eliminar_reserva("Test2")
        delete_time = time.time() - start_time
        print(f"Tiempo de eliminación: {delete_time} segundos")

    def tearDown(self):
        self.crud.bd.collection.delete_many({})
