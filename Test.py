import unittest
from unittest.mock import MagicMock
from AccesoDatos.DataBase import EntradasBlogGuardadas
from LogicaNegocio.CRUD import Singleton, CRUD
import pyautogui
import time
from subprocess import Popen
import os
import unittest
from AccesoDatos.DataBase import EntradasBlogGuardadas

#Pruebas de Integracion

class TestEntradasBlogGuardadas(unittest.TestCase):

    def setUp(self):
        self.blog = EntradasBlogGuardadas()

    def test_insertar_y_obtener_entrada(self):
        self.blog.insertar_entrada("Titulo 1", "Contenido 1")
        entrada = self.blog.obtener_entrada(1)
        self.assertEqual(entrada["titulo"], "Titulo 1")
        self.assertEqual(entrada["contenido"], "Contenido 1")

    def test_modificar_entrada(self):
        self.blog.insertar_entrada("Titulo 1", "Contenido 1")
        self.blog.modificar_entrada(1, "Titulo 2", "Contenido 2")
        entrada = self.blog.obtener_entrada(1)
        self.assertEqual(entrada["titulo"], "Titulo 2")
        self.assertEqual(entrada["contenido"], "Contenido 2")

    def test_borrar_entrada(self):
        self.blog.insertar_entrada("Titulo 1", "Contenido 1")
        self.blog.borrar_entrada(1)
        entrada = self.blog.obtener_entrada(1)
        self.assertIsNone(entrada)

    def test_manejo_de_errores(self):
        entrada = self.blog.obtener_entrada(999)
        self.assertIsNone(entrada)
        self.blog.modificar_entrada(999, "Titulo 2", "Contenido 2")
        self.blog.borrar_entrada(999)

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

#Prueba end to end

def test_end_to_end():
    # Iniciar la aplicación
    p = Popen(['python', 'ruta/a/tu/archivo.py'])
    time.sleep(5)  # Esperar a que la aplicación se inicie

    # Crear entrada
    pyautogui.click(100, 100)  # Coordenadas del botón "Crear entrada"
    pyautogui.write('Titulo de prueba', interval=0.1)
    pyautogui.press('enter')
    pyautogui.write('Contenido de prueba', interval=0.1)
    pyautogui.press('enter')
    time.sleep(2)  # Esperar a que se cree la entrada

    # Ver entradas
    pyautogui.click(200, 100)  # Coordenadas del botón "Ver entradas"
    time.sleep(2)  # Esperar a que se muestren las entradas

    # Actualizar entrada
    pyautogui.click(100, 200)  # Coordenadas del botón "Actualizar entrada"
    pyautogui.write('1', interval=0.1)  # ID de la entrada
    pyautogui.press('enter')
    pyautogui.write('Nuevo titulo', interval=0.1)
    pyautogui.press('enter')
    pyautogui.write('Nuevo contenido', interval=0.1)
    pyautogui.press('enter')
    time.sleep(2)  # Esperar a que se actualice la entrada

    # Ver entrada específica
    pyautogui.click(200, 200)  # Coordenadas del botón "Ver entrada específica"
    pyautogui.write('1', interval=0.1)  # ID de la entrada
    pyautogui.press('enter')
    time.sleep(2)  # Esperar a que se muestre la entrada

    # Eliminar entrada pruebas
    pyautogui.click(100, 300)  # Coordenadas del botón "Eliminar entrada"
    pyautogui.write('1', interval=0.1)  # ID de la entrada
    pyautogui.press('enter')
    time.sleep(2)  # Esperar a que se elimine la entrada

    # Cerrar la aplicación
    p.terminate()


if __name__ == '__main__':
    unittest.main()