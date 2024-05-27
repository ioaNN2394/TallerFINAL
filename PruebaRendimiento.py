import time

from AccesoDatos.TablesDataBase import TableModel

import threading


def realizar_operaciones(table_model, request_counter):
    start_time = time.perf_counter()
    table_model.insert_reserva({"Nombre_Reserva": "Prueba", "Cantidad_Comensales": 4})
    end_time = time.perf_counter()
    print(f"Tiempo de creación: {end_time - start_time} segundos")
    request_counter[0] += 1

    start_time = time.perf_counter()
    table_model.leer_entradas()
    end_time = time.perf_counter()
    print(f"Tiempo de lectura: {end_time - start_time} segundos")
    request_counter[0] += 1

    start_time = time.perf_counter()
    table_model.modificar_entrada("Prueba", "PruebaModificada", 5)
    end_time = time.perf_counter()
    print(f"Tiempo de actualización: {end_time - start_time} segundos")
    request_counter[0] += 1


if __name__ == "__main__":
    table_model = TableModel()
    print("Conectado a MongoDB")

    request_counter = [
        0
    ]  # Usamos una lista para que sea mutable y pueda ser actualizada dentro de la función
    start_time_global = time.perf_counter()

    threads = []
    for _ in range(1000):  # Crear 1000 hilos
        thread = threading.Thread(
            target=realizar_operaciones, args=(table_model, request_counter)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:  # Esperar a que todos los hilos terminen
        thread.join()

    end_time_global = time.perf_counter()
    print(f"Tiempo total de la prueba: {end_time_global - start_time_global} segundos")
    print(f"Cantidad total de solicitudes realizadas: {request_counter[0]}")
