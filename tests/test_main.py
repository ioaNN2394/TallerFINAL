from LogicaNegocio import CRUD
from AccesoDatos import MongoConnection
import unittest
from unittest.mock import patch, MagicMock
from Presentacion.Menu import Menu
import pytest

# ---------------------------PRUEBAS UNITARIAS----------------------------------


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.bd_mock = unittest.mock.MagicMock(spec=CRUD.CRUD)  # Mock de CRUD
        self.menu = Menu(self.bd_mock)  # Instanciamos Menu con el mock

    # Pruebas unitarias con mocking

    def test_opcion_crear_reserva(self):
        with patch("builtins.input", side_effect=["John Doe", "4"]):
            self.menu.opcion_crear_reserva()
        self.bd_mock.crear_reserva.assert_called_once_with(
            {"Nombre_Reserva": "John Doe", "Cantidad_Comensales": "4"}
        )

    def test_opcion_ver_mesas_reservadas(self):
        self.bd_mock.leer_entradas.return_value = [
            {"Nombre_Reserva": "John Doe", "Cantidad_Comensales": "4"},
            {"Nombre_Reserva": "Jane Smith", "Cantidad_Comensales": "2"},
        ]
        with patch("builtins.print") as mock_print:
            self.menu.opcion_ver_mesas_reservadas()
            mock_print.assert_any_call(
                "\nNombre de la reserva: John Doe\nCantidad de comensales: 4"
            )
            mock_print.assert_any_call(
                "\nNombre de la reserva: Jane Smith\nCantidad de comensales: 2"
            )

    def test_opcion_actualizar_reserva(self):
        with patch("builtins.input", side_effect=["John Doe", "Jane Doe", "5"]):
            self.menu.opcion_actualizar_reserva()
        self.bd_mock.actualizar_reserva.assert_called_once_with(
            "John Doe", "Jane Doe", "5"
        )

    def test_opcion_eliminar_reserva(self):
        with patch("builtins.input", return_value="John Doe"):
            self.menu.opcion_eliminar_reserva()
        self.bd_mock.eliminar_reserva.assert_called_once_with("John Doe")


@pytest.mark.skip(reason="CI")
class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.crud = CRUD.CRUD.get_instance()
        self.crud.bd.mongo_connection.connect()

    def test_should_create_a_reservation(self):
        self.crud.bd.insert_reserva = MagicMock(return_value=True)
        result = self.crud.crear_reserva(
            {"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}
        )
        self.assertEqual(result, "Reserva creada exitosamente.")

    def test_should_not_create_reservation_if_max_comensales_exceeded(self):
        result = self.crud.crear_reserva(
            {"Nombre_Reserva": "Test", "Cantidad_Comensales": "10"}
        )
        self.assertEqual(
            result, "Error: Supera la cantidad máxima de comensales permitida (8)."
        )

    def test_should_not_create_reservation_if_max_tables_exceeded(self):
        self.crud.bd.contar_reservas = MagicMock(return_value=10)
        result = self.crud.crear_reserva(
            {"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}
        )
        self.assertEqual(result, "Error: No hay mesas disponibles.")

    def test_should_read_entries(self):
        self.crud.bd.leer_entradas = MagicMock(
            return_value=[{"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}]
        )
        result = self.crud.leer_entradas()
        self.assertEqual(
            result, [{"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}]
        )

    def test_should_update_reservation(self):
        self.crud.bd.obtener_entrada = MagicMock(
            return_value={"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}
        )
        self.crud.bd.modificar_entrada = MagicMock(return_value=True)
        result = self.crud.actualizar_reserva("Test", "Test2", "5")
        self.assertEqual(result, "Reserva a nombre de Test actualizada correctamente.")

    def test_should_not_update_reservation_if_not_found(self):
        self.crud.bd.obtener_entrada = MagicMock(return_value=None)
        result = self.crud.actualizar_reserva("Test", "Test2", "5")
        self.assertEqual(
            result, "Reserva a nombre de Test no encontrada. No se pudo actualizar."
        )

    def test_should_delete_reservation(self):
        self.crud.bd.obtener_entrada = MagicMock(
            return_value={
                "Nombre_Reserva": "Test",
                "Cantidad_Comensales": "4",
                "Cancelada": True,
            }
        )
        self.crud.bd.borrar_entrada = MagicMock(return_value=True)
        result = self.crud.eliminar_reserva("Test")
        self.assertEqual(result, "Reserva a nombre de Test eliminada exitosamente.")

    def test_should_not_delete_reservation_if_not_found_or_not_cancelled(self):
        self.crud.bd.obtener_entrada = MagicMock(return_value=None)
        result = self.crud.eliminar_reserva("Test")
        self.assertEqual(
            result,
            "Reserva a nombre de Test no encontrada o no ha sido cancelada. No se pudo eliminar.",
        )

    @pytest.mark.skip(reason="CI")
    def test_flujo_completo_crear_y_ver_reserva(self):
        bd = CRUD.CRUD.get_instance()  # Usamos una instancia real de CRUD
        menu = Menu(bd)

        with patch("builtins.input", side_effect=["3", "John Doe", "4", "1", "5", "s"]):
            menu.menu()

        reservas = bd.leer_entradas()
        # Asegurarse de que el diccionario existe en la lista, sin importar el valor de _id
        self.assertTrue(
            any(
                r["Nombre_Reserva"] == "John Doe" and r["Cantidad_Comensales"] == "4"
                for r in reservas
            )
        )


@pytest.mark.skip(reason="CI")
# ---------------------------PRUEBAS INTEGRACIÓN----------------------------------
class TestBD(unittest.TestCase):
    def setUp(self):
        self.crud = CRUD.CRUD.get_instance()
        self.mongo_connection = MongoConnection.MongoConnection()
        self.mongo_connection.connect()
        self.crud.bd.db = self.mongo_connection.client["Restaurante"]
        self.crud.bd.collection = self.crud.bd.db["Mesas"]

    def test_should_create_a_reservation_in_database(self):
        reserva_info = {"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}
        self.crud.crear_reserva(reserva_info)
        reserva_in_db = self.crud.bd.leer_reserva("Test")
        self.assertEqual(reserva_in_db["Nombre_Reserva"], "Test")
        self.assertEqual(reserva_in_db["Cantidad_Comensales"], "4")

    def test_should_update_reservation_in_database(self):
        reserva_info = {"Nombre_Reserva": "Test", "Cantidad_Comensales": "4"}
        self.crud.crear_reserva(reserva_info)
        self.crud.actualizar_reserva("Test", "Test2", "5")
        reserva_in_db = self.crud.bd.leer_reserva("Test2")
        self.assertEqual(reserva_in_db["Nombre_Reserva"], "Test2")
        self.assertEqual(reserva_in_db["Cantidad_Comensales"], "5")

    def test_should_delete_reservation_in_database(self):
        reserva_info = {
            "Nombre_Reserva": "Test",
            "Cantidad_Comensales": "4",
            "Cancelada": True,
        }
        self.crud.crear_reserva(reserva_info)
        self.crud.eliminar_reserva("Test")
        reserva_in_db = self.crud.bd.leer_reserva("Test")
        self.assertIsNone(reserva_in_db)

    def tearDown(self):
        self.crud.bd.collection.delete_many({})


if __name__ == "__main__":
    unittest.main()
