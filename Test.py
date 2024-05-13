import unittest
from unittest.mock import MagicMock
from AccesoDatos.DataBase import EntradasBlogGuardadas
from LogicaNegocio.CRUD import Singleton, CRUD

#--------------------------PRUEBAS UNITARIAS--------------------------
class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        instance1 = Singleton.get_instance()
        instance2 = Singleton.get_instance()
        self.assertEqual(instance1, instance2)

class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=EntradasBlogGuardadas)
        CRUD._instance = None
        self.crud = CRUD.get_instance()
        self.crud.bd = self.mock_db

    def test_crear_entrada(self):
        self.crud.crear_entrada("titulo", "contenido")
        self.mock_db.insertar_entrada.assert_called_with("titulo", "contenido")

    def test_leer_entradas(self):
        self.crud.leer_entradas()
        self.mock_db.obtener_entradas.assert_called()

    def test_leer_entrada(self):
        self.mock_db.obtener_entrada.return_value = None
        self.assertIsNone(self.crud.leer_entrada(1))

    def test_actualizar_entrada(self):
        self.mock_db.obtener_entrada.return_value = None
        self.assertEqual(self.crud.actualizar_entrada(1, "titulo", "contenido"), "Entrada con ID 1 no encontrada. No se pudo actualizar.")

    def test_eliminar_entrada(self):
        self.mock_db.obtener_entrada.return_value = None
        self.assertEqual(self.crud.eliminar_entrada(1), "Entrada con ID 1 no encontrada. No se pudo eliminar.")

if __name__ == '__main__':
    unittest.main()